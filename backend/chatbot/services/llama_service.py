import os
import json
import requests
import logging
from django.conf import settings
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class LlamaService:
    """
    Service pour interagir avec le modèle Llama 3.3 70B Instruct via OpenRouter
    """
    
    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.CHATBOT_MODEL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://medlink.com",
            "Content-Type": "application/json"
        }
        logger.info(f"Initialisation de LlamaService avec le modèle: {self.model}")
    
    def get_chat_response(
        self, 
        messages: List[Dict[str, str]],
        user_role: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Envoie une requête au modèle Llama et retourne la réponse
        
        Args:
            messages: Liste des messages de la conversation
            user_role: Rôle de l'utilisateur (patient, medecin, etc.)
            temperature: Créativité des réponses (0-1), utilise la valeur par défaut si None
            max_tokens: Nombre maximum de tokens dans la réponse, utilise la valeur par défaut si None
            
        Returns:
            Dictionnaire contenant la réponse du modèle
        """
        # Utiliser les valeurs par défaut du settings si non spécifiées
        if temperature is None:
            temperature = settings.CHATBOT_TEMPERATURE
        if max_tokens is None:
            max_tokens = settings.CHATBOT_MAX_TOKENS
            
        logger.debug(f"Envoi d'une requête au modèle {self.model} avec {len(messages)} messages")
        
        # Personnalisation du contexte en fonction du rôle
        system_prompt = self._get_system_prompt(user_role)
        
        # Préparation des messages avec le prompt système
        chat_messages = [{"role": "system", "content": system_prompt}]
        chat_messages.extend(messages)
        
        payload = {
            "model": self.model,
            "messages": chat_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        try:
            response = requests.post(
                self.BASE_URL,
                headers=self.headers,
                json=payload,
                timeout=30  # Timeout de 30 secondes
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Erreur lors de la requête à l'API OpenRouter: {str(e)}"
            if hasattr(e, 'response') and e.response:
                error_msg += f" - {e.response.text}"
            raise Exception(error_msg)
    
    def _get_system_prompt(self, user_role: Optional[str] = None, session_type: Optional[str] = None) -> str:
        """
        Retourne le prompt système en fonction du rôle de l'utilisateur et du type de session
        
        Args:
            user_role: Rôle de l'utilisateur (ex: 'medecin', 'infirmier', 'patient', etc.)
            session_type: Type de session ('GENERAL', 'MEDICAL', 'TECHNICAL', 'ADMIN')
            
        Returns:
            str: Le prompt système formaté
        """
        # Définir le rôle par défaut si non spécifié
        user_role = user_role or 'utilisateur'
        
        # Définir le type de session par défaut si non spécifié
        session_type = session_type or 'GENERAL'
        
        # Mapper les types de session à des descriptions plus lisibles
        session_type_names = {
            'GENERAL': 'général',
            'MEDICAL': 'médical',
            'TECHNICAL': 'technique',
            'ADMIN': 'administratif'
        }
        session_name = session_type_names.get(session_type, 'général')
        
        # Base du prompt commun à tous les rôles et types de session
        base_prompt = f"""
        Tu es MedLink, un assistant médical professionnel. 
        Tu fournis des informations médicales précises et fiables.
        Type de session actuelle : {session_name.upper()}.
        
        Règles importantes à TOUJOURS suivre :
        1. Ne pose JAMAIS de diagnostic médical définitif
        2. Ne remplace PAS une consultation médicale en personne
        3. Sois bienveillant, clair et rassurant
        4. Demande des précisions si nécessaire
        5. Sois précis dans tes explications
        6. Utilise un langage adapté à ton interlocuteur
        """
        
        # Personnalisation en fonction du type de session
        session_specific = ""
        if session_type == 'MEDICAL':
            session_specific = """
            Tu es dans une session MÉDICALE. 
            Concentre-toi sur les aspects cliniques, les symptômes, les traitements.
            Sois particulièrement attentif aux signes d'urgence médicale.
            """
        elif session_type == 'TECHNICAL':
            session_specific = """
            Tu es dans une session TECHNIQUE.
            Tu peux entrer dans les détails techniques, les protocoles, les procédures.
            Utilise la terminologie appropriée tout en restant clair.
            """
        elif session_type == 'ADMIN':
            session_specific = """
            Tu es dans une session ADMINISTRATIVE.
            Concentre-toi sur les aspects administratifs, les rendez-vous, les documents.
            Sois précis dans les informations procédurales.
            """
        
        # Personnalisation en fonction du rôle utilisateur
        role_specific = ""
        if user_role.lower() in ['medecin', 'docteur', 'médecin', 'dr']:
            role_specific = """
            Tu t'adresses à un professionnel de santé.
            Tu peux utiliser un vocabulaire médical technique et précis.
            N'hésite pas à entrer dans les détails cliniques si nécessaire.
            """
        elif user_role.lower() in ['infirmier', 'infirmière', 'aide-soignant', 'aide soignant']:
            role_specific = """
            Tu t'adresses à un membre du personnel soignant.
            Utilise un langage technique mais adapté aux soins infirmiers.
            Mets l'accent sur les aspects pratiques des soins.
            """
        elif user_role.lower() in ['patient', 'usager']:
            role_specific = """
            Tu t'adresses à un patient.
            Utilise un langage simple et évite le jargon médical inutile.
            Si tu dois utiliser des termes techniques, explique-les clairement.
            Sois particulièrement attentif à rassurer et à expliquer clairement.
            """
        else:
            role_specific = """
            Tu t'adresses à un utilisateur dont le rôle n'est pas spécifié.
            Sois particulièrement prudent dans tes réponses.
            Évite tout conseil médical direct et encourage la consultation d'un professionnel.
            """
        
        # Instructions finales
        closing = """
        
        Rappel important :
        - Si la question sort de ton domaine d'expertise, signale-le clairement
        - En cas de doute sur une information, précise que tu n'es pas certain
        - Ne donne jamais l'impression de pouvoir remplacer un avis médical professionnel
        - Sois bienveillant et empathique en toutes circonstances
        """
        
        # Combiner toutes les parties du prompt
        full_prompt = base_prompt + "\n" + session_specific + "\n" + role_specific + "\n" + closing
        
        # Nettoyer le prompt (supprimer les lignes vides en trop)
        full_prompt = "\n".join([line for line in full_prompt.split("\n") if line.strip() != ""])
        
        logger.debug(f"Prompt système généré - Rôle: {user_role}, Type: {session_type}")
        return full_prompt
    
    def format_chat_history(self, messages: List[Dict]) -> List[Dict]:
        """Formate l'historique des messages pour l'API"""
        formatted = []
        for msg in messages:
            role = "user" if msg["type"] == "USER" else "assistant"
            formatted.append({"role": role, "content": msg["content"]})
        return formatted
