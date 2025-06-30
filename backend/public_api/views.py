from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, throttling, generics, filters
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from patients.models import Appointment, Patient
from blood_bank.models import BloodDonation, BloodBankCenter
from .models import Disease, DiseaseCategory
from .serializers import (
    PublicAppointmentSerializer, PublicDonorSerializer, PublicContactSerializer,
    DiseaseListSerializer, DiseaseDetailSerializer, DiseaseCategorySerializer
)


class DiseaseCategoryList(generics.ListAPIView):
    """
    Liste toutes les catégories de maladies disponibles.
    """
    queryset = DiseaseCategory.objects.all()
    serializer_class = DiseaseCategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None


class DiseaseList(generics.ListAPIView):
    """
    Liste toutes les maladies publiées avec possibilité de filtrage et de recherche.
    """
    serializer_class = DiseaseListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'category': ['exact'],
        'severity': ['exact'],
        'is_emergency': ['exact'],
    }
    search_fields = ['name', 'scientific_name', 'short_description', 'main_symptoms']
    ordering_fields = ['name', 'severity', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        queryset = Disease.objects.filter(is_published=True)
        
        # Filtre par recherche textuelle
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(scientific_name__icontains=search_query) |
                Q(short_description__icontains=search_query) |
                Q(main_symptoms__icontains=search_query)
            )
            
        return queryset.select_related('category').prefetch_related('resources')


class DiseaseDetail(generics.RetrieveAPIView):
    """
    Détails d'une maladie spécifique.
    """
    queryset = Disease.objects.filter(is_published=True)
    serializer_class = DiseaseDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class DiseaseSearchView(generics.ListAPIView):
    """
    Recherche avancée dans les maladies.
    """
    serializer_class = DiseaseListSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Disease.objects.filter(is_published=True)
        
        # Filtres de recherche
        query = self.request.query_params.get('q', None)
        category = self.request.query_params.get('category', None)
        severity = self.request.query_params.get('severity', None)
        
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(scientific_name__icontains=query) |
                Q(short_description__icontains=query) |
                Q(main_symptoms__icontains=query) |
                Q(other_symptoms__icontains=query)
            )
            
        if category:
            queryset = queryset.filter(category__slug=category)
            
        if severity:
            queryset = queryset.filter(severity=severity)
            
        return queryset.select_related('category')

class PublicAppointmentView(APIView):
    """
    Endpoint pour la prise de rendez-vous publique.
    Throttling activé pour éviter le spam.
    """
    throttle_classes = [throttling.AnonRateThrottle]
    
    def post(self, request):
        serializer = PublicAppointmentSerializer(data=request.data)
        if serializer.is_valid():
            # Créer ou récupérer le patient
            patient, created = Patient.objects.get_or_create(
                phone=serializer.validated_data['phone'],
                defaults={
                    'first_name': serializer.validated_data['name'].split()[0],
                    'last_name': ' '.join(serializer.validated_data['name'].split()[1:]),
                    'email': serializer.validated_data.get('email', '')
                }
            )
            
            # Créer le rendez-vous
            appointment = Appointment.objects.create(
                patient=patient,
                scheduled_datetime=serializer.validated_data['date'],
                reason=serializer.validated_data['reason'],
                status='pending'
            )
            
            # Envoyer un email de confirmation
            send_mail(
                'Confirmation de demande de rendez-vous',
                f'Votre demande de rendez-vous pour le {appointment.scheduled_datetime.strftime("%d/%m/%Y")} a bien été enregistrée. Nous vous contacterons pour confirmer.',
                settings.DEFAULT_FROM_EMAIL,
                [patient.email] if patient.email else [],
                fail_silently=True
            )
            
            return Response(
                {'success': 'Demande de rendez-vous enregistrée.'}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PublicDonorView(APIView):
    """
    Endpoint pour l'inscription des donneurs de sang.
    Throttling activé pour éviter le spam.
    """
    throttle_classes = [throttling.AnonRateThrottle]
    
    def post(self, request):
        serializer = PublicDonorSerializer(data=request.data)
        if serializer.is_valid():
            # Trouver le centre le plus proche
            center = BloodBankCenter.objects.filter(
                region=serializer.validated_data.get('region', '')
            ).first()
            
            if not center:
                return Response(
                    {'error': 'Aucun centre de don trouvé dans votre région.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Créer le don
            donation = BloodDonation.objects.create(
                center=center,
                donor_name=serializer.validated_data['name'],
                donor_phone=serializer.validated_data['phone'],
                donor_email=serializer.validated_data.get('email', ''),
                blood_group=serializer.validated_data['blood_group'],
                donation_date=timezone.now() + timezone.timedelta(days=7),  # Par défaut dans 7 jours
                status='SCHEDULED'
            )
            
            # Envoyer un email de confirmation
            if donation.donor_email:
                send_mail(
                    'Confirmation d\'inscription au don de sang',
                    f'Votre don de sang a été programmé pour le {donation.donation_date.strftime("%d/%m/%Y")} au centre {center.name}.',
                    settings.DEFAULT_FROM_EMAIL,
                    [donation.donor_email],
                    fail_silently=True
                )
            
            return Response(
                {'success': 'Inscription au don de sang enregistrée.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PublicContactView(APIView):
    """
    Endpoint pour le formulaire de contact.
    Throttling activé pour éviter le spam.
    """
    throttle_classes = [throttling.AnonRateThrottle]
    
    def post(self, request):
        serializer = PublicContactSerializer(data=request.data)
        if serializer.is_valid():
            # Envoyer l'email au support
            send_mail(
                f'Nouveau message de contact de {serializer.validated_data["name"]}',
                f"""
                Nom: {serializer.validated_data['name']}
                Email: {serializer.validated_data['email']}
                Téléphone: {serializer.validated_data['phone']}
                
                Message:
                {serializer.validated_data['message']}
                """,
                settings.DEFAULT_FROM_EMAIL,
                [settings.SUPPORT_EMAIL],
                fail_silently=True
            )
            
            # Envoyer un email de confirmation
            send_mail(
                'Confirmation de votre message',
                'Nous avons bien reçu votre message et nous vous répondrons dans les plus brefs délais.',
                settings.DEFAULT_FROM_EMAIL,
                [serializer.validated_data['email']],
                fail_silently=True
            )
            
            return Response(
                {'success': 'Message envoyé avec succès.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
