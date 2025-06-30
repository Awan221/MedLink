from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
import json
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from .models import AIModel, AIPrediction, AIAlert
from .serializers import AIModelSerializer, AIPredictionSerializer, AIAlertSerializer
from authentication.permissions import IsAdmin, IsMedecin, IsSpecialiste
from patients.models import Patient, MedicalRecord

class AIModelViewSet(viewsets.ModelViewSet):
    queryset = AIModel.objects.all()
    serializer_class = AIModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['model_type', 'target_disease', 'status']
    search_fields = ['name', 'description', 'target_disease']
    ordering_fields = ['name', 'version', 'accuracy', 'training_date']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated & IsAdmin]
        return super().get_permissions()

class AIPredictionViewSet(viewsets.ModelViewSet):
    queryset = AIPrediction.objects.all()
    serializer_class = AIPredictionSerializer
    permission_classes = [permissions.IsAuthenticated & (IsMedecin | IsSpecialiste)]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['patient', 'model', 'severity', 'requires_attention', 'validated']
    search_fields = ['prediction_result', 'validation_notes']
    ordering_fields = ['created_at', 'confidence_score']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['post'])
    def predict(self, request):
        patient_id = request.data.get('patient_id')
        model_id = request.data.get('model_id')
        medical_record_id = request.data.get('medical_record_id')
        input_data = request.data.get('input_data')
        
        if not patient_id or not model_id or not input_data:
            return Response(
                {"detail": "Les paramètres patient_id, model_id et input_data sont requis."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            patient = Patient.objects.get(id=patient_id)
            model = AIModel.objects.get(id=model_id)
            
            medical_record = None
            if medical_record_id:
                medical_record = MedicalRecord.objects.get(id=medical_record_id, patient=patient)
            
            # Simulation d'une prédiction IA (à remplacer par l'appel réel au modèle)
            # Dans un environnement réel, vous feriez appel à un service ML ou à une API
            prediction_result, confidence, severity = self._simulate_prediction(model, input_data)
            
            # Créer la prédiction
            prediction = AIPrediction.objects.create(
                patient=patient,
                medical_record=medical_record,
                model=model,
                prediction_result=prediction_result,
                confidence_score=confidence,
                severity=severity,
                requires_attention=severity in ['HIGH', 'CRITICAL'],
                input_data=input_data,
                created_by=request.user
            )
            
            # Créer une alerte si nécessaire
            if severity in ['HIGH', 'CRITICAL']:
                alert = AIAlert.objects.create(
                    prediction=prediction,
                    alert_type='ANOMALY',
                    title=f"Alerte {severity} pour {patient.full_name}",
                    description=f"Le modèle {model.name} a détecté une anomalie avec une confiance de {confidence:.2f}. Résultat: {prediction_result}",
                    assigned_to=request.user
                )
            
            serializer = self.get_serializer(prediction)
            return Response(serializer.data)
            
        except (Patient.DoesNotExist, AIModel.DoesNotExist, MedicalRecord.DoesNotExist) as e:
            return Response(
                {"detail": f"Objet non trouvé: {str(e)}"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": f"Erreur lors de la prédiction: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _simulate_prediction(self, model, input_data):
        """Simulation d'une prédiction IA pour démonstration."""
        # Note: Cette fonction simule une prédiction. 
        # Dans un environnement réel, vous utiliseriez un modèle ML déjà formé.
        
        # Simuler différents résultats en fonction du modèle
        if model.model_type == 'CLASSIFICATION':
            # Pour les modèles de classification de maladies
            if model.target_disease == 'Diabète':
                prediction = "Risque de diabète de type 2"
                confidence = np.random.uniform(0.7, 0.95)
            elif model.target_disease == 'Cardiaque':
                prediction = "Risque d'insuffisance cardiaque"
                confidence = np.random.uniform(0.6, 0.9)
            else:
                prediction = f"Risque de {model.target_disease}"
                confidence = np.random.uniform(0.5, 0.85)
        
        elif model.model_type == 'ANOMALY':
            # Pour les modèles de détection d'anomalies
            anomaly_detected = np.random.choice([True, False], p=[0.3, 0.7])
            prediction = "Anomalie détectée" if anomaly_detected else "Aucune anomalie détectée"
            confidence = np.random.uniform(0.6, 0.95) if anomaly_detected else np.random.uniform(0.75, 0.98)
        
        else:
            # Pour les autres types de modèles
            prediction = "Résultat de prédiction générique"
            confidence = np.random.uniform(0.6, 0.9)
        
        # Déterminer la sévérité en fonction de la confiance et du type de prédiction
        if "Aucune" in prediction or "Normal" in prediction:
            severity = "LOW"
        elif confidence > 0.85 and ("Risque" in prediction or "Anomalie" in prediction):
            severity = "HIGH" if confidence > 0.92 else "MEDIUM"
        elif "Critique" in prediction or confidence > 0.95:
            severity = "CRITICAL"
        else:
            severity = "MEDIUM"
        
        return prediction, float(confidence), severity
    
    @action(detail=True, methods=['post'])
    def validate(self, request, pk=None):
        prediction = self.get_object()
        validation_status = request.data.get('validated', True)
        validation_notes = request.data.get('validation_notes', '')
        
        prediction.validated = validation_status
        prediction.validated_at = timezone.now()
        prediction.validated_by = request.user
        prediction.validation_notes = validation_notes
        prediction.save()
        
        return Response({
            "detail": "Prédiction validée avec succès.",
            "validated": prediction.validated,
            "validated_at": prediction.validated_at
        })

class AIAlertViewSet(viewsets.ModelViewSet):
    queryset = AIAlert.objects.all()
    serializer_class = AIAlertSerializer
    permission_classes = [permissions.IsAuthenticated & (IsMedecin | IsSpecialiste)]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['prediction__patient', 'alert_type', 'status', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'viewed_at', 'resolved_at']
    
    def get_queryset(self):
        user = self.request.user
        
        # Filtrer les alertes par utilisateur assigné, sauf pour les administrateurs
        if user.is_staff or user.role in ['ADMIN', 'SUPER_ADMIN']:
            return AIAlert.objects.all()
        
        return AIAlert.objects.filter(assigned_to=user)
    
    @action(detail=True, methods=['post'])
    def mark_as_viewed(self, request, pk=None):
        alert = self.get_object()
        
        if alert.status == 'PENDING':
            alert.status = 'VIEWED'
            alert.viewed_at = timezone.now()
            alert.save()
        
        return Response({
            "detail": "Alerte marquée comme vue.",
            "status": alert.status,
            "viewed_at": alert.viewed_at
        })
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        alert = self.get_object()
        resolution_notes = request.data.get('resolution_notes', '')
        
        if alert.status in ['PENDING', 'VIEWED', 'ACKNOWLEDGED']:
            alert.status = 'RESOLVED'
            alert.resolved_at = timezone.now()
            alert.resolution_notes = resolution_notes
            alert.save()
        
        return Response({
            "detail": "Alerte résolue avec succès.",
            "status": alert.status,
            "resolved_at": alert.resolved_at
        })
    
    @action(detail=True, methods=['post'])
    def dismiss(self, request, pk=None):
        alert = self.get_object()
        dismissal_reason = request.data.get('dismissal_reason', '')
        
        if alert.status in ['PENDING', 'VIEWED', 'ACKNOWLEDGED']:
            alert.status = 'DISMISSED'
            alert.resolved_at = timezone.now()
            alert.resolution_notes = f"Alerte ignorée. Raison: {dismissal_reason}"
            alert.save()
        
        return Response({
            "detail": "Alerte ignorée avec succès.",
            "status": alert.status
        })