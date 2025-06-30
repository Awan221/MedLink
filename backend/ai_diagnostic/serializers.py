from rest_framework import serializers
from .models import AIModel, AIPrediction, AIAlert

class AIModelSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = AIModel
        fields = ['id', 'name', 'version', 'model_type', 'description', 
                 'target_disease', 'accuracy', 'status', 'training_date', 
                 'last_updated', 'created_by', 'created_by_name']
        read_only_fields = ['id', 'last_updated', 'created_by']

class AIPredictionSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    model_name = serializers.CharField(source='model.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = AIPrediction
        fields = ['id', 'patient', 'patient_name', 'medical_record', 
                 'model', 'model_name', 'prediction_result', 'confidence_score', 
                 'severity', 'requires_attention', 'input_data', 
                 'created_at', 'created_by', 'created_by_name', 
                 'validated', 'validated_at', 'validated_by', 'validation_notes']
        read_only_fields = ['id', 'created_at', 'created_by']

class AIAlertSerializer(serializers.ModelSerializer):
    prediction_id = serializers.CharField(source='prediction.id', read_only=True)
    patient_name = serializers.CharField(source='prediction.patient.full_name', read_only=True)
    
    class Meta:
        model = AIAlert
        fields = ['id', 'prediction', 'prediction_id', 'patient_name', 
                 'alert_type', 'title', 'description', 'status', 
                 'assigned_to', 'created_at', 'viewed_at', 
                 'resolved_at', 'resolution_notes']
        read_only_fields = ['id', 'created_at', 'viewed_at', 'resolved_at']

