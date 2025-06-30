from django.db import models
from django.utils import timezone
from authentication.models import User
from patients.models import Patient, MedicalRecord
import uuid
import os

class ActionLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='action_logs')
    action = models.CharField(max_length=100)
    target_type = models.CharField(max_length=100)
    target_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('SUCCESS', 'Succès'), ('FAIL', 'Échec')])
    message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.action} - {self.status}"

    class Meta:
        app_label = 'imaging'
        db_table = 'imaging_action_logs'
        verbose_name = 'Log d\'action'
        verbose_name_plural = 'Logs d\'action'
        ordering = ['-timestamp']

def dicom_file_path(instance, filename):
    """
    Génère le chemin de stockage pour les fichiers DICOM.
    Format: dicom_files/patient_id/study_date/original_filename
    """
    # Vérifier si l'instance a un fichier et une série associée
    if hasattr(instance, 'series') and instance.series and hasattr(instance.series, 'study'):
        study = instance.series.study
        patient_id = study.patient.id
        date_str = study.study_date.strftime('%Y%m%d')
        return f'dicom_files/{patient_id}/{date_str}/{filename}'
    
    # Fallback si les relations ne sont pas disponibles
    return f'dicom_files/unknown/{timezone.now().strftime("%Y%m%d")}/{filename}'

class DicomStudy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='dicom_studies')
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.SET_NULL, null=True, blank=True, related_name='dicom_studies')
    
    # DICOM metadata
    study_instance_uid = models.CharField(max_length=100, unique=True)
    study_date = models.DateField(default=timezone.now)
    study_time = models.TimeField(default=timezone.now)
    study_description = models.CharField(max_length=200, blank=True, null=True)
    modality = models.CharField(max_length=50)
    
    # Orthanc metadata
    orthanc_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('UPLOADED', 'Téléchargé'),
        ('PENDING', 'En attente d\'analyse'),
        ('ANALYZED', 'Analysé'),
        ('REPORTED', 'Rapport disponible'),
    ], default='UPLOADED')
    
    # Tracking
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_studies')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Étude {self.modality} pour {self.patient.full_name} le {self.study_date}"
    
    class Meta:
        verbose_name = 'Étude DICOM'
        verbose_name_plural = 'Études DICOM'
        ordering = ['-study_date', '-study_time']

class DicomSeries(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    study = models.ForeignKey(DicomStudy, on_delete=models.CASCADE, related_name='series')
    
    # DICOM metadata
    series_instance_uid = models.CharField(max_length=100, unique=True)
    series_number = models.IntegerField()
    series_description = models.CharField(max_length=200, blank=True, null=True)
    body_part = models.CharField(max_length=100, blank=True, null=True)
    
    # Orthanc metadata
    orthanc_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Série {self.series_number} - {self.series_description or 'Sans description'}"
    
    class Meta:
        verbose_name = 'Série DICOM'
        verbose_name_plural = 'Séries DICOM'
        ordering = ['series_number']

class DicomInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    series = models.ForeignKey(DicomSeries, on_delete=models.CASCADE, related_name='instances')
    
    # DICOM metadata
    sop_instance_uid = models.CharField(max_length=100, unique=True)
    instance_number = models.IntegerField()
    
    # File
    file = models.FileField(upload_to=dicom_file_path, blank=True, null=True)
    
    # Orthanc metadata
    orthanc_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Instance {self.instance_number}"
    
    class Meta:
        verbose_name = 'Instance DICOM'
        verbose_name_plural = 'Instances DICOM'
        ordering = ['instance_number']

class RadiologyReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    study = models.OneToOneField(DicomStudy, on_delete=models.CASCADE, related_name='report')
    
    # Report details
    radiologist = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='radiology_reports')
    findings = models.TextField()
    impression = models.TextField()
    recommendations = models.TextField(blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('DRAFT', 'Brouillon'),
        ('PRELIMINARY', 'Préliminaire'),
        ('FINAL', 'Final'),
        ('AMENDED', 'Modifié'),
    ], default='DRAFT')
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    finalized_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Rapport pour {self.study}"
    
    class Meta:
        verbose_name = 'Rapport de radiologie'
        verbose_name_plural = 'Rapports de radiologie'
        ordering = ['-created_at']