from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.contrib.auth.models import AnonymousUser

class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware personnalisé pour gérer l'authentification JWT.
    Permet l'accès anonyme aux endpoints du chatbot.
    """
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__(get_response)
        self.auth = JWTAuthentication()

    def __call__(self, request):
        # Liste des chemins qui ne nécessitent pas d'authentification
        public_paths = [
            '/api/chatbot/request',
            '/api/chatbot/session',
            '/api/chatbot/feedback',
        ]

        # Vérifier si le chemin actuel est dans la liste des chemins publics
        is_public_path = any(request.path.startswith(path) for path in public_paths)
        
        # Si c'est une requête OPTIONS, laisser passer sans authentification
        if request.method == 'OPTIONS':
            response = JsonResponse({}, status=200)
            self._add_cors_headers(request, response)
            return response
        
        # Pour les chemins publics, essayer d'authentifier si un token est fourni
        if is_public_path:
            # Vérifier si un token est présent dans l'en-tête
            auth_header = request.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                try:
                    # Essayer d'authentifier avec le token fourni
                    auth_result = self.auth.authenticate(request)
                    if auth_result is not None:
                        request.user, request.auth = auth_result
                except (InvalidToken, AuthenticationFailed):
                    # Si le token est invalide, continuer en tant qu'utilisateur anonyme
                    request.user = AnonymousUser()
                    request.auth = None
            else:
                # Aucun token fourni, continuer en tant qu'utilisateur anonyme
                request.user = AnonymousUser()
                request.auth = None
                
            response = self.get_response(request)
            self._add_cors_headers(request, response)
            return response
        
        # Pour les autres chemins, utiliser l'authentification JWT normale
        try:
            auth_result = self.auth.authenticate(request)
            if auth_result is not None:
                request.user, request.auth = auth_result
                response = self.get_response(request)
                self._add_cors_headers(request, response)
                return response
            else:
                return JsonResponse(
                    {'error': 'Informations d\'authentification non fournies'}, 
                    status=401
                )
        except (InvalidToken, AuthenticationFailed) as e:
            return JsonResponse(
                {'error': 'Token d\'authentification invalide ou expiré'}, 
                status=401
            )

    def _add_cors_headers(self, request, response):
        """Ajoute les en-têtes CORS nécessaires à la réponse."""
        origin = request.headers.get('Origin', '*')
        response['Access-Control-Allow-Origin'] = origin
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-CSRFToken, X-Requested-With'
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Max-Age'] = '86400'  # 24 heures
