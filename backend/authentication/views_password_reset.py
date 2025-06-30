from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class PasswordResetRequestView(APIView):
    """
    Vue pour demander une réinitialisation de mot de passe.
    Envoie un email avec un lien de réinitialisation.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response(
                {'error': 'Email is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Ne pas révéler si l'email existe ou pas pour des raisons de sécurité
            return Response(
                {'message': 'If this email exists in our system, you will receive a password reset link.'},
                status=status.HTTP_200_OK
            )
        
        # Générer un token de réinitialisation
        refresh = RefreshToken.for_user(user)
        reset_token = str(refresh.access_token)
        
        # Construire l'URL de réinitialisation (à adapter selon votre frontend)
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}&email={email}"
        
        # Envoyer l'email (à personnaliser selon vos besoins)
        subject = 'Réinitialisation de votre mot de passe'
        message = f'''
        Bonjour {user.get_full_name() or 'utilisateur'},
        
        Vous avez demandé la réinitialisation de votre mot de passe. 
        Veuillez cliquer sur le lien ci-dessous pour définir un nouveau mot de passe :
        
        {reset_url}
        
        Si vous n'avez pas demandé cette réinitialisation, veuillez ignorer cet email.
        
        Cordialement,
        L'équipe MedLink
        '''
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            return Response(
                {'message': 'If this email exists in our system, you will receive a password reset link.'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to send email: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PasswordResetConfirmView(APIView):
    """
    Vue pour confirmer la réinitialisation du mot de passe avec un token valide.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        
        if not all([token, email, new_password]):
            return Response(
                {'error': 'Token, email and new_password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email=email)
            # Vérifier si le token est valide
            refresh = RefreshToken(token)
            if refresh['user_id'] != user.id:
                raise Exception('Invalid token for this user')
            
            # Mettre à jour le mot de passe
            user.set_password(new_password)
            user.save()
            
            # Invalider le token après utilisation
            refresh.blacklist()
            
            return Response(
                {'message': 'Password has been reset successfully'},
                status=status.HTTP_200_OK
            )
            
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Invalid or expired token: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
