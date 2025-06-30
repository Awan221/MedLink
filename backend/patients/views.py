from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Patient, MedicalRecord, Prescription, Appointment
from .serializers import PatientSerializer, MedicalRecordSerializer, PrescriptionSerializer, AppointmentSerializer
from authentication.permissions import IsMedecin, IsSpecialiste

from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
try:
    from django.contrib.postgres.search import TrigramSimilarity
    HAS_TRIGRAM = True
except ImportError:
    HAS_TRIGRAM = False

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated & (IsMedecin | IsSpecialiste)]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gender', 'blood_group', 'region']
    search_fields = ['first_name', 'last_name', 'medical_id', 'national_id']
    ordering_fields = ['last_name', 'first_name', 'date_of_birth', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Patient.objects.all()
        return Patient.objects.none()

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='fuzzy-search')
    def fuzzy_search(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response([])
        qs = Patient.objects.all()
        if HAS_TRIGRAM:
            from django.db.models.functions import Greatest
            qs = qs.annotate(
                similarity=Greatest(
                    TrigramSimilarity('first_name', query),
                    TrigramSimilarity('last_name', query),
                    TrigramSimilarity('medical_id', query),
                    TrigramSimilarity('national_id', query)
                )
            ).filter(similarity__gt=0.2).order_by('-similarity')[:10]
        else:
            qs = qs.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(medical_id__icontains=query) |
                Q(national_id__icontains=query)
            )[:10]
        data = [
            {
                'id': p.id,
                'full_name': p.full_name,
                'medical_id': p.medical_id,
                'national_id': p.national_id,
                'gender': p.gender,
                'age': p.age,
            } for p in qs
        ]
        return Response(data)

    @action(detail=False, methods=['post'], url_path='check-duplicate')
    def check_duplicate(self, request):
        first_name = request.data.get('first_name', '').strip()
        last_name = request.data.get('last_name', '').strip()
        date_of_birth = request.data.get('date_of_birth', '').strip()
        if not (first_name and last_name and date_of_birth):
            return Response({'error': 'first_name, last_name et date_of_birth requis.'}, status=400)
        qs = Patient.objects.filter(
            first_name__iexact=first_name,
            last_name__iexact=last_name,
            date_of_birth=date_of_birth
        )
        # Recherche tolérante si pas de match strict
        if not qs.exists():
            qs = Patient.objects.filter(
                Q(first_name__icontains=first_name) |
                Q(last_name__icontains=last_name),
                date_of_birth=date_of_birth
            )
        data = [
            {
                'id': p.id,
                'full_name': p.full_name,
                'medical_id': p.medical_id,
                'national_id': p.national_id,
                'gender': p.gender,
                'age': p.age,
            } for p in qs
        ]
        return Response(data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated & (IsMedecin | IsSpecialiste)]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['patient', 'doctor', 'date']
    ordering_fields = ['date', 'created_at']
    
    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "has_permission") and user.has_permission("medicalrecords.view_all"):
            return MedicalRecord.objects.all()
        # Un médecin ou un patient ne voit que ses propres dossiers
        return MedicalRecord.objects.filter(Q(patient=user) | Q(doctor=user))

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated & (IsMedecin | IsSpecialiste)]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['patient', 'doctor', 'date']
    ordering_fields = ['date', 'created_at']
    
    def perform_create(self, serializer):
        serializer.save()
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "has_permission") and user.has_permission("prescriptions.view_all"):
            return Prescription.objects.all()
        # Un médecin ou un patient ne voit que ses propres prescriptions
        return Prescription.objects.filter(Q(patient=user) | Q(doctor=user))

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['patient', 'doctor', 'status', 'scheduled_datetime']
    ordering_fields = ['scheduled_datetime', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "has_permission") and user.has_permission("appointments.view_all"):
            return Appointment.objects.all()
        # Un patient ne peut voir que ses rendez-vous, un médecin que les siens
        return Appointment.objects.filter(Q(patient=user) | Q(doctor=user))

    def perform_create(self, serializer):
        serializer.save()

    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated & (IsMedecin | IsSpecialiste)]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['patient', 'doctor', 'date']
    ordering_fields = ['date', 'created_at']
    
    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)
    
    def get_queryset(self):
        return Prescription.objects.filter(patient_id=self.kwargs.get('patient_id'))
