from django.db import models
from django.utils import timezone
from authentication.models import User
from patients.models import Patient, MedicalRecord
import uuid

class AIModel(models.Model):
    MODEL_TYPE_CHOICES = (
        ('CLASSIFICATION', 'Classification'),
        ('REGRESSION', 'Régression'),
        ('ANOMALY', 'Détection d\'anomalies'),
        ('SEGMENTATION', 'Segmentation d\'image'),
    )
    
    STATUS_CHOICES = (
        ('DEVELOPMENT', 'En développement'),
        ('TESTING', 'En test'),
        ('PRODUCTION', 'En production'),
        ('DEPRECATED', 'Déprécié'),
    )
    
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    model_type = models.CharField(max_length=20, choices=MODEL_TYPE_CHOICES)
    description = models.TextField()
    target_disease = models.CharField(max_length=100)
    accuracy = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DEVELOPMENT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Métadonnées
    training_date = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_models')
    
    class Meta:
        app_label = 'ai_diagnostic'
        db_table = 'ai_diagnostic_models'
        verbose_name = 'Modèle IA'
        verbose_name_plural = 'Modèles IA'
        ordering = ['name', '-version']
        unique_together = ('name', 'version')

class AIPrediction(models.Model):
    SEVERITY_CHOICES = (
        ('LOW', 'Faible'),
        ('MEDIUM', 'Moyenne'),
        ('HIGH', 'Élevée'),
        ('CRITICAL', 'Critique'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='ai_predictions')
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_predictions')
    model = models.ForeignKey(AIModel, on_delete=models.PROTECT, related_name='predictions')
    
    # Résultats de prédiction
    prediction_result = models.TextField()
    confidence_score = models.FloatField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    requires_attention = models.BooleanField(default=False)
    
    # Données d'entrée
    input_data = models.JSONField(help_text="Données utilisées pour la prédiction")
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_predictions')
    
    # Validation
    validated = models.BooleanField(default=False)
    validated_at = models.DateTimeField(null=True, blank=True)
    validated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='validated_predictions')
    validation_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Prédiction pour {self.patient.full_name} - {self.model.name}"
    
    class Meta:
        verbose_name = 'Prédiction IA'
        verbose_name_plural = 'Prédictions IA'
        ordering = ['-created_at']

class AIAlert(models.Model):
    ALERT_TYPE_CHOICES = (
        ('ANOMALY', 'Anomalie détectée'),
        ('CRITICAL', 'Valeur critique'),
        ('TREND', 'Tendance inquiétante'),
        ('INTERACTION', 'Interaction médicamenteuse'),
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'En attente'),
        ('VIEWED', 'Vue'),
        ('ACKNOWLEDGED', 'Confirmée'),
        ('RESOLVED', 'Résolue'),
        ('DISMISSED', 'Ignorée'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prediction = models.ForeignKey(AIPrediction, on_delete=models.CASCADE, related_name='alerts')
    
    # Détails de l'alerte
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Destinataires
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_alerts')
    
    # Suivi
    created_at = models.DateTimeField(auto_now_add=True)
    viewed_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_alert_type_display()} pour {self.prediction.patient.full_name}"
    
    class Meta:
        verbose_name = 'Alerte IA'
        verbose_name_plural = 'Alertes IA'
        ordering = ['-created_at']