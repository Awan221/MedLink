from django.apps import AppConfig

class BloodDonationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blood_donation'
 
    def ready(self):
        import blood_donation.tasks  # noqa 