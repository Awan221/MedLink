from django.db import models
from django.utils import timezone
from authentication.models import User
import uuid

class Patient(models.Model):
    GENDER_CHOICES = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('A', 'Autre'),
    )
    
    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )
    
    # Identifiants uniques
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    national_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    medical_id = models.CharField(max_length=50, unique=True)
    
    # Informations personnelles
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    
    # Informations de contact
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    
    # Informations médicales
    allergies = models.TextField(blank=True, null=True)
    chronic_diseases = models.TextField(blank=True, null=True)
    current_medications = models.TextField(blank=True, null=True)
    
    # Suivi
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_patients')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.medical_id})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        today = timezone.now().date()
        born = self.date_of_birth
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    
    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ['last_name', 'first_name']

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='medical_records')
    date = models.DateTimeField(default=timezone.now)
    
    # Consultation
    reason = models.TextField()
    symptoms = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Vital signs
    temperature = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    blood_pressure = models.CharField(max_length=20, blank=True, null=True)
    heart_rate = models.IntegerField(blank=True, null=True)
    respiratory_rate = models.IntegerField(blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    # Suivi
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Consultation de {self.patient.full_name} le {self.date.strftime('%d/%m/%Y')}"
    
    class Meta:
        verbose_name = 'Dossier médical'
        verbose_name_plural = 'Dossiers médicaux'
        ordering = ['-date']

class PatientHistory(models.Model):
    ACTION_CHOICES = [
        ('create', 'Création'),
        ('update', 'Modification'),
        ('delete', 'Suppression'),
    ]
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    performed_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    performed_at = models.DateTimeField(auto_now_add=True)
    snapshot = models.JSONField()  # Etat du patient au moment de l'action

    def __str__(self):
        return f"{self.patient} - {self.action} - {self.performed_at}"


class MedicalRecordHistory(models.Model):
    ACTION_CHOICES = [
        ('create', 'Création'),
        ('update', 'Modification'),
        ('delete', 'Suppression'),
    ]
    medical_record = models.ForeignKey('MedicalRecord', on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    performed_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    performed_at = models.DateTimeField(auto_now_add=True)
    snapshot = models.JSONField()  # Etat du dossier médical au moment de l'action

    def __str__(self):
        return f"{self.medical_record} - {self.action} - {self.performed_at}"

class PrescriptionHistory(models.Model):
    ACTION_CHOICES = [
        ('create', 'Création'),
        ('update', 'Modification'),
        ('delete', 'Suppression'),
    ]
    prescription = models.ForeignKey('Prescription', on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    performed_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    performed_at = models.DateTimeField(auto_now_add=True)
    snapshot = models.JSONField()  # Etat de la prescription au moment de l'action

    def __str__(self):
        return f"{self.prescription} - {self.action} - {self.performed_at}"

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='prescriptions')
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    date = models.DateTimeField(default=timezone.now)
    
    medications = models.TextField()
    dosage = models.TextField()
    duration = models.CharField(max_length=100)
    instructions = models.TextField(blank=True, null=True)
    
    # Suivi
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Prescription pour {self.patient.full_name} du {self.date.strftime('%d/%m/%Y')}"
    
    class Meta:
        verbose_name = 'Prescription'
        verbose_name_plural = 'Prescriptions'
        ordering = ['-date']

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmé'),
        ('cancelled', 'Annulé'),
        ('completed', 'Terminé'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='appointments')
    scheduled_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_datetime']
        verbose_name = 'Rendez-vous'
        verbose_name_plural = 'Rendez-vous'

    def __str__(self):
        return f"{self.patient.full_name} avec {self.doctor} le {self.scheduled_datetime.strftime('%d/%m/%Y %H:%M')}"