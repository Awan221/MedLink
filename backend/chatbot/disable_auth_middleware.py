from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser

class DisableAuthForChatbotMiddleware(MiddlewareMixin):
    """
    Middleware qui désactive l'authentification pour les endpoints du chatbot.
    """
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__(get_response)

    def __call__(self, request):
        # Liste des chemins qui ne nécessitent pas d'authentification
        public_paths = [
            '/api/chatbot/request',
            '/api/chatbot/session',
            '/api/chatbot/feedback',
        ]

        # Vérifier si le chemin actuel est dans la liste des chemins publics
        if any(request.path.startswith(path) for path in public_paths):
            # Définir l'utilisateur comme anonyme
            request.user = AnonymousUser()
            
            # Gérer les requêtes OPTIONS pour CORS
            if request.method == 'OPTIONS':
                response = JsonResponse({}, status=200)
                self._add_cors_headers(request, response)
                return response
        
        response = self.get_response(request)
        
        # Ajouter les en-têtes CORS si c'est une requête vers le chatbot
        if any(request.path.startswith(path) for path in public_paths):
            self._add_cors_headers(request, response)
            
        return response

    def _add_cors_headers(self, request, response):
        """Ajoute les en-têtes CORS nécessaires à la réponse."""
        origin = request.headers.get('Origin', '*')
        response['Access-Control-Allow-Origin'] = origin
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-CSRFToken, X-Requested-With'
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Max-Age'] = '86400'  # 24 heures
