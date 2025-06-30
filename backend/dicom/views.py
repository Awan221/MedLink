from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.conf import settings
from django.http import JsonResponse
import requests
import json
from .models import DICOMStudy, DICOMSeries, DICOMInstance
from .serializers import DICOMStudySerializer, DICOMSeriesSerializer, DICOMInstanceSerializer
from authentication.permissions import IsMedecin, IsRadiologue


class OHIFViewerAPIView(APIView):
    """
    API View pour intégrer le visualiseur OHIF avec Orthanc.
    Fournit les configurations nécessaires pour initialiser le visualiseur OHIF.
    """
    permission_classes = [permissions.IsAuthenticated & (IsMedecin | IsRadiologue)]
    
    def get(self, request, *args, **kwargs):
        # Configuration de base pour OHIF Viewer
        config = {
            'routerBasename': 'dicomViewer',
            'showStudyList': True,
            'servers': {
                'dicomWeb': [
                    {
                        'name': 'Orthanc',
                        'wadoUriRoot': f"{settings.ORTHANC_URL}/wado",
                        'wadoRoot': f"{settings.ORTHANC_URL}/dicom-web",
                        'qidoRoot': f"{settings.ORTHANC_URL}/dicom-web",
                        'wadoRoot': f"{settings.ORTHANC_URL}/dicom-web",
                        'qidoSupportsIncludeField': False,
                        'imageRendering': 'wadouri',
                        'thumbnailRendering': 'wadouri',
                        'requestOptions': {
                            'auth': (settings.ORTHANC_USERNAME, settings.ORTHANC_PASSWORD) if hasattr(settings, 'ORTHANC_USERNAME') else None,
                        },
                    },
                ],
            },
            'defaultViewport': {
                'colormap': 'Grayscale',
                'invert': False,
                'pixelReplication': False,
                'rotation': 0,
                'scale': 1,
                'hflip': False,
                'vflip': False,
            },
            'hotkeys': [
                {
                    'commandName': 'incrementActiveViewport',
                    'keys': ['right'],
                    'label': 'Next Viewport',
                },
                {
                    'commandName': 'decrementActiveViewport',
                    'keys': ['left'],
                    'label': 'Previous Viewport',
                },
            ],
        }
        
        return JsonResponse(config)

class DICOMStudyViewSet(viewsets.ModelViewSet):
    serializer_class = DICOMStudySerializer
    permission_classes = [permissions.IsAuthenticated & (IsMedecin | IsRadiologue)]
    
    def get_queryset(self):
        queryset = DICOMStudy.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset
    
    @action(detail=True, methods=['get'])
    def series(self, request, pk=None):
        study = self.get_object()
        series = study.series.all()
        serializer = DICOMSeriesSerializer(series, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def search_pacs(self, request):
        """Recherche des études dans le PACS Orthanc"""
        try:
            # Configuration de la connexion à Orthanc
            orthanc_url = getattr(settings, 'ORTHANC_URL', 'http://orthanc:8042')
            orthanc_user = getattr(settings, 'ORTHANC_USER', 'orthanc')
            orthanc_password = getattr(settings, 'ORTHANC_PASSWORD', 'orthanc')
            
            # Recherche des études correspondant aux critères
            search_data = request.data
            if not search_data:
                search_data = {}
            
            # Ajout de filtres par défaut si nécessaire
            if 'PatientID' not in search_data and 'PatientName' not in search_data:
                return Response(
                    {"error": "Au moins un critère de recherche est requis (PatientID ou PatientName)"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Appel à l'API Orthanc
            response = requests.post(
                f"{orthanc_url}/tools/find",
                auth=(orthanc_user, orthanc_password),
                json={"Level": "Study", "Query": search_data},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                return Response(
                    {"error": f"Erreur lors de la recherche dans Orthanc: {response.text}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            studies = response.json()
            return Response({"studies": studies})
            
        except Exception as e:
            return Response(
                {"error": f"Erreur lors de la recherche PACS: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DICOMSeriesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DICOMSeriesSerializer
    permission_classes = [permissions.IsAuthenticated & (IsMedecin | IsRadiologue)]
    
    def get_queryset(self):
        queryset = DICOMSeries.objects.all()
        study_id = self.request.query_params.get('study_id')
        if study_id:
            queryset = queryset.filter(study_id=study_id)
        return queryset
    
    @action(detail=True, methods=['get'])
    def instances(self, request, pk=None):
        series = self.get_object()
        instances = series.instances.all()
        serializer = DICOMInstanceSerializer(instances, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def view_series(self, request, pk=None):
        """Renvoie l'URL pour visualiser la série dans un visualiseur DICOM"""
        series = self.get_object()
        viewer_url = f"/dicom-viewer/?series={series.series_uid}"
        return Response({"viewer_url": viewer_url})

class DICOMInstanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DICOMInstanceSerializer
    permission_classes = [permissions.IsAuthenticated & (IsMedecin | IsRadiologue)]
    
    def get_queryset(self):
        queryset = DICOMInstance.objects.all()
        series_id = self.request.query_params.get('series_id')
        if series_id:
            queryset = queryset.filter(series_id=series_id)
        return queryset
    
    @action(detail=True, methods=['get'])
    def view_instance(self, request, pk=None):
        """Renvoie l'URL pour visualiser une instance spécifique"""
        instance = self.get_object()
        viewer_url = f"/dicom-viewer/?instance={instance.sop_instance_uid}"
        return Response({"viewer_url": viewer_url})
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Télécharge l'instance DICOM"""
        instance = self.get_object()
        # Ici, vous devrez implémenter la logique pour servir le fichier DICOM
        # Cette implémentation dépend de la façon dont vous stockez les fichiers
        return Response({"detail": "Téléchargement non implémenté"})
