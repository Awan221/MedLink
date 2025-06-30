from django.db import models
from django.conf import settings
from patients.models import Patient

class DICOMStudy(models.Model):
    study_uid = models.CharField(max_length=128, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='dicom_module_studies')
    study_date = models.DateTimeField()
    study_description = models.TextField(blank=True, null=True)
    modality = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.study_description} - {self.patient.full_name}"

class DICOMSeries(models.Model):
    study = models.ForeignKey(DICOMStudy, on_delete=models.CASCADE, related_name='dicom_module_series')
    series_uid = models.CharField(max_length=128, unique=True)
    series_number = models.IntegerField()
    series_description = models.TextField(blank=True, null=True)
    modality = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.series_description or 'Série'} - {self.study.patient.full_name}"

class DICOMInstance(models.Model):
    series = models.ForeignKey(DICOMSeries, on_delete=models.CASCADE, related_name='dicom_module_instances')
    sop_instance_uid = models.CharField(max_length=128, unique=True)
    instance_number = models.IntegerField()
    file_path = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Instance {self.instance_number} - {self.series}"
