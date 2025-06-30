from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import UserRegistrationRequest
from .serializers import UserRegistrationRequestSerializer
from .email_utils import send_admin_notification

from rest_framework.permissions import AllowAny

class UserRegistrationRequestCreateView(generics.CreateAPIView):
    queryset = UserRegistrationRequest.objects.all()
    serializer_class = UserRegistrationRequestSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Notifier les admins
        send_admin_notification(
            subject='Nouvelle demande d’inscription MedLink',
            message='Une nouvelle demande d’inscription vient d’être soumise et attend validation dans l’interface admin.'
        )
        headers = self.get_success_headers(serializer.data)
        return Response({'detail': 'Votre demande a été enregistrée et sera validée par un administrateur.'}, status=status.HTTP_201_CREATED, headers=headers)
