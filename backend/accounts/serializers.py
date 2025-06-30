from rest_framework import serializers
from .models import User, UserDocument

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirmation = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    documents = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    specialite_display = serializers.CharField(source='get_specialite_display', read_only=True)
    region_display = serializers.CharField(source='get_region_display', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'password', 'password_confirmation', 'first_name', 'last_name',
            'role', 'role_display', 'specialite', 'specialite_display', 'telephone',
            'hopital', 'region', 'region_display', 'numero_licence', 'date_obtention',
            'documents', 'is_active', 'is_verified', 'date_joined'
        ]
        read_only_fields = ['id', 'is_active', 'is_verified', 'date_joined']

    def validate(self, data):
        if data.get('password') != data.get('password_confirmation'):
            raise serializers.ValidationError({
                "password_confirmation": "Les mots de passe ne correspondent pas."
            })
        
        # Validation spécifique pour les banques de sang
        if data.get('role') == 'BANQUE_SANG':
            if not data.get('hopital'):
                raise serializers.ValidationError({
                    "hopital": "Le nom de l'hôpital est requis pour les banques de sang."
                })
            if not data.get('region'):
                raise serializers.ValidationError({
                    "region": "La région est requise pour les banques de sang."
                })
            if not data.get('numero_licence'):
                raise serializers.ValidationError({
                    "numero_licence": "Le numéro de licence est requis pour les banques de sang."
                })
            if not data.get('date_obtention'):
                raise serializers.ValidationError({
                    "date_obtention": "La date d'obtention de la licence est requise pour les banques de sang."
                })
            if not data.get('documents'):
                raise serializers.ValidationError({
                    "documents": "Au moins un document est requis pour les banques de sang."
                })

        return data

    def create(self, validated_data):
        documents = validated_data.pop('documents', [])
        password = validated_data.pop('password')
        validated_data.pop('password_confirmation')
        
        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        # Créer les documents associés
        for doc in documents:
            UserDocument.objects.create(
                user=user,
                document_type='LICENCE',
                file=doc
            )

        return user 