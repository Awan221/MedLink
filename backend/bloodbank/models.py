from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.gis.db import models as gis_models

class BloodDonationCenter(models.Model):
    name = models.CharField('Nom du centre', max_length=255)
    address = models.TextField('Adresse')
    city = models.CharField('Ville', max_length=100)
    region = models.CharField('Région', max_length=100)
    country = models.CharField('Pays', max_length=100, default='Sénégal')
    phone = models.CharField('Téléphone', max_length=20)
    email = models.EmailField('Email', blank=True, null=True)
    location = gis_models.PointField('Localisation', geography=True, null=True, blank=True)
    is_active = models.BooleanField('Actif', default=True)
    created_at = models.DateTimeField('Date de création', auto_now_add=True)
    updated_at = models.DateTimeField('Dernière mise à jour', auto_now=True)

    class Meta:
        verbose_name = 'Centre de don de sang'
        verbose_name_plural = 'Centres de don de sang'
        ordering = ['name', 'city']

    def __str__(self):
        return f"{self.name} - {self.city}"
        
    def save(self, *args, **kwargs):
        # Mettre à jour les coordonnées si elles sont fournies
        if not self.location and hasattr(self, 'latitude') and hasattr(self, 'longitude') and self.latitude and self.longitude:
            from django.contrib.gis.geos import Point
            self.location = Point(float(self.longitude), float(self.latitude))
        super().save(*args, **kwargs)
        
    @property
    def latitude(self):
        return self.location.y if self.location else None
        
    @property
    def longitude(self):
        return self.location.x if self.location else None

class BloodInventory(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    
    center = models.ForeignKey(BloodDonationCenter, on_delete=models.CASCADE, related_name='inventory')
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    quantity_ml = models.PositiveIntegerField(default=0)
    minimum_required_ml = models.PositiveIntegerField(default=1000)  # 1L par défaut
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Blood Inventories'
        unique_together = ('center', 'blood_type')
    
    def __str__(self):
        return f"{self.blood_type} - {self.center.name}"
    
    @property
    def status(self):
        if self.quantity_ml == 0:
            return 'critical'
        elif self.quantity_ml < (self.minimum_required_ml * 0.3):
            return 'low'
        elif self.quantity_ml < self.minimum_required_ml:
            return 'warning'
        return 'good'

class BloodDonation(models.Model):
    donor_name = models.CharField(max_length=255)
    donor_blood_type = models.CharField(max_length=3, choices=BloodInventory.BLOOD_TYPES)
    donor_phone = models.CharField(max_length=20, blank=True, null=True)
    donation_center = models.ForeignKey(BloodDonationCenter, on_delete=models.SET_NULL, null=True, related_name='donations')
    donation_date = models.DateTimeField(default=timezone.now)
    quantity_ml = models.PositiveIntegerField()
    is_processed = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_processed and not self._state.adding:
            self._update_inventory()
    
    def _update_inventory(self):
        if not self.is_processed or not self.donation_center:
            return
            
        inventory, created = BloodInventory.objects.get_or_create(
            center=self.donation_center,
            blood_type=self.donor_blood_type,
            defaults={'quantity_ml': self.quantity_ml}
        )
        
        if not created:
            inventory.quantity_ml += self.quantity_ml
            inventory.save()
    
    def __str__(self):
        return f"Don de {self.quantity_ml}ml ({self.donor_blood_type}) - {self.donor_name}"
