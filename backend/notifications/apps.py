from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'
    
    def ready(self):
        # Import des signaux ici pour éviter les problèmes de chargement
        import notifications.signals  # noqa
