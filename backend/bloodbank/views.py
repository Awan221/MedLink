from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, F, Q
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import BloodDonationCenter, BloodInventory, BloodDonation
from .serializers import (
    BloodDonationCenterSerializer, BloodInventorySerializer,
    BloodDonationSerializer, BloodDonationCenterWithDistanceSerializer
)
from authentication.permissions import IsMedecin, IsInfirmier, IsAdminUser

class BloodDonationCenterViewSet(viewsets.ModelViewSet):
    queryset = BloodDonationCenter.objects.filter(is_active=True)
    serializer_class = BloodDonationCenterSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['region', 'city', 'is_active']
    search_fields = ['name', 'city', 'region', 'address']
    ordering_fields = ['name', 'city', 'region', 'created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtre par distance si les coordonnées sont fournies
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        radius = self.request.query_params.get('radius', 50)  # 50km par défaut
        
        if lat and lng:
            try:
                user_location = Point(float(lng), float(lat), srid=4326)
                queryset = queryset.filter(
                    location__distance_lte=(user_location, float(radius) * 1000)
                ).annotate(
                    distance=Distance('location', user_location)
                ).order_by('distance')
            except (ValueError, TypeError):
                pass
                
        return queryset
    
    @action(detail=False, methods=['get'])
    def near_me(self, request):
        """Trouve les centres de don les plus proches d'une position donnée"""
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        radius_km = float(request.query_params.get('radius', 50))  # 50km par défaut
        
        if not (lat and lng):
            return Response(
                {"error": "Les paramètres 'lat' et 'lng' sont requis"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user_location = Point(float(lng), float(lat), srid=4326)
            
            # Trouver les centres dans un rayon donné (en mètres)
            centers = BloodDonationCenter.objects.filter(
                location__distance_lte=(user_location, radius_km * 1000)
            ).annotate(
                distance=Distance('location', user_location)
            ).order_by('distance')
            
            serializer = BloodDonationCenterWithDistanceSerializer(centers, many=True)
            return Response(serializer.data)
            
        except (ValueError, TypeError) as e:
            return Response(
                {"error": "Coordonnées GPS invalides"},
                status=status.HTTP_400_BAD_REQUEST
            )

class BloodInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BloodInventorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['center', 'blood_type']
    ordering_fields = ['blood_type', 'last_updated']
    
    def get_queryset(self):
        queryset = BloodInventory.objects.all()
        
        # Filtre par statut (low, critical, good)
        status_filter = self.request.query_params.get('status')
        if status_filter:
            # Convertir la liste en mémoire pour filtrer par propriété
            return [item for item in queryset if item.status == status_filter.lower()]
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Résumé des stocks de sang par groupe sanguin"""
        summary = BloodInventory.objects.values('blood_type').annotate(
            total_ml=Sum('quantity_ml'),
            center_count=Sum('center__is_active')
        ).order_by('blood_type')
        
        # Calculer le statut global pour chaque groupe sanguin
        result = []
        for item in summary:
            # Logique simplifiée pour déterminer le statut global
            if item['total_ml'] == 0:
                status = 'critical'
            elif item['total_ml'] < (1000 * item['center_count'] * 0.3):  # Moins de 30% du minimum souhaité
                status = 'low'
            elif item['total_ml'] < (1000 * item['center_count']):  # Moins que le minimum souhaité
                status = 'warning'
            else:
                status = 'good'
                
            result.append({
                'blood_type': item['blood_type'],
                'total_ml': item['total_ml'],
                'status': status,
                'center_count': item['center_count']
            })
            
        return Response(result)

class BloodDonationViewSet(viewsets.ModelViewSet):
    serializer_class = BloodDonationSerializer
    permission_classes = [permissions.IsAuthenticated & (IsMedecin | IsInfirmier | IsAdminUser)]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['donation_center', 'donor_blood_type', 'is_processed']
    ordering_fields = ['-donation_date', 'created_at']
    
    def get_queryset(self):
        user = self.request.user
        queryset = BloodDonation.objects.all()
        
        # Les médecins et infirmiers ne voient que les dons de leur établissement
        if hasattr(user, 'hopital'):
            queryset = queryset.filter(donation_center__name=user.hopital)
            
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """Marquer un don comme traité et mettre à jour l'inventaire"""
        donation = self.get_object()
        
        if donation.is_processed:
            return Response(
                {"error": "Ce don a déjà été traité"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        donation.is_processed = True
        donation.save()
        
        # La méthode save() mettra à jour automatiquement l'inventaire
        # grâce à la méthode save() surchargée du modèle
        
        return Response({"status": "Don traité avec succès"})
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques sur les dons de sang"""
        from django.db.models import Count, Sum, Avg
        from django.utils import timezone
        from datetime import timedelta
        
        # Dons par groupe sanguin
        by_blood_type = BloodDonation.objects.values('donor_blood_type').annotate(
            count=Count('id'),
            total_ml=Sum('quantity_ml')
        ).order_by('-total_ml')
        
        # Dons des 30 derniers jours
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_donations = BloodDonation.objects.filter(
            donation_date__gte=thirty_days_ago,
            is_processed=True
        )
        
        # Statistiques mensuelles
        monthly_stats = recent_donations.extra({
            'month': "date_trunc('month', donation_date)"
        }).values('month').annotate(
            count=Count('id'),
            total_ml=Sum('quantity_ml')
        ).order_by('month')
        
        return Response({
            'by_blood_type': list(by_blood_type),
            'monthly_stats': list(monthly_stats),
            'total_donations': recent_donations.count(),
            'total_ml': recent_donations.aggregate(Sum('quantity_ml'))['quantity_ml__sum'] or 0,
            'avg_donation_ml': recent_donations.aggregate(Avg('quantity_ml'))['quantity_ml__avg'] or 0
        })
