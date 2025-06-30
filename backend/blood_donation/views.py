from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import BloodCenter, BloodDonationAlert
from .serializers import BloodCenterSerializer, BloodDonationAlertSerializer

class BloodCenterViewSet(viewsets.ModelViewSet):
    queryset = BloodCenter.objects.all()
    serializer_class = BloodCenterSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        radius = request.query_params.get('radius', 10)  # Rayon en km par défaut

        if not latitude or not longitude:
            return Response(
                {'error': 'Latitude et longitude requises'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculer les centres à proximité
        centers = BloodCenter.objects.all()
        nearby_centers = []
        
        for center in centers:
            distance = self.calculate_distance(
                float(latitude),
                float(longitude),
                center.latitude,
                center.longitude
            )
            
            if distance <= float(radius):
                center_data = self.get_serializer(center).data
                center_data['distance'] = round(distance, 1)
                nearby_centers.append(center_data)

        return Response(nearby_centers)

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371  # Rayon de la Terre en km

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c

        return distance

class BloodDonationAlertViewSet(viewsets.ModelViewSet):
    serializer_class = BloodDonationAlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BloodDonationAlert.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        center_id = request.data.get('centerId')
        
        try:
            center = BloodCenter.objects.get(id=center_id)
        except BloodCenter.DoesNotExist:
            return Response(
                {'error': 'Centre de don non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )

        alert, created = BloodDonationAlert.objects.get_or_create(
            user=request.user,
            center=center,
            defaults={'is_active': True}
        )

        if not created:
            alert.is_active = True
            alert.save()

        return Response(
            self.get_serializer(alert).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk=None):
        try:
            alert = self.get_object()
            alert.is_active = False
            alert.save()
            return Response({'status': 'unsubscribed'})
        except BloodDonationAlert.DoesNotExist:
            return Response(
                {'error': 'Alerte non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            ) 