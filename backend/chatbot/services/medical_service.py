"""
Service de validation et d'enrichissement des réponses médicales.
"""
import re
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class MedicalService:
    """Service de validation et d'enrichissement des réponses médicales."""
    
    # Mots-clés pour la détection d'urgence
    EMERGENCY_KEYWORDS = [
        'urgence', 'urgent', 'immédiat', 'immédiatement', 'appelez le 15', 
        'SAMU', 'composez le 15', 'service d\'urgence', 'allez aux urgences'
    ]
    
    # Avertissements standard
    DISCLAIMERS = {
        'general': (
            "⚠️ <strong>Information importante :</strong> Cette réponse est générée par une IA et ne remplace pas "
            "l'avis d'un professionnel de santé. En cas d'urgence, composez le 15 ou le 112."
        ),
        'symptoms': (
            "🔍 <strong>Conseil :</strong> Si vos symptômes persistent ou s'aggravent, "
            "veuillez consulter un professionnel de santé."
        ),
        'medication': (
            "💊 <strong>Important :</strong> Ne modifiez pas votre traitement sans l'avis d'un professionnel de santé."
        )
    }
    
    async def validate_response(self, query: str, response: str) -> Dict:
        """Valide une réponse médicale et ajoute des avertissements si nécessaire."""
        validation = {
            'requires_urgent_attention': self._check_emergency(response),
            'disclaimers': self._get_relevant_disclaimers(query, response),
            'sources': self._extract_sources(response)
        }
        return validation
    
    def _check_emergency(self, text: str) -> bool:
        """Vérifie si le texte contient des indicateurs d'urgence."""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.EMERGENCY_KEYWORDS)
    
    def _get_relevant_disclaimers(self, query: str, response: str) -> List[str]:
        """Retourne les avertissements pertinents en fonction de la requête et de la réponse."""
        disclaimers = [self.DISCLAIMERS['general']]
        
        # Vérifier les symptômes dans la requête
        symptom_keywords = ['mal', 'douleur', 'symptôme', 'fièvre', 'nausée', 'fatigue']
        if any(keyword in query.lower() for keyword in symptom_keywords):
            disclaimers.append(self.DISCLAIMERS['symptoms'])
        
        # Vérifier les médicaments dans la réponse
        if any(word in response.lower() for word in ['médicament', 'prendre', 'dose', 'traitement']):
            disclaimers.append(self.DISCLAIMERS['medication'])
            
        return disclaimers
    
    def _extract_sources(self, text: str) -> List[Dict]:
        """Extrait les sources mentionnées dans le texte."""
        # Cette version simplifiée retourne des sources génériques
        # Dans une version complète, cela pourrait faire une recherche dans une base de données
        return [
            {
                'name': 'Ministère de la Santé',
                'url': 'https://solidarites-sante.gouv.fr/'
            },
            {
                'name': 'HAS - Haute Autorité de Santé',
                'url': 'https://www.has-sante.fr/'
            }
        ]

# Singleton instance
_medical_service = None

def get_medical_service():
    """Retourne une instance singleton du service médical."""
    global _medical_service
    if _medical_service is None:
        _medical_service = MedicalService()
    return _medical_service
