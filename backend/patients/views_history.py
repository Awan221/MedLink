from rest_framework import generics
from .models import MedicalRecordHistory, PatientHistory
from .serializers import MedicalRecordHistorySerializer, PatientHistorySerializer

class MedicalRecordHistoryList(generics.ListAPIView):
    serializer_class = MedicalRecordHistorySerializer

    def get_queryset(self):
        medical_record_id = self.kwargs['medical_record_id']
        return MedicalRecordHistory.objects.filter(medical_record__id=medical_record_id).order_by('-performed_at')

class PatientHistoryList(generics.ListAPIView):
    serializer_class = PatientHistorySerializer

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return PatientHistory.objects.filter(patient__id=patient_id).order_by('-performed_at')
