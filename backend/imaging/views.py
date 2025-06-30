from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.http import FileResponse
import os
import requests
import json
import base64
from django.conf import settings

from .models import DicomStudy, DicomSeries, DicomInstance, RadiologyReport, ActionLog
from .serializers import (
    DicomStudySerializer, DicomSeriesSerializer, 
    DicomInstanceSerializer, RadiologyReportSerializer, ActionLogSerializer
)
from authentication.permissions import IsMedecin, IsRadiologue, IsTechnicien
from authentication.permissions import IsMedecin, IsRadiologue, IsTechnicien
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

class ActionLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActionLog.objects.select_related('user').all().order_by('-timestamp')
    serializer_class = ActionLogSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'action', 'status', 'target_type', 'target_id']
    search_fields = ['message']
    ordering_fields = ['timestamp', 'user', 'action', 'status']

class DicomStudyViewSet(viewsets.ModelViewSet):
    queryset = DicomStudy.objects.all()
    serializer_class = DicomStudySerializer
    permission_classes = [permissions.IsAuthenticated & (IsMedecin | IsRadiologue | IsTechnicien)]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['patient', 'status', 'modality']
    search_fields = ['study_description', 'patient__first_name', 'patient__last_name', 'patient__medical_id']
    ordering_fields = ['study_date', 'study_time', 'uploaded_at']
    
    def get_queryset(self):
        """
        Retourne les études DICOM filtrées selon les paramètres de requête.
        Les médecins voient toutes les études, les autres utilisateurs ne voient que celles qu'ils ont uploadées.
        """
        queryset = DicomStudy.objects.select_related('patient', 'uploaded_by')
        
        # Filtrage par défaut : pour les non-médecins, ne montrer que leurs propres uploads
        from authentication.permissions import IsMedecin
        is_doctor = IsMedecin().has_permission(self.request, self)
        if not is_doctor and not self.request.user.is_superuser:
            queryset = queryset.filter(uploaded_by=self.request.user)
            
        # Filtrage par patient si spécifié
        patient_id = self.request.query_params.get('patient')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
            
        # Filtrage par statut si spécifié
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        # Filtrage par modalité si spécifié
        modality = self.request.query_params.get('modality')
        if modality:
            queryset = queryset.filter(modality__iexact=modality)
            
        # Tri par défaut : du plus récent au plus ancien
        return queryset.order_by('-study_date', '-study_time', '-uploaded_at')
    
    @action(detail=False, methods=['get'], url_path='import-logs')
    def import_logs(self, request):
        from django.db.models import Q
        import datetime
        search = request.query_params.get('search', '').strip()
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        status = request.query_params.get('status')
        qs = self.get_queryset().select_related('patient', 'uploaded_by').prefetch_related('series__instances')
        if search:
            qs = qs.filter(
                Q(patient__first_name__icontains=search) |
                Q(patient__last_name__icontains=search) |
                Q(patient__medical_id__icontains=search) |
                Q(uploaded_by__first_name__icontains=search) |
                Q(uploaded_by__last_name__icontains=search) |
                Q(series__instances__file__icontains=search)
            ).distinct()
        if date_from:
            try:
                qs = qs.filter(uploaded_at__date__gte=datetime.datetime.strptime(date_from, '%Y-%m-%d').date())
            except Exception:
                pass
        if date_to:
            try:
                qs = qs.filter(uploaded_at__date__lte=datetime.datetime.strptime(date_to, '%Y-%m-%d').date())
            except Exception:
                pass
        if status:
            qs = qs.filter(status=status)
        qs = qs.order_by('-uploaded_at')[:100]
        logs = []
        for study in qs:
            first_instance = None
            for series in study.series.all():
                if series.instances.all():
                    first_instance = series.instances.first()
                    break
            logs.append({
                'id': study.id,
                'uploaded_at': study.uploaded_at,
                'patient_name': study.patient.full_name if study.patient else '',
                'patient_medical_id': study.patient.medical_id if study.patient else '',
                'file_name': first_instance.file.name if first_instance and first_instance.file else '',
                'uploaded_by_name': study.uploaded_by.full_name if study.uploaded_by else '',
                'status': study.status,
            })
        return Response(logs)

    @action(methods=['post'], detail=False, url_path='direct_upload')
    def direct_upload(self, request):
        from patients.models import Patient
        from .models import DicomSeries, DicomInstance
        from .serializers import DicomStudySerializer
        medical_id = request.data.get('patient_medical_id')
        dicom_file = request.FILES.get('file')
        from .models import ActionLog
        if not medical_id or not dicom_file:
            ActionLog.objects.create(
                user=request.user,
                action='DICOM_UPLOAD',
                target_type='Patient',
                target_id=medical_id or '',
                status='FAIL',
                message='patient_medical_id et fichier requis.'
            )
            return Response({'detail': 'patient_medical_id et fichier requis.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            patient = Patient.objects.get(medical_id=medical_id)
        except Patient.DoesNotExist:
            ActionLog.objects.create(
                user=request.user,
                action='DICOM_UPLOAD',
                target_type='Patient',
                target_id=medical_id,
                status='FAIL',
                message='Patient introuvable.'
            )
            return Response({'detail': 'Patient introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        # Création de l'étude
        study = DicomStudy.objects.create(
            patient=patient,
            modality='OT',  # ou extraire du DICOM si possible
            status='UPLOADED',
            uploaded_by=request.user
        )
        # Création d'une série
        series = DicomSeries.objects.create(
            study=study,
            series_instance_uid=str(uuid.uuid4()),
            series_number=1
        )
        # Création de l'instance DICOM
        instance = DicomInstance.objects.create(
            series=series,
            sop_instance_uid=str(uuid.uuid4()),
            instance_number=1,
            file=dicom_file
        )
        serializer = DicomStudySerializer(study, context={'request': request})
        ActionLog.objects.create(
            user=request.user,
            action='DICOM_UPLOAD',
            target_type='DicomStudy',
            target_id=str(study.id),
            status='SUCCESS',
            message=f'Upload DICOM direct pour le patient {patient.full_name} ({patient.medical_id})'
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    queryset = DicomStudy.objects.all()
    serializer_class = DicomStudySerializer
    permission_classes = [permissions.IsAuthenticated & (IsMedecin | IsRadiologue | IsTechnicien)]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['patient', 'medical_record', 'study_date', 'modality', 'status']
    search_fields = ['study_description', 'study_instance_uid']
    ordering_fields = ['study_date', 'study_time', 'uploaded_at']
    
    def create(self, request, *args, **kwargs):
        from .models import ActionLog
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # Vérifier si un fichier DICOM est fourni
            if 'dicom_file' not in request.FILES:
                return Response(
                    {'detail': 'Aucun fichier DICOM fourni'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Lire le fichier DICOM
            dicom_file = request.FILES['dicom_file']
            file_content = dicom_file.read()
            
            # Envoyer le fichier à Orthanc
            orthanc_url = f"{settings.ORTHANC_URL}/instances"
            auth = (settings.ORTHANC_USERNAME, settings.ORTHANC_PASSWORD)
            
            try:
                response = requests.post(
                    orthanc_url,
                    data=file_content,
                    auth=auth,
                    headers={'Content-Type': 'application/dicom'},
                    timeout=30
                )
                response.raise_for_status()
                orthanc_data = response.json()
                
                # Préparer les données pour la création de l'étude
                data = request.data.copy()
                data['dicom_file'] = request.FILES['dicom_file']
                data['uploaded_by'] = request.user.id
                data['orthanc_id'] = orthanc_data.get('ParentStudy', orthanc_data.get('ID'))
                
                # Extraire les métadonnées DICOM si disponibles
                if 'MainDicomTags' in orthanc_data:
                    tags = orthanc_data['MainDicomTags']
                    data.update({
                        'study_instance_uid': tags.get('StudyInstanceUID', ''),
                        'study_date': tags.get('StudyDate', timezone.now().date()),
                        'study_time': tags.get('StudyTime', timezone.now().time()),
                        'study_description': tags.get('StudyDescription', ''),
                        'modality': tags.get('Modality', 'OT')
                    })
                
                # Créer l'étude dans la base de données
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                
                # Journaliser la création réussie
                study = serializer.instance
                ActionLog.objects.create(
                    user=request.user,
                    action='DICOM_STUDY_CREATE',
                    target_type='DicomStudy',
                    target_id=str(study.id),
                    status='SUCCESS',
                    message=f'Étude DICOM créée et envoyée à Orthanc pour le patient {study.patient.full_name}'
                )
                
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                
            except requests.RequestException as e:
                error_msg = f"Erreur lors de l'envoi à Orthanc: {str(e)}"
                logger.error(error_msg, exc_info=True)
                
                ActionLog.objects.create(
                    user=request.user,
                    action='DICOM_STUDY_CREATE',
                    target_type='DicomStudy',
                    target_id='',
                    status='FAIL',
                    message=error_msg
                )
                
                return Response(
                    {'detail': "Échec de l'envoi du fichier DICOM à Orthanc"},
                    status=status.HTTP_502_BAD_GATEWAY
                )
            
        except Exception as e:
            # Journaliser l'erreur
            error_msg = f"Erreur lors de la création de l'étude DICOM: {str(e)}"
            logger.error(error_msg, exc_info=True)
            
            ActionLog.objects.create(
                user=request.user,
                action='DICOM_STUDY_CREATE',
                target_type='DicomStudy',
                target_id='',
                status='FAIL',
                message=error_msg
            )
            
            return Response(
                {'detail': 'Une erreur est survenue lors de la création de l\'étude DICOM'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def perform_create(self, serializer):
        # Cette méthode est appelée par create() après la validation
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def upload_to_orthanc(self, request, pk=None):
        study = self.get_object()
        
        # Vérifier si l'étude a déjà un orthanc_id
        if study.orthanc_id:
            return Response(
                {"detail": "Cette étude a déjà été téléchargée vers Orthanc."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier si le fichier est présent dans la requête
        if 'dicom_file' not in request.FILES:
            return Response(
                {"detail": "Fichier DICOM manquant."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        dicom_file = request.FILES['dicom_file']
        
        # Lire le fichier DICOM
        file_content = dicom_file.read()
        
        # Encoder le contenu en base64
        file_base64 = base64.b64encode(file_content).decode('utf-8')
        
        # Envoyer le fichier à Orthanc
        orthanc_url = f"{settings.ORTHANC_URL}/instances"
        auth = (settings.ORTHANC_USERNAME, settings.ORTHANC_PASSWORD)
        
        try:
            response = requests.post(
                orthanc_url,
                data=file_base64,
                auth=auth,
                headers={'Content-Type': 'application/dicom'}
            )
            
            if response.status_code == 200:
                # Extraire les IDs Orthanc
                data = response.json()
                
                # Mettre à jour l'étude avec l'ID Orthanc
                if 'StudyID' in data:
                    study.orthanc_id = data['StudyID']
                    study.save()
                
                # Créer les séries et instances si présentes
                if 'SeriesID' in data:
                    series = DicomSeries.objects.create(
                        study=study,
                        series_instance_uid=data.get('SeriesUID', ''),
                        series_number=data.get('SeriesNumber', 0),
                        orthanc_id=data['SeriesID']
                    )
                    
                    if 'ID' in data:
                        instance = DicomInstance.objects.create(
                            series=series,
                            sop_instance_uid=data.get('SOPInstanceUID', ''),
                            instance_number=data.get('InstanceNumber', 0),
                            orthanc_id=data['ID'],
                            file=dicom_file
                        )
                
                return Response({
                    "detail": "Fichier DICOM téléchargé avec succès vers Orthanc.",
                    "orthanc_ids": data
                })
            else:
                return Response(
                    {"detail": f"Erreur lors du téléchargement vers Orthanc: {response.text}"},
                    status=response.status_code
                )
        except Exception as e:
            return Response(
                {"detail": f"Erreur de communication avec Orthanc: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DicomSeriesViewSet(viewsets.ModelViewSet):
    queryset = DicomSeries.objects.all()
    serializer_class = DicomSeriesSerializer
    permission_classes = [permissions.IsAuthenticated & (IsMedecin | IsRadiologue | IsTechnicien)]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['study', 'body_part']
    ordering_fields = ['series_number', 'created_at']
    
    def get_queryset(self):
        return DicomSeries.objects.filter(study_id=self.kwargs.get('study_id'))

class DicomInstanceViewSet(viewsets.ModelViewSet):
    queryset = DicomInstance.objects.all()
    serializer_class = DicomInstanceSerializer
    permission_classes = [permissions.IsAuthenticated & (IsMedecin | IsRadiologue | IsTechnicien)]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['series']
    ordering_fields = ['instance_number', 'created_at']
    
    def get_queryset(self):
        return DicomInstance.objects.filter(series_id=self.kwargs.get('series_id'))
    
    def retrieve(self, request, *args, **kwargs):
        """Surcharge pour gérer le téléchargement du fichier DICOM"""
        instance = self.get_object()
        
        # Vérifier si on doit retourner le fichier ou les métadonnées
        if request.query_params.get('download') == 'true':
            if not instance.file:
                return Response(
                    {'detail': 'Aucun fichier associé à cette instance'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            try:
                response = FileResponse(instance.file)
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(instance.file.name)}"'
                response['Content-Type'] = 'application/dicom'
                return response
            except FileNotFoundError:
                return Response(
                    {'detail': 'Le fichier DICOM est introuvable sur le serveur'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Comportement par défaut (retourne les métadonnées)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class RadiologyReportViewSet(viewsets.ModelViewSet):
    queryset = RadiologyReport.objects.all()
    serializer_class = RadiologyReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['study', 'radiologist', 'status']
    search_fields = ['findings', 'impression', 'recommendations']
    ordering_fields = ['created_at', 'updated_at', 'finalized_at']
    
    def perform_create(self, serializer):
        serializer.save(radiologist=self.request.user)
    
    @action(detail=True, methods=['post'])
    def finalize(self, request, pk=None):
        report = self.get_object()
        
        # Vérifier si le rapport peut être finalisé
        if report.status == 'FINAL' or report.status == 'AMENDED':
            return Response(
                {"detail": "Ce rapport est déjà finalisé."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier si l'utilisateur est un radiologue
        if not hasattr(request.user, 'role') or request.user.role != 'RADIOLOGUE':
            return Response(
                {"detail": "Seul un radiologue peut finaliser un rapport."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Mettre à jour le statut et la date de finalisation
        report.status = 'FINAL'
        report.finalized_at = timezone.now()
        report.save()
        
        # Mettre à jour le statut de l'étude associée
        study = report.study
        study.status = 'REPORTED'
        study.save()
        
        return Response({"detail": "Rapport finalisé avec succès."})