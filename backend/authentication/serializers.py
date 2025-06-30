from rest_framework import serializers
from .models import User, UserRegistrationRequest, RolePermission, SubRolePermission, Role, UserDocument
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import os
from django.db import connection
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class SubRolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubRolePermission
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class UserRegistrationRequestSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirmation = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    role = serializers.CharField(write_only=True, required=True)
    documents = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=True
    )

    class Meta:
        model = UserRegistrationRequest
        fields = [
            'email', 'password', 'password_confirmation', 'first_name', 'last_name',
            'role', 'phone', 'hopital', 'region', 'numero_licence', 'date_licence',
            'documents'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone': {'required': True},
            'hopital': {'required': True},
            'region': {'required': True},
            'numero_licence': {'required': True},
            'date_licence': {'required': True},
        }

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({"password_confirmation": "Les mots de passe ne correspondent pas."})
        return data

    def create(self, validated_data):
        # Extraire les données du formulaire
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        role = validated_data['role']
        phone = validated_data['phone']
        hopital = validated_data['hopital']
        region = validated_data['region']
        numero_licence = validated_data['numero_licence']
        date_licence = validated_data['date_licence']
        documents = validated_data['documents']

        # Créer la demande d'inscription
        request = UserRegistrationRequest.objects.create(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role,
            phone=phone,
            hopital=hopital,
            region=region,
            numero_licence=numero_licence,
            date_licence=date_licence,
            documents=documents[0] if documents else None
        )

        return request

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'phone', 'hopital', 'region', 'numero_licence', 'date_licence']
        read_only_fields = ['id']

    def get_role(self, obj):
        return obj.role.name if obj.role else None

class UserRegistrationRequestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegistrationRequest
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'phone', 'hopital', 'region', 'numero_licence', 'date_licence', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirmation = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    phone = serializers.CharField(required=True)
    hopital = serializers.CharField(required=True)
    region = serializers.CharField(required=True)
    numero_licence = serializers.CharField(required=True)
    date_licence = serializers.DateField(required=True)
    documents = serializers.ListField(
        child=serializers.FileField(),
        required=True,
        write_only=True
    )
    terms = serializers.BooleanField(required=True, write_only=True)
    specialist_type = serializers.CharField(required=False)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        source='role',
        required=False,
        write_only=True
    )
    
    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirmation', 'first_name', 'last_name',
            'role_id', 'specialist_type', 'phone', 'hopital', 'region',
            'numero_licence', 'date_licence', 'documents', 'terms'
        ]
        read_only_fields = ['id', 'is_active']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        
        if not attrs.get('terms'):
            raise serializers.ValidationError({"terms": "Vous devez accepter les conditions d'utilisation."})
        
        # Si role_id n'est pas fourni, utiliser le rôle par défaut (médecin)
        if 'role' not in attrs:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'authentication_role')")
                    table_exists = cursor.fetchone()[0]
                
                if not table_exists:
                    raise serializers.ValidationError({"role": "La table des rôles n'est pas encore créée. Veuillez contacter l'administrateur."})
                
                default_role = Role.objects.get(name='doctor')
                attrs['role'] = default_role
            except Role.DoesNotExist:
                raise serializers.ValidationError({"role": "Rôle par défaut non trouvé."})
        
        # Vérifier que specialist_type est fourni si le rôle est specialist
        role = attrs.get('role')
        if role and role.name == 'specialist' and not attrs.get('specialist_type'):
            raise serializers.ValidationError({"specialist_type": "La spécialité est requise pour un médecin spécialiste."})
        
        return attrs
    
    def create(self, validated_data):
        # Extraire les données qui ne font pas partie du modèle User
        documents = validated_data.pop('documents', [])
        password_confirmation = validated_data.pop('password_confirmation')
        terms = validated_data.pop('terms')
        specialist_type = validated_data.pop('specialist_type', None)
        
        # Créer l'utilisateur
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
            phone=validated_data['phone'],
            hopital=validated_data['hopital'],
            region=validated_data['region'],
            numero_licence=validated_data['numero_licence'],
            date_licence=validated_data['date_licence']
        )
        
        # Si un type de spécialiste est fourni, l'associer à l'utilisateur
        if specialist_type:
            try:
                specialist_type_obj = SpecialistType.objects.get(name=specialist_type)
                user.specialist_type = specialist_type_obj
                user.save()
            except SpecialistType.DoesNotExist:
                raise serializers.ValidationError({"specialist_type": "Type de spécialiste invalide."})
        
        # Sauvegarder les documents
        if documents:
            for document in documents:
                UserDocument.objects.create(
                    user=user,
                    file=document,
                    document_type='REGISTRATION'
                )
            
        return user

class UserRegistrationRequestAdminSerializer(serializers.ModelSerializer):
    documents = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = UserRegistrationRequest
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def update(self, instance, validated_data):
        if 'status' in validated_data and validated_data['status'] == UserRegistrationRequest.Status.APPROVED:
            # Créer un nouvel utilisateur
            user = User.objects.create(
                email=instance.email,
                first_name=instance.first_name,
                last_name=instance.last_name,
                role=instance.medical_role,
                is_active=True
            )
            # Générer un mot de passe temporaire
            temporary_password = User.objects.make_random_password()
            user.set_password(temporary_password)
        user.save()
            
            # Envoyer l'email de confirmation
        from .email_utils import send_registration_approved_email
        send_registration_approved_email(
            user_email=instance.email,
            user_name=f"{instance.first_name} {instance.last_name}",
            temporary_password=temporary_password
        )
        
        return super().update(instance, validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']

class ProcessRegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegistrationRequest
        fields = ['status', 'note']

    def validate(self, data):
        # Pas de vérification de mot de passe ici
        return data