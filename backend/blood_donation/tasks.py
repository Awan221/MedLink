from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import BloodCenter, BloodDonationAlert

@shared_task
def check_blood_stock_levels():
    """
    Vérifie les niveaux de stock de tous les centres de don
    et envoie des notifications si nécessaire
    """
    # Seuil critique pour le niveau de stock (en pourcentage)
    CRITICAL_THRESHOLD = 20
    
    # Récupérer tous les centres avec un niveau de stock critique
    critical_centers = BloodCenter.objects.filter(
        stock_level__lte=CRITICAL_THRESHOLD,
        is_critical=False
    )
    
    for center in critical_centers:
        # Marquer le centre comme critique
        center.is_critical = True
        center.save()
        
        # Envoyer des notifications aux utilisateurs abonnés
        send_critical_stock_notifications(center)
    
    # Réinitialiser le statut critique pour les centres qui ne sont plus en situation critique
    BloodCenter.objects.filter(
        stock_level__gt=CRITICAL_THRESHOLD,
        is_critical=True
    ).update(is_critical=False)

def send_critical_stock_notifications(center):
    """
    Envoie des notifications aux utilisateurs abonnés à un centre
    """
    # Récupérer les alertes actives pour ce centre
    alerts = BloodDonationAlert.objects.filter(
        center=center,
        is_active=True
    ).select_related('user')
    
    # Filtrer les alertes qui n'ont pas reçu de notification récemment
    recent_alerts = alerts.filter(
        last_notification__isnull=True
    ) | alerts.filter(
        last_notification__lt=timezone.now() - timedelta(days=1)
    )
    
    for alert in recent_alerts:
        # Envoyer l'email
        send_mail(
            subject=f'Urgent : Niveau de stock critique à {center.name}',
            message=f'''
            Bonjour,
            
            Le centre de don de sang {center.name} a atteint un niveau de stock critique ({center.stock_level}%).
            Votre don est plus que jamais nécessaire.
            
            Adresse : {center.address}
            Téléphone : {center.phone}
            
            Merci de votre générosité.
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[alert.user.email],
            fail_silently=True
        )
        
        # Mettre à jour la date de dernière notification
        alert.last_notification = timezone.now()
        alert.save() 