import os
from celery import Celery

# Définir les variables d'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Créer l'instance Celery
app = Celery('core')

# Charger la configuration depuis les paramètres Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Découvrir automatiquement les tâches dans les applications Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')