#!/usr/bin/env python
import os
import sys
import json
import requests
import pydicom
from io import BytesIO
from datetime import datetime

# Ajouter le répertoire du projet au chemin Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurer l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

from django.conf import settings
from patients.models import Patient
from imaging.models import DicomStudy, DicomSeries, DicomInstance

# Configuration d'Orthanc
ORTHANC_URL = settings.ORTHANC_URL
ORTHANC_USERNAME = settings.ORTHANC_USERNAME
ORTHANC_PASSWORD = settings.ORTHANC_PASSWORD

def get_orthanc_studies():
    """Récupérer la liste des études depuis Orthanc."""
    try:
        response = requests.get(
            f"{ORTHANC_URL}/studies",
            auth=(ORTHANC_USERNAME, ORTHANC_PASSWORD)
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erreur lors de la récupération des études: {response.text}")
            return []
    except Exception as e:
        print(f"Exception lors de la récupération des études: {str(e)}")
        return []

def get_study_details(study_id):
    """Récupérer les détails d'une étude depuis Orthanc."""
    try:
        response = requests.get(
            f"{ORTHANC_URL}/studies/{study_id}",
            auth=(ORTHANC_USERNAME, ORTHANC_PASSWORD)
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erreur lors de la récupération des détails de l'étude {study_id}: {response.text}")
            return None
    except Exception as e:
        print(f"Exception lors de la récupération des détails de l'étude {study_id}: {str(e)}")
        return None

def get_series_details(series_id):
    """Récupérer les détails d'une série depuis Orthanc."""
    try:
        response = requests.get(
            f"{ORTHANC_URL}/series/{series_id}",
            auth=(ORTHANC_USERNAME, ORTHANC_PASSWORD)
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erreur lors de la récupération des détails de la série {series_id}: {response.text}")
            return None
    except Exception as e:
        print(f"Exception lors de la récupération des détails de la série {series_id}: {str(e)}")
        return None

def get_instance_details(instance_id):
    """Récupérer les détails d'une instance depuis Orthanc."""
    try:
        response = requests.get(
            f"{ORTHANC_URL}/instances/{instance_id}",
            auth=(ORTHANC_USERNAME, ORTHANC_PASSWORD)
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erreur lors de la récupération des détails de l'instance {instance_id}: {response.text}")
            return None
    except Exception as e:
        print(f"Exception lors de la récupération des détails de l'instance {instance_id}: {str(e)}")
        return None

def get_instance_dicom(instance_id):
    """Récupérer le fichier DICOM d'une instance depuis Orthanc."""
    try:
        response = requests.get(
            f"{ORTHANC_URL}/instances/{instance_id}/file",
            auth=(ORTHANC_USERNAME, ORTHANC_PASSWORD)
        )
        
        if response.status_code == 200:
            return response.content
        else:
            print(f"Erreur lors de la récupération du fichier DICOM de l'instance {instance_id}: {response.text}")
            return None
    except Exception as e:
        print(f"Exception lors de la récupération du fichier DICOM de l'instance {instance_id}: {str(e)}")
        return None

def synchronize_studies():
    """Synchroniser les études DICOM d'Orthanc avec la base de données Django."""
    # Récupérer la liste des études depuis Orthanc
    study_ids = get_orthanc_studies()
    
    if not study_ids:
        print("Aucune étude trouvée dans Orthanc.")
        return
    
    print(f"Nombre d'études trouvées dans Orthanc: {len(study_ids)}")
    
    # Traiter chaque étude
    for study_id in study_ids:
        study_details = get_study_details(study_id)
        
        if not study_details:
            continue
        
        # Extraire les métadonnées de l'étude
        study_main_dicom_tags = study_details.get('MainDicomTags', {})
        patient_main_dicom_tags = study_details.get('PatientMainDicomTags', {})
        
        # Extraire les informations du patient
        patient_id = patient_main_dicom_tags.get('PatientID', '')
        patient_name = patient_main_dicom_tags.get('PatientName', '')
        patient_birth_date_str = patient_main_dicom_tags.get('PatientBirthDate', '')
        patient_sex = patient_main_dicom_tags.get('PatientSex', '')
        
        # Traiter le nom du patient (format: "Nom^Prénom")
        if '^' in patient_name:
            last_name, first_name = patient_name.split('^', 1)
        else:
            last_name, first_name = patient_name, ''
        
        # Convertir la date de naissance
        try:
            if patient_birth_date_str:
                patient_birth_date = datetime.strptime(patient_birth_date_str, '%Y%m%d').date()
            else:
                patient_birth_date = None
        except ValueError:
            print(f"Format de date de naissance invalide: {patient_birth_date_str}")
            patient_birth_date = None
        
        # Convertir le sexe
        if patient_sex == 'M':
            gender = 'M'
        elif patient_sex == 'F':
            gender = 'F'
        else:
            gender = 'O'
        
        # Vérifier si le patient existe déjà
        patient = Patient.objects.filter(social_security_number=patient_id).first()
        
        if not patient:
            # Créer un nouveau patient
            patient = Patient.objects.create(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=patient_birth_date or datetime.now().date(),
                gender=gender,
                social_security_number=patient_id
            )
            print(f"Nouveau patient créé: {patient}")
        else:
            print(f"Patient existant: {patient}")
        
        # Extraire les informations de l'étude
        study_instance_uid = study_main_dicom_tags.get('StudyInstanceUID', '')
        study_date_str = study_main_dicom_tags.get('StudyDate', '')
        study_time_str = study_main_dicom_tags.get('StudyTime', '')
        study_description = study_main_dicom_tags.get('StudyDescription', '')
        modality = study_main_dicom_tags.get('Modality', '')
        
        # Convertir la date et l'heure de l'étude
        try:
            if study_date_str:
                study_date = datetime.strptime(study_date_str, '%Y%m%d').date()
            else:
                study_date = datetime.now().date()
                
            if study_time_str:
                # Gérer les formats d'heure possibles (HHMMSS, HHMMSS.ffffff)
                if '.' in study_time_str:
                    study_time_str = study_time_str.split('.')[0]
                
                if len(study_time_str) == 6:
                    study_time = datetime.strptime(study_time_str, '%H%M%S').time()
                else:
                    study_time = datetime.now().time()
            else:
                study_time = datetime.now().time()
        except ValueError as e:
            print(f"Erreur de format de date/heure: {e}")
            study_date = datetime.now().date()
            study_time = datetime.now().time()
        
        # Vérifier si l'étude existe déjà
        study = DicomStudy.objects.filter(study_instance_uid=study_instance_uid).first()
        
        if not study:
            # Créer une nouvelle étude
            study = DicomStudy.objects.create(
                patient=patient,
                study_instance_uid=study_instance_uid,
                study_date=study_date,
                study_time=study_time,
                study_description=study_description,
                modality=modality,
                orthanc_id=study_id,
                status='COMPLETED'
            )
            print(f"Nouvelle étude créée: {study}")
        else:
            # Mettre à jour l'étude existante
            study.study_date = study_date
            study.study_time = study_time
            study.study_description = study_description
            study.modality = modality
            study.orthanc_id = study_id
            study.status = 'COMPLETED'
            study.save()
            print(f"Étude mise à jour: {study}")
        
        # Traiter les séries de l'étude
        for series_id in study_details.get('Series', []):
            series_details = get_series_details(series_id)
            
            if not series_details:
                continue
            
            # Extraire les métadonnées de la série
            series_main_dicom_tags = series_details.get('MainDicomTags', {})
            series_instance_uid = series_main_dicom_tags.get('SeriesInstanceUID', '')
            series_number = series_main_dicom_tags.get('SeriesNumber', 0)
            series_description = series_main_dicom_tags.get('SeriesDescription', '')
            
            # Vérifier si la série existe déjà
            series = DicomSeries.objects.filter(series_instance_uid=series_instance_uid).first()
            
            if not series:
                # Créer une nouvelle série
                series = DicomSeries.objects.create(
                    study=study,
                    series_instance_uid=series_instance_uid,
                    series_number=series_number,
                    series_description=series_description,
                    orthanc_id=series_id
                )
                print(f"Nouvelle série créée: {series}")
            else:
                # Mettre à jour la série existante
                series.series_number = series_number
                series.series_description = series_description
                series.orthanc_id = series_id
                series.save()
                print(f"Série mise à jour: {series}")
            
            # Traiter les instances de la série
            for instance_id in series_details.get('Instances', []):
                instance_details = get_instance_details(instance_id)
                
                if not instance_details:
                    continue
                
                # Extraire les métadonnées de l'instance
                instance_main_dicom_tags = instance_details.get('MainDicomTags', {})
                sop_instance_uid = instance_main_dicom_tags.get('SOPInstanceUID', '')
                instance_number = instance_main_dicom_tags.get('InstanceNumber', 0)
                
                # Vérifier si l'instance existe déjà
                instance = DicomInstance.objects.filter(sop_instance_uid=sop_instance_uid).first()
                
                if not instance:
                    # Créer une nouvelle instance
                    instance = DicomInstance.objects.create(
                        series=series,
                        sop_instance_uid=sop_instance_uid,
                        instance_number=instance_number,
                        orthanc_id=instance_id
                    )
                    print(f"Nouvelle instance créée: {instance}")
                    
                    # Télécharger le fichier DICOM
                    dicom_data = get_instance_dicom(instance_id)
                    
                    if dicom_data:
                        try:
                            # Parser les données DICOM
                            ds = pydicom.dcmread(BytesIO(dicom_data))
                            
                            # Enregistrer le fichier DICOM
                            file_name = f"{sop_instance_uid}.dcm"
                            file_path = f"dicom_files/{patient.id}/{study.study_date.strftime('%Y%m%d')}/{file_name}"
                            
                            # Créer les répertoires si nécessaire
                            os.makedirs(os.path.dirname(f"media/{file_path}"), exist_ok=True)
                            
                            with open(f"media/{file_path}", 'wb') as f:
                                f.write(dicom_data)
                            
                            instance.file.name = file_path
                            instance.save()
                            
                            print(f"Fichier DICOM enregistré pour l'instance {instance}")
                        except Exception as e:
                            print(f"Erreur lors du traitement du fichier DICOM: {str(e)}")
                    else:
                        print(f"Aucune donnée DICOM récupérée pour l'instance {instance}")
                else:
                    # Mettre à jour l'instance existante
                    instance.instance_number = instance_number
                    instance.save()
                    print(f"Instance mise à jour: {instance}")

if __name__ == "__main__":
    print("Début de la synchronisation des études DICOM...")
    synchronize_studies()
    print("Synchronisation terminée.")