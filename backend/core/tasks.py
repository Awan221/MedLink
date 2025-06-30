from celery import shared_task
import os
import sys
import logging

# Configurer le logger
logger = logging.getLogger(__name__)

@shared_task
def synchronize_orthanc():
    """Tâche Celery pour synchroniser les études DICOM depuis Orthanc."""
    try:
        # Ajouter le répertoire du projet au chemin Python
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Importer le script de synchronisation
        from scripts.orthanc_integration import synchronize_studies
        
        # Exécuter la synchronisation
        logger.info("Début de la synchronisation Orthanc...")
        synchronize_studies()
        logger.info("Synchronisation Orthanc terminée avec succès.")
        
        return True
    except Exception as e:
        logger.error(f"Erreur lors de la synchronisation Orthanc: {str(e)}")
        return False