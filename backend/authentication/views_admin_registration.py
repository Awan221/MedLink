from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import UserRegistrationRequest
from .serializers import UserRegistrationRequestAdminSerializer
from .email_utils import send_admin_notification

class UserRegistrationRequestListView(generics.ListAPIView):
    queryset = UserRegistrationRequest.objects.all()
    serializer_class = UserRegistrationRequestAdminSerializer
    permission_classes = [IsAdminUser]

class UserRegistrationRequestDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserRegistrationRequest.objects.all()
    serializer_class = UserRegistrationRequestAdminSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Notifier l'administrateur du changement de statut
        if 'status' in request.data:
            status_message = f"La demande d'inscription de {instance.first_name} {instance.last_name} a été {request.data['status'].lower()}."
            send_admin_notification(
                subject='Mise à jour du statut de la demande d\'inscription',
                message=status_message
            )

        return Response(serializer.data)

class UserRegistrationRequestStatsView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total = UserRegistrationRequest.objects.count()
        pending = UserRegistrationRequest.objects.filter(status='PENDING').count()
        approved = UserRegistrationRequest.objects.filter(status='APPROVED').count()
        rejected = UserRegistrationRequest.objects.filter(status='REJECTED').count()

        return Response({
            'total': total,
            'pending': pending,
            'approved': approved,
            'rejected': rejected
        })
