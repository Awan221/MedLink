from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import logging

logger = logging.getLogger(__name__)

class OrthancProxyView(APIView):
    """
    Vue proxy pour rediriger les requêtes vers le serveur Orthanc sans authentification
    """
    
    def get_base_url(self):
        """Construit l'URL de base du serveur Orthanc"""
        return 'http://localhost:8042'  # URL directe sans authentification
    
    def forward_request(self, method, path, request):
        """
        Transmet la requête au serveur Orthanc
        """
        url = f"{self.get_base_url()}/{path.lstrip('/')}"
        
        # Préparer les en-têtes
        headers = {}
        if 'HTTP_CONTENT_TYPE' in request.META:
            headers['Content-Type'] = request.META['HTTP_CONTENT_TYPE']
        
        # Préparer les paramètres de requête
        params = request.query_params.dict()
        
        # Préparer les données de la requête
        data = request.body if request.body else None
        
        try:
            # Faire la requête à Orthanc sans authentification
            response = requests.request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=headers,
                stream=True,
                timeout=30
            )
            
            # Construire la réponse avec le contenu et les en-têtes d'Orthanc
            response_headers = dict(response.headers)
            
            # Liste des en-têtes à supprimer (y compris les en-têtes hop-by-hop)
            headers_to_remove = [
                'Content-Length', 'Content-Encoding', 'Transfer-Encoding',
                'Connection', 'Keep-Alive', 'Proxy-Authenticate',
                'Proxy-Authorization', 'TE', 'Trailers', 'Upgrade'
            ]
            
            # Supprimer les en-têtes problématiques
            for header in headers_to_remove:
                response_headers.pop(header, None)
            
            # Créer la réponse avec les en-têtes nettoyés
            return Response(
                response.content,
                status=response.status_code,
                content_type=response.headers.get('Content-Type'),
                headers=response_headers
            )
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur lors de la requête vers Orthanc: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
    
    def get(self, request, path=''):
        return self.forward_request('GET', path, request)
    
    def post(self, request, path=''):
        return self.forward_request('POST', path, request)
    
    def put(self, request, path=''):
        return self.forward_request('PUT', path, request)
    
    def delete(self, request, path=''):
        return self.forward_request('DELETE', path, request)
