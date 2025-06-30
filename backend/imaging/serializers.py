import base64
from rest_framework import serializers
from .models import DicomStudy, DicomSeries, DicomInstance, RadiologyReport, ActionLog

class ActionLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    class Meta:
        model = ActionLog
        fields = ['id', 'user', 'user_name', 'action', 'target_type', 'target_id', 'timestamp', 'status', 'message']
        read_only_fields = ['id', 'timestamp']

class DicomInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DicomInstance
        fields = ['id', 'series', 'sop_instance_uid', 'instance_number', 'file', 
                  'orthanc_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class DicomSeriesSerializer(serializers.ModelSerializer):
    instances = DicomInstanceSerializer(many=True, read_only=True)
    
    class Meta:
        model = DicomSeries
        fields = ['id', 'study', 'series_instance_uid', 'series_number', 
                  'series_description', 'body_part', 'orthanc_id', 
                  'instances', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class DicomStudySerializer(serializers.ModelSerializer):
    series = DicomSeriesSerializer(many=True, read_only=True)
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    uploaded_by_name = serializers.CharField(source='uploaded_by.full_name', read_only=True)
    dicom_file = serializers.FileField(write_only=True, required=False)
    
    class Meta:
        model = DicomStudy
        fields = ['id', 'patient', 'patient_name', 'medical_record', 
                  'study_instance_uid', 'study_date', 'study_time', 
                  'study_description', 'modality', 'orthanc_id', 
                  'status', 'uploaded_by', 'uploaded_by_name', 
                  'uploaded_at', 'updated_at', 'series', 'dicom_file']
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at', 'updated_at']
    
    def create(self, validated_data):
        from .models import DicomSeries, DicomInstance
        import uuid
        from django.utils import timezone
        import requests
        from django.conf import settings
        import logging
        
        logger = logging.getLogger(__name__)
        
        # Extraire le fichier DICOM s'il est présent
        dicom_file = validated_data.pop('dicom_file', None)
        
        # Préparer les données pour la création de l'étude
        study_data = validated_data.copy()
        
        # Définir les valeurs par défaut si elles ne sont pas fournies
        if 'study_date' not in study_data:
            study_data['study_date'] = timezone.now().date()
        if 'study_time' not in study_data:
            study_data['study_time'] = timezone.now().time()
        if 'status' not in study_data:
            study_data['status'] = 'UPLOADED'
        
        # Si un fichier DICOM est fourni, l'envoyer à Orthanc
        orthanc_id = None
        if dicom_file:
            try:
                # Vérifier que le fichier a une taille valide
                if not dicom_file:
                    raise ValueError("Aucun fichier DICOM fourni")
                    
                # Sauvegarder la position du curseur du fichier
                current_position = dicom_file.tell()
                
                # Lire le contenu du fichier
                file_content = dicom_file.read()
                
                # Vérifier que le fichier n'est pas vide
                if not file_content:
                    raise ValueError("Le fichier DICOM est vide")
                
                # Vérifier la signature DICOM (DICM à l'offset 128)
                if len(file_content) > 132 and file_content[128:132] != b'DICM':
                    logger.warning("Le fichier ne semble pas être un fichier DICOM valide (signature DICM manquante)")
                
                # Configuration Orthanc
                orthanc_url = 'http://localhost:8042/instances'
                
                # Log des informations de débogage
                logger.info(f"Envoi du fichier DICOM à Orthanc: {orthanc_url}")
                logger.info(f"Taille du fichier: {len(file_content)} octets")
                logger.debug(f"Début du contenu (hex): {file_content[:16].hex() if file_content else 'vide'}")
                
                # Réinitialiser le curseur du fichier pour une lecture ultérieure
                dicom_file.seek(0)  # Toujours revenir au début du fichier
                
                # En-têtes de la requête
                headers = {
                    'Content-Type': 'application/dicom',
                    'Accept': 'application/json',
                    'Content-Length': str(len(file_content))  # Ajouter la taille du contenu
                }
                
                try:
                    logger.info(f"Envoi de {len(file_content)} octets vers {orthanc_url}")
                    
                    # Envoyer la requête à Orthanc sans authentification
                    response = requests.post(
                        orthanc_url,
                        data=file_content,
                        headers=headers,
                        timeout=30
                    )
                    
                    logger.info(f"Réponse d'Orthanc: {response.status_code} - {response.reason}")
                    logger.debug(f"En-têtes de la réponse: {dict(response.headers)}")
                    
                    response.raise_for_status()
                    logger.info("Fichier DICOM envoyé avec succès à Orthanc")
                    
                except Exception as e:
                    logger.error(f"Erreur lors de l'envoi à Orthanc: {str(e)}")
                    if hasattr(e, 'response') and e.response is not None:
                        logger.error(f"Réponse d'erreur: {e.response.text}")
                    raise
                
                # Log de la réponse brute
                logger.info(f"Code de statut de la réponse: {response.status_code}")
                logger.info(f"En-têtes de la réponse: {dict(response.headers)}")
                try:
                    logger.info(f"Corps de la réponse: {response.text[:500]}")
                except Exception as e:
                    logger.error(f"Erreur lors de la lecture du corps de la réponse: {str(e)}")
                response.raise_for_status()
                
                # Récupérer l'ID de l'étude Orthanc
                orthanc_data = response.json()
                orthanc_id = orthanc_data.get('ParentStudy', orthanc_data.get('ID'))
                
                # Mettre à jour les métadonnées avec les informations d'Orthanc si disponibles
                if 'MainDicomTags' in orthanc_data:
                    tags = orthanc_data['MainDicomTags']
                    study_data.update({
                        'study_instance_uid': tags.get('StudyInstanceUID', study_data.get('study_instance_uid', '')),
                        'study_date': tags.get('StudyDate', study_data.get('study_date')),
                        'study_description': tags.get('StudyDescription', study_data.get('study_description', '')),
                        'modality': tags.get('Modality', study_data.get('modality', 'OT'))
                    })
                
            except Exception as e:
                # En cas d'erreur, on continue quand même la création de l'étude
                # mais on journalise l'erreur
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Erreur lors de l'envoi à Orthanc: {str(e)}")
        
        # Ajouter l'ID Orthanc aux données de l'étude si disponible
        if orthanc_id:
            study_data['orthanc_id'] = orthanc_id
            
        # Ajouter l'utilisateur qui a téléversé le fichier
        study_data['uploaded_by'] = self.context['request'].user
        
        # Créer l'étude DICOM
        study = DicomStudy.objects.create(**study_data)
        
        # Si un fichier DICOM est fourni, créer une série et une instance
        if dicom_file:
            # Créer une série pour cette étude
            series = DicomSeries.objects.create(
                study=study,
                series_instance_uid=str(uuid.uuid4()),
                series_number=1,
                series_description=study_data.get('study_description', 'Série principale')
            )
            
            # Créer une instance pour cette série
            instance_data = {
                'series': series,
                'sop_instance_uid': str(uuid.uuid4()),
                'instance_number': 1,
                'file': dicom_file
            }
            if orthanc_id:
                instance_data['orthanc_id'] = orthanc_id
                
            DicomInstance.objects.create(**instance_data)
        
        return study

class RadiologyReportSerializer(serializers.ModelSerializer):
    study_description = serializers.CharField(source='study.study_description', read_only=True)
    patient_name = serializers.CharField(source='study.patient.full_name', read_only=True)
    radiologist_name = serializers.CharField(source='radiologist.full_name', read_only=True)
    
    class Meta:
        model = RadiologyReport
        fields = ['id', 'study', 'study_description', 'patient_name', 
                  'radiologist', 'radiologist_name', 'findings', 
                  'impression', 'recommendations', 'status', 
                  'created_at', 'updated_at', 'finalized_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'finalized_at']
