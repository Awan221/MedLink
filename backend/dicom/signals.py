"""
Signaux pour l'application DICOM.
Ce fichier contient les signaux qui permettent de déclencher des actions
lors d'événements spécifiques liés aux modèles DICOM.
"""
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Exemple de signal (à adapter selon vos besoins)
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#         logger.info(f"Profil utilisateur créé pour {instance.username}")

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()
#     logger.debug(f"Profil utilisateur sauvegardé pour {instance.username}")
