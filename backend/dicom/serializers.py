from rest_framework import serializers
from .models import DICOMStudy, DICOMSeries, DICOMInstance
from patients.serializers import PatientSerializer

class DICOMInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DICOMInstance
        fields = '__all__'
        read_only_fields = ('created_at',)

class DICOMSeriesSerializer(serializers.ModelSerializer):
    instance_count = serializers.IntegerField(source='instances.count', read_only=True)
    
    class Meta:
        model = DICOMSeries
        fields = '__all__'
        read_only_fields = ('created_at',)

class DICOMStudySerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    patient_id = serializers.UUIDField(write_only=True)
    series_count = serializers.IntegerField(source='series.count', read_only=True)
    
    class Meta:
        model = DICOMStudy
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def validate_patient_id(self, value):
        from patients.models import Patient
        try:
            Patient.objects.get(pk=value)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient non trouvé")
        return value
    
    def create(self, validated_data):
        from patients.models import Patient
        patient_id = validated_data.pop('patient_id')
        patient = Patient.objects.get(pk=patient_id)
        return DICOMStudy.objects.create(patient=patient, **validated_data)
