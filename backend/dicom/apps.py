from django.apps import AppConfig

class DicomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dicom'
    verbose_name = 'Téléradiologie DICOM'
    
    def ready(self):
        # Importer les signaux ici pour éviter les imports circulaires
        import dicom.signals  # noqa
