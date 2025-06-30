from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance as DistanceFunction

from .models import BloodBankCenter, BloodStock, BloodDonation, BloodRequest
from .serializers import (
    BloodBankCenterSerializer, BloodStockSerializer, 
    BloodDonationSerializer, BloodRequestSerializer
)
from authentication.permissions import IsMedecin, IsBanqueSang

class BloodBankCenterViewSet(viewsets.ModelViewSet):
    queryset = BloodBankCenter.objects.all()
    serializer_class = BloodBankCenterSerializer
    permission_classes = [permissions.AllowAny]  # Accès public en lecture seule
    
    def get_queryset(self):
        from django.contrib.gis.geos import Point
        queryset = super().get_queryset()
        # Ajouter des coordonnées par défaut pour les centres qui n'en ont pas
        for center in queryset.filter(location__isnull=True):
            center.location = Point(-17.4677, 14.7167, srid=4326)  # Dakar par défaut
            center.save(update_fields=['location'])
        return queryset
    
    def get_permissions(self):
        # Seulement la lecture est autorisée sans authentification
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        # Les autres actions nécessitent une authentification
        return [permissions.IsAuthenticated()]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['region']
    search_fields = ['name', 'address', 'region']
    ordering_fields = ['name', 'region']
    
    @action(detail=False, methods=['get'])
    def nearby(self, request):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        radius = request.query_params.get('radius', 10)  # km
        
        if not latitude or not longitude:
            return Response(
                {"detail": "Les paramètres latitude et longitude sont requis."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            radius = float(radius)
        except ValueError:
            return Response(
                {"detail": "Les coordonnées doivent être des nombres valides."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_location = Point(longitude, latitude, srid=4326)
        
        centers = BloodBankCenter.objects.filter(
            location__distance_lte=(user_location, Distance(km=radius))
        ).annotate(
            distance=DistanceFunction('location', user_location)
        ).order_by('distance')
        
        serializer = self.get_serializer(centers, many=True)
        return Response(serializer.data)

class BloodStockViewSet(viewsets.ModelViewSet):
    queryset = BloodStock.objects.all()
    serializer_class = BloodStockSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsBanqueSang | IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user, last_updated=timezone.now())
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user, last_updated=timezone.now())
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['center', 'blood_group']
    ordering_fields = ['center', 'blood_group', 'units_available', 'last_updated']
    
    @action(detail=False, methods=['get'])
    def by_blood_group(self, request):
        blood_group = request.query_params.get('blood_group')
        
        if not blood_group:
            return Response(
                {"detail": "Le paramètre blood_group est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        stocks = BloodStock.objects.filter(blood_group=blood_group).order_by('-units_available')
        serializer = self.get_serializer(stocks, many=True)
        return Response(serializer.data)

class BloodDonationViewSet(viewsets.ModelViewSet):
    queryset = BloodDonation.objects.all()
    serializer_class = BloodDonationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['center', 'blood_group', 'status', 'donation_date']
    search_fields = ['donor_name', 'donor_email', 'donor_phone']
    ordering_fields = ['donation_date', 'created_at']
    
    @action(detail=True, methods=['post'], permission_classes=[IsBanqueSang])
    def complete(self, request, pk=None):
        donation = self.get_object()
        
        if donation.status != 'SCHEDULED':
            return Response(
                {"detail": "Ce don n'est pas programmé."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        donation.status = 'COMPLETED'
        donation.completed_by = request.user
        donation.save()
        
        # Mettre à jour le stock de sang
        try:
            stock = BloodStock.objects.get(center=donation.center, blood_group=donation.blood_group)
            stock.units_available += 1
            stock.last_updated = timezone.now()
            stock.updated_by = request.user
            stock.save()
        except BloodStock.DoesNotExist:
            BloodStock.objects.create(
                center=donation.center,
                blood_group=donation.blood_group,
                units_available=1,
                last_updated=timezone.now(),
                updated_by=request.user
            )
        
        return Response({"detail": "Don complété avec succès."})

class BloodRequestViewSet(viewsets.ModelViewSet):
    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['center', 'blood_group', 'priority', 'status']
    search_fields = ['patient_name', 'reason']
    ordering_fields = ['priority', 'created_at']
    
    def perform_create(self, serializer):
        serializer.save(requesting_doctor=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsBanqueSang])
    def approve(self, request, pk=None):
        blood_request = self.get_object()
        
        if blood_request.status != 'PENDING':
            return Response(
                {"detail": "Cette demande n'est pas en attente."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier la disponibilité du stock
        try:
            stock = BloodStock.objects.get(center=blood_request.center, blood_group=blood_request.blood_group)
            
            if stock.units_available < blood_request.units_requested:
                return Response(
                    {"detail": "Stock insuffisant pour cette demande."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Mettre à jour le stock
            stock.units_available -= blood_request.units_requested
            stock.last_updated = timezone.now()
            stock.updated_by = request.user
            stock.save()
            
            # Mettre à jour la demande
            blood_request.status = 'APPROVED'
            blood_request.approved_by = request.user
            blood_request.save()
            
            return Response({"detail": "Demande approuvée avec succès."})
            
        except BloodStock.DoesNotExist:
            return Response(
                {"detail": "Aucun stock disponible pour ce groupe sanguin."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsBanqueSang])
    def fulfill(self, request, pk=None):
        blood_request = self.get_object()
        
        if blood_request.status != 'APPROVED':
            return Response(
                {"detail": "Cette demande n'est pas approuvée."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        blood_request.status = 'FULFILLED'
        blood_request.fulfilled_at = timezone.now()
        blood_request.save()
        
        return Response({"detail": "Demande satisfaite avec succès."})