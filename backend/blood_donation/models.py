from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BloodCenter(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    stock_level = models.IntegerField(default=100)  # Pourcentage
    is_critical = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'blood_donation'
        db_table = 'blood_donation_blood_center'
        ordering = ['-updated_at']

class BloodDonationAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    center = models.ForeignKey(BloodCenter, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_notification = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'center']
        ordering = ['-created_at']

    def __str__(self):
        return f"Alerte pour {self.user.email} - {self.center.name}" 