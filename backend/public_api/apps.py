from django.apps import AppConfig

class PublicApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'public_api'
    verbose_name = 'API Publique'
    
    def ready(self):
        # Importer les signaux si nécessaire
        pass
