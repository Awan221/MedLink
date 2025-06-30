from django.apps import AppConfig


class BloodbankConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bloodbank'
    verbose_name = 'Banque de Sang'
    
    def ready(self):
        # Importer les signaux ici pour éviter les imports circulaires
        import bloodbank.signals  # noqa
