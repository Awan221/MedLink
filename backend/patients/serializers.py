from rest_framework import serializers
from .models import Patient, MedicalRecord, Prescription, MedicalRecordHistory, PrescriptionHistory, Appointment, PatientHistory

import random
from datetime import datetime

class PatientSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'medical_id', 'national_id', 'first_name', 'last_name', 
                 'full_name', 'gender', 'date_of_birth', 'age', 'blood_group',
                 'email', 'phone', 'address', 'region', 'allergies', 
                 'chronic_diseases', 'current_medications', 'created_by', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Génération automatique du medical_id si non fourni
        if not validated_data.get('medical_id'):
            today = datetime.now().strftime('%Y%m%d')
            for _ in range(10):
                random_digits = random.randint(1000, 9999)
                medical_id = f"MED-{today}-{random_digits}"
                if not Patient.objects.filter(medical_id=medical_id).exists():
                    validated_data['medical_id'] = medical_id
                    break
            else:
                raise serializers.ValidationError('Impossible de générer un medical_id unique. Réessayez.')
        # Création normale (mono-base)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Mise à jour normale (mono-base)
        return super().update(instance, validated_data)

        # Génération automatique du medical_id si non fourni
        if not validated_data.get('medical_id'):
            today = datetime.now().strftime('%Y%m%d')
            for _ in range(10):
                random_digits = random.randint(1000, 9999)
                medical_id = f"MED-{today}-{random_digits}"
                if not Patient.objects.filter(medical_id=medical_id).exists():
                    validated_data['medical_id'] = medical_id
                    break
            else:
                raise serializers.ValidationError('Impossible de générer un medical_id unique. Réessayez.')
        # Création dans la base régionale
        patient = super().create(validated_data)
        # Synchronisation dans la base centrale (default)
        Patient.objects.using('default').update_or_create(
            medical_id=patient.medical_id,
            defaults={
                'national_id': patient.national_id,
                'first_name': patient.first_name,
                'last_name': patient.last_name,
                'gender': patient.gender,
                'date_of_birth': patient.date_of_birth,
                'blood_group': patient.blood_group,
                'email': patient.email,
                'phone': patient.phone,
                'address': patient.address,
                'region': patient.region,
                'allergies': patient.allergies,
                'chronic_diseases': patient.chronic_diseases,
                'current_medications': patient.current_medications,
                'created_by': patient.created_by,
                'created_at': patient.created_at,
                'updated_at': patient.updated_at,
            }
        )
        return patient


class MedicalRecordSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'doctor', 'doctor_name', 'date', 'reason', 
                 'symptoms', 'diagnosis', 'treatment', 'notes', 'temperature', 
                 'blood_pressure', 'heart_rate', 'respiratory_rate', 'weight', 
                 'height', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class MedicalRecordHistorySerializer(serializers.ModelSerializer):
    performed_by = serializers.StringRelatedField()

    class Meta:
        model = MedicalRecordHistory
        fields = ['id', 'action', 'performed_by', 'performed_at', 'snapshot']

class PatientHistorySerializer(serializers.ModelSerializer):
    performed_by = serializers.StringRelatedField()

    class Meta:
        model = PatientHistory
        fields = ['id', 'action', 'performed_by', 'performed_at', 'snapshot']

class PrescriptionHistorySerializer(serializers.ModelSerializer):
    performed_by = serializers.StringRelatedField()

    class Meta:
        model = PrescriptionHistory
        fields = ['id', 'action', 'performed_by', 'performed_at', 'snapshot']

class PrescriptionSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)
    
    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'doctor', 'doctor_name', 'medical_record', 
                 'date', 'medications', 'dosage', 'duration', 'instructions', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'scheduled_datetime', 'status', 'reason', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'patient_name', 'doctor_name']
        read_only_fields = ['id', 'created_at', 'updated_at']