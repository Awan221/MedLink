from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, logout
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from .models import User, UserRegistrationRequest, RolePermission, SubRolePermission, Role
from .serializers import (
    UserSerializer, UserRegistrationSerializer, 
    UserRegistrationRequestSerializer, LoginSerializer,
    RolePermissionSerializer, SubRolePermissionSerializer,
    RoleSerializer,
    UserRegistrationRequestAdminSerializer,
    ProcessRegistrationRequestSerializer
)
from .permissions import IsAdmin, IsSuperAdmin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.mail import send_mail
from django.conf import settings

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Créer une demande d'inscription avec les informations de l'utilisateur
        # Assurez-vous que user.role est bien une instance du modèle Role avant de l'assigner
        registration_request = UserRegistrationRequest.objects.create(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            role=user.role,  # user.role est déjà l'instance du modèle Role ici
            status='pending'
        )
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"detail": "Demande d'inscription créée avec succès. Veuillez attendre la validation par un administrateur."},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            request,
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        
        if user is None:
            return Response(
                {"detail": "Email ou mot de passe incorrect."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active or user.status != 'ACTIF':
            return Response(
                {"detail": "Ce compte n'est pas actif ou en attente de validation."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Mettre à jour la dernière connexion
        user.last_login = timezone.now()
        user.save()
        
        # Générer les tokens
        refresh = RefreshToken.for_user(user)
        
        # Obtenir le token CSRF
        csrf_token = get_token(request)
        
        response = Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })
        
        # Définir les cookies de session sécurisés
        response.set_cookie(
            key='csrftoken',
            value=csrf_token,
            httponly=True,
            samesite='Lax',
            secure=settings.CSRF_COOKIE_SECURE
        )
        
        return response

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            # Blacklist le refresh token
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            # Déconnecter l'utilisateur
            logout(request)
            
            # Créer une réponse de succès
            response = Response(
                {"detail": "Déconnexion réussie."},
                status=status.HTTP_205_RESET_CONTENT
            )
            
            # Supprimer les cookies
            response.delete_cookie('csrftoken')
            response.delete_cookie('sessionid')
            
            return response
            
        except Exception as e:
            return Response(
                {"detail": "Erreur lors de la déconnexion."},
                status=status.HTTP_400_BAD_REQUEST
            )

class RolePermissionListView(generics.ListCreateAPIView):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsSuperAdmin]

class RolePermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsSuperAdmin]

class SubRolePermissionListView(generics.ListCreateAPIView):
    queryset = SubRolePermission.objects.all()
    serializer_class = SubRolePermissionSerializer
    permission_classes = [IsSuperAdmin]

class SubRolePermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubRolePermission.objects.all()
    serializer_class = SubRolePermissionSerializer
    permission_classes = [IsSuperAdmin]

class PermissionCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        module = request.data.get('module')
        action = request.data.get('action')
        
        if not module or not action:
            return Response(
                {"detail": "Module et action requis."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier les permissions au niveau du rôle
        role_permission = RolePermission.objects.filter(
            role=request.user.role,
            module=module,
            action=action
        ).first()
        
        if role_permission and role_permission.is_allowed:
            return Response({"allowed": True})
        
        # Vérifier les permissions au niveau du sous-rôle
        sub_role_permission = SubRolePermission.objects.filter(
            role=request.user.role,
            sub_role=request.user.sub_role,
            module=module,
            action=action
        ).first()
        
        if sub_role_permission and sub_role_permission.is_allowed:
            return Response({"allowed": True})
        
        return Response({"allowed": False})

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filterset_fields = ['role', 'is_active', 'region']
    search_fields = ['email', 'first_name', 'last_name', 'hospital']
    ordering_fields = ['last_name', 'first_name', 'date_joined']

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class PendingRegistrationRequestsView(generics.ListAPIView):
    serializer_class = UserRegistrationRequestAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = UserRegistrationRequest.objects.filter(status='pending')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = [
            {
                'id': obj.id,
                'email': obj.email,
                'first_name': obj.first_name,
                'last_name': obj.last_name,
                'role': str(obj.role) if obj.role else '',
                'specialite': getattr(obj, 'specialite', ''),
                'phone': getattr(obj, 'phone', ''),
                'hopital': getattr(obj, 'hopital', ''),
                'region': getattr(obj, 'region', ''),
                'numero_licence': getattr(obj, 'numero_licence', ''),
                'date_licence': obj.date_licence.isoformat() if getattr(obj, 'date_licence', None) else '',
                'justificatif': obj.justificatif.url if getattr(obj, 'justificatif', None) else '',
                'created_at': obj.created_at.isoformat() if obj.created_at else '',
                'updated_at': obj.updated_at.isoformat() if getattr(obj, 'updated_at', None) else '',
                'status': obj.status,
                # Ajoute d'autres champs personnalisés ici selon le modèle
            }
            for obj in queryset
        ]
        return Response(data)

class ProcessRegistrationRequestView(generics.UpdateAPIView):
    queryset = UserRegistrationRequest.objects.all()
    serializer_class = ProcessRegistrationRequestSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Met à jour le status et la note sur l'instance
        instance.status = serializer.validated_data.get('status', instance.status)
        instance.note = serializer.validated_data.get('note', instance.note)
        instance.save()
        
        if serializer.validated_data.get('status') == 'approved':
            # Vérifie que le rôle existe
            role_obj = Role.objects.filter(name__iexact=instance.role).first()
            if not role_obj:
                return Response({"detail": f"Le rôle '{instance.role}' n'existe pas dans la table Role."}, status=400)
            # Créer un nouvel utilisateur
            user = User.objects.create(
                email=instance.email,
                username=instance.email,  # username obligatoire, on prend l'email
                first_name=instance.first_name,
                last_name=instance.last_name,
                role=role_obj,
                phone=instance.phone,
                hopital=instance.hopital,
                region=instance.region,
                numero_licence=instance.numero_licence,
                date_licence=instance.date_licence,
                is_active=True
            )
            # Définir le mot de passe
            user.set_password(instance.password)
            user.save()
            
            # Envoyer l'email de confirmation
            from .email_utils import send_registration_approved_email
            send_registration_approved_email(
                user_email=instance.email,
                user_name=f"{instance.first_name} {instance.last_name}",
                temporary_password=instance.password
            )
        
        self.perform_update(serializer)
        return Response(serializer.data)

class ManageRolesView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperAdmin]
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Seul le Super Admin peut modifier les rôles
        if not request.user.role == 'SUPER_ADMIN':
            return Response(
                {"detail": "Vous n'avez pas les permissions nécessaires pour cette action."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().partial_update(request, *args, **kwargs)

class RoleListView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Role.objects.exclude(name='SUPER_ADMIN')

class UserRegistrationRequestView(generics.CreateAPIView):
    queryset = UserRegistrationRequest.objects.all()
    serializer_class = UserRegistrationRequestSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        print("Données reçues:", request.data)  # Log des données reçues
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Erreurs de validation:", serializer.errors)  # Log des erreurs
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            self.perform_create(serializer)
            # Envoyer un email de confirmation
            send_mail(
                'Demande d\'inscription reçue',
                'Votre demande d\'inscription a été reçue et est en cours d\'examen.',
                settings.DEFAULT_FROM_EMAIL,
                [serializer.data['email']],
                fail_silently=False,
            )
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print("Erreur lors de la création:", str(e))  # Log des erreurs
            return Response(
                {"detail": f"Une erreur est survenue lors de l'inscription: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ValidateRegistrationRequestView(generics.UpdateAPIView):
    queryset = UserRegistrationRequest.objects.all()
    serializer_class = UserRegistrationRequestSerializer
    permission_classes = [IsAdmin]

    def perform_update(self, serializer):
        registration_request = serializer.save(status='APPROVED')
        # Créer l'utilisateur
        user = User.objects.create_user(
            email=registration_request.email,
            password=registration_request.password,
            first_name=registration_request.first_name,
            last_name=registration_request.last_name,
            role=registration_request.role,
            status='ACTIF'
        )
        # Envoyer un email de validation
        send_mail(
            'Votre compte a été validé',
            'Votre demande d\'inscription a été approuvée. Vous pouvez maintenant vous connecter.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )