from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from authentication.models import UserRegistrationRequest, User
from blood_donation.models import BloodDonationAlert
from ai_diagnostic.models import AIAlert
from django.utils import timezone
from datetime import timedelta

class AdminRecentActivityView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 5 dernières inscriptions
        recent_registrations = UserRegistrationRequest.objects.order_by('-created_at')[:5]
        # 5 derniers utilisateurs activés
        recent_users = User.objects.filter(is_active=True).order_by('-date_joined')[:5]
        # Formatage simple
        registrations = [
            {
                'id': r.id,
                'email': r.email,
                'status': r.status,
                'created_at': r.created_at,
                'first_name': r.first_name,
                'last_name': r.last_name,
            } for r in recent_registrations
        ]
        users = [
            {
                'id': u.id,
                'email': u.email,
                'role': u.role.name if u.role else None,
                'date_joined': u.date_joined,
                'first_name': u.first_name,
                'last_name': u.last_name,
            } for u in recent_users
        ]
        return Response({
            'recent_registrations': registrations,
            'recent_users': users
        })

class AdminAlertsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 5 dernières alertes de don du sang
        blood_alerts = BloodDonationAlert.objects.order_by('-created_at')[:5]
        # 5 dernières alertes IA
        ai_alerts = AIAlert.objects.order_by('-created_at')[:5]
        alerts = []
        for alert in blood_alerts:
            alerts.append({
                'type': 'blood',
                'id': alert.id,
                'message': alert.message,
                'created_at': alert.created_at,
                'status': alert.status,
            })
        for alert in ai_alerts:
            alerts.append({
                'type': 'ai',
                'id': alert.id,
                'message': getattr(alert, 'message', ''),
                'created_at': alert.created_at,
                'status': getattr(alert, 'status', ''),
            })
        # Trie les alertes par date (desc)
        alerts = sorted(alerts, key=lambda x: x['created_at'], reverse=True)[:5]
        return Response({'alerts': alerts})
