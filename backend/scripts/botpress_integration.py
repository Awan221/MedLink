#!/usr/bin/env python
import os
import sys
import json
import requests
from datetime import datetime

# Ajouter le répertoire du projet au chemin Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurer l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

from django.conf import settings
from chatbot.models import ChatbotKnowledgeBase

def export_knowledge_to_botpress():
    """Exporter la base de connaissances vers Botpress."""
    # URL de l'API Botpress
    botpress_url = settings.BOTPRESS_URL
    bot_id = settings.BOTPRESS_BOT_ID
    
    # Récupérer toutes les entrées de la base de connaissances
    knowledge_entries = ChatbotKnowledgeBase.objects.all()
    
    if not knowledge_entries:
        print("Aucune entrée dans la base de connaissances.")
        return
    
    # Préparer les données pour Botpress
    qna_data = []
    
    for entry in knowledge_entries:
        # Extraire les mots-clés
        keywords = entry.keywords.split(',') if entry.keywords else []
        
        # Créer une entrée QnA pour Botpress
        qna_item = {
            "id": f"kb-{entry.id}",
            "data": {
                "action": "text",
                "contexts": [entry.category.lower()],
                "enabled": True,
                "answers": {
                    "fr": [entry.content]
                },
                "questions": {
                    "fr": [entry.title] + keywords
                },
                "redirectFlow": "",
                "redirectNode": ""
            }
        }
        
        qna_data.append(qna_item)
    
    # Chemin du fichier d'exportation
    export_dir = os.path.join(settings.MEDIA_ROOT, 'botpress_exports')
    os.makedirs(export_dir, exist_ok=True)
    
    export_file = os.path.join(export_dir, f"qna_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    # Sauvegarder les données au format JSON
    with open(export_file, 'w', encoding='utf-8') as f:
        json.dump(qna_data, f, ensure_ascii=False, indent=2)
    
    print(f"Base de connaissances exportée vers {export_file}")
    
    # Importer les données dans Botpress via l'API
    try:
        # Vérifier si l'API Botpress est accessible
        response = requests.get(f"{botpress_url}/api/v1/admin/bots")
        
        if response.status_code == 200:
            # Importer les données QnA
            import_url = f"{botpress_url}/api/v1/bots/{bot_id}/qna/import"
            
            with open(export_file, 'r', encoding='utf-8') as f:
                files = {'file': f}
                response = requests.post(import_url, files=files)
                
                if response.status_code == 200:
                    print("Base de connaissances importée avec succès dans Botpress.")
                else:
                    print(f"Erreur lors de l'importation dans Botpress: {response.text}")
        else:
            print(f"Impossible de se connecter à l'API Botpress: {response.text}")
    except Exception as e:
        print(f"Erreur lors de la communication avec Botpress: {str(e)}")

if __name__ == "__main__":
    export_knowledge_to_botpress()