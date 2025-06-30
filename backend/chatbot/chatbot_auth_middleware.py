from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
import re

class ChatbotAuthMiddleware(MiddlewareMixin):
    """
    Middleware pour gérer l'authentification des endpoints du chatbot.
    Permet l'accès anonyme aux endpoints spécifiés.
    """
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__(get_response)

    def is_chatbot_request(self, request):
        """Vérifie si la requête est destinée au chatbot et ne nécessite pas d'authentification."""
        # Liste des chemins qui ne nécessitent pas d'authentification
        chatbot_paths = [
            r'^/api/chatbot/request/?$',
            r'^/api/chatbot/session/?$',
            r'^/api/chatbot/feedback/?$',
            r'^/api/chatbot/sessions/[^/]+/?$',  # Pour les requêtes sur des sessions spécifiques
        ]
        
        # Vérifier si le chemin correspond à un des patterns
        path = request.path
        return any(re.match(pattern, path) for pattern in chatbot_paths)
        
    def process_request(self, request):
        # Vérifier si c'est une requête pour le chatbot
        is_chatbot_path = self.is_chatbot_request(request)
        
        # Si c'est une requête OPTIONS, laisser passer sans authentification
        if request.method == 'OPTIONS':
            response = JsonResponse({}, status=200)
            self._add_cors_headers(request, response)
            return response
            
        # Pour les chemins du chatbot, définir l'utilisateur comme anonyme
        if is_chatbot_path:
            # Supprimer les en-têtes d'authentification de META
            auth_headers = [k for k in request.META if k.startswith('HTTP_AUTHORIZATION')]
            for header in auth_headers:
                del request.META[header]
            
            # Définir l'utilisateur comme anonyme et désactiver la vérification CSRF
            request.user = AnonymousUser()
            request._dont_enforce_csrf_checks = True
            return None
            
        # Pour les autres chemins, laisser Django gérer l'authentification
        return None

    def process_response(self, request, response):
        # Ajouter les en-têtes CORS uniquement pour les requêtes du chatbot
        if hasattr(request, 'user') and isinstance(request.user, AnonymousUser):
            self._add_cors_headers(request, response)
        return response

    def _add_cors_headers(self, request, response):
        """Ajoute les en-têtes CORS nécessaires à la réponse."""
        # Ne pas ajouter d'en-têtes CORS si la réponse est déjà définie
        if 'Access-Control-Allow-Origin' in response:
            return
            
        # Définir l'origine autorisée
        origin = request.headers.get('Origin', '*')
        response['Access-Control-Allow-Origin'] = origin
        
        # Définir les méthodes autorisées
        if 'Access-Control-Allow-Methods' not in response:
            response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
            
        # Définir les en-têtes autorisés
        if 'Access-Control-Allow-Headers' not in response:
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-CSRFToken, X-Requested-With'
            
        # Autoriser les credentials
        if 'Access-Control-Allow-Credentials' not in response:
            response['Access-Control-Allow-Credentials'] = 'true'
            
        # Définir la durée de mise en cache pour les pré-vérifications
        if 'Access-Control-Max-Age' not in response:
            response['Access-Control-Max-Age'] = '86400'  # 24 heures
