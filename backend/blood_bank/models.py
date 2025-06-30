from django.db import models
from django.utils import timezone
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from authentication.models import User

class BloodBankCenter(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    region = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    
    # Coordonnées géographiques (PostGIS)
    location = gis_models.PointField(geography=True, null=True, blank=True)
    
    # Horaires d'ouverture
    opening_hours = models.CharField(max_length=200, blank=True, null=True)
    
    # Responsable
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_blood_banks')
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.region}"
        
    class Meta:
        app_label = 'blood_bank'
        db_table = 'blood_bank_centers'
        verbose_name = 'Centre de transfusion sanguine'
        verbose_name_plural = 'Centres de transfusion sanguine'
        ordering = ['name']

class BloodStock(models.Model):
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
    
    center = models.ForeignKey(BloodBankCenter, on_delete=models.CASCADE, related_name='blood_stocks')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    units_available = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(default=timezone.now)
    
    # Utilisateur qui a mis à jour
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_blood_stocks')
    
    def __str__(self):
        return f"{self.blood_group} - {self.center.name} ({self.units_available} unités)"
    
    class Meta:
        verbose_name = 'Stock de Sang'
        verbose_name_plural = 'Stocks de Sang'
        ordering = ['center', 'blood_group']
        unique_together = ('center', 'blood_group')

class BloodDonation(models.Model):
    STATUS_CHOICES = (
        ('SCHEDULED', 'Programmé'),
        ('COMPLETED', 'Complété'),
        ('CANCELLED', 'Annulé'),
    )
    
    center = models.ForeignKey(BloodBankCenter, on_delete=models.CASCADE, related_name='blood_donations')
    donor_name = models.CharField(max_length=100)
    donor_email = models.EmailField(blank=True, null=True)
    donor_phone = models.CharField(max_length=20)
    blood_group = models.CharField(max_length=3, choices=BloodStock.BLOOD_GROUP_CHOICES)
    donation_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    
    # Suivi
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='completed_donations')
    
    def __str__(self):
        return f"Don de {self.donor_name} ({self.blood_group}) à {self.center.name}"
    
    class Meta:
        verbose_name = 'Don de Sang'
        verbose_name_plural = 'Dons de Sang'
        ordering = ['-donation_date']

class BloodRequest(models.Model):
    PRIORITY_CHOICES = (
        ('NORMAL', 'Normal'),
        ('URGENT', 'Urgent'),
        ('EMERGENCY', 'Urgence Vitale'),
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'En attente'),
        ('APPROVED', 'Approuvé'),
        ('FULFILLED', 'Satisfait'),
        ('CANCELLED', 'Annulé'),
    )
    
    center = models.ForeignKey(BloodBankCenter, on_delete=models.CASCADE, related_name='blood_requests')
    requesting_doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='blood_requests')
    blood_group = models.CharField(max_length=3, choices=BloodStock.BLOOD_GROUP_CHOICES)
    units_requested = models.PositiveIntegerField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='NORMAL')
    patient_name = models.CharField(max_length=100)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Suivi
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_blood_requests')
    fulfilled_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Demande de {self.units_requested} unités de {self.blood_group} pour {self.patient_name}"
    
    class Meta:
        verbose_name = 'Demande de Sang'
        verbose_name_plural = 'Demandes de Sang'
        ordering = ['-priority', '-created_at']