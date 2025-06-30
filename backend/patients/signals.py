from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from .models import MedicalRecord, MedicalRecordHistory, Prescription, PrescriptionHistory, Patient, PatientHistory
from django.conf import settings

@receiver(post_save, sender=Patient)
def log_patient_save(sender, instance, created, **kwargs):
    user = getattr(instance, '_action_user', None)
    action = 'create' if created else 'update'
    PatientHistory.objects.create(
        patient=instance,
        action=action,
        performed_by=user,
        snapshot=model_to_dict(instance)
    )

@receiver(post_save, sender=MedicalRecord)
def log_medical_record_save(sender, instance, created, **kwargs):
    # On veut ignorer les updates automatiques (ex: updated_at)
    user = getattr(instance, '_action_user', None)
    action = 'create' if created else 'update'
    MedicalRecordHistory.objects.create(
        medical_record=instance,
        action=action,
        performed_by=user,
        snapshot=model_to_dict(instance)
    )

@receiver(post_delete, sender=Patient)
def log_patient_delete(sender, instance, **kwargs):
    user = getattr(instance, '_action_user', None)
    PatientHistory.objects.create(
        patient=instance,
        action='delete',
        performed_by=user,
        snapshot=model_to_dict(instance)
    )

@receiver(post_delete, sender=MedicalRecord)
def log_medical_record_delete(sender, instance, **kwargs):
    user = getattr(instance, '_action_user', None)
    MedicalRecordHistory.objects.create(
        medical_record=instance,
        action='delete',
        performed_by=user,
        snapshot=model_to_dict(instance)
    )

@receiver(post_save, sender=Prescription)
def log_prescription_save(sender, instance, created, **kwargs):
    user = getattr(instance, '_action_user', None)
    action = 'create' if created else 'update'
    PrescriptionHistory.objects.create(
        prescription=instance,
        action=action,
        performed_by=user,
        snapshot=model_to_dict(instance)
    )

@receiver(post_delete, sender=Prescription)
def log_prescription_delete(sender, instance, **kwargs):
    user = getattr(instance, '_action_user', None)
    PrescriptionHistory.objects.create(
        prescription=instance,
        action='delete',
        performed_by=user,
        snapshot=model_to_dict(instance)
    )
