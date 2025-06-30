from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
import json

class AllowOptionsMiddleware(MiddlewareMixin):
    """
    Middleware pour gérer les requêtes OPTIONS et permettre l'accès anonyme
    aux endpoints du chatbot.
    """
    def process_request(self, request):
        # Autoriser les requêtes OPTIONS sans authentification
        if request.method == 'OPTIONS':
            response = JsonResponse({}, status=200)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-CSRFToken'
            response['Access-Control-Allow-Credentials'] = 'true'
            return response
        return None

    def process_response(self, request, response):
        # Ajouter les en-têtes CORS nécessaires à toutes les réponses
        response['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-CSRFToken'
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
