from rest_framework import serializers
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Disease, DiseaseCategory, DiseaseResource

class PublicAppointmentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    phone = serializers.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Le numéro de téléphone doit être au format: '+999999999'."
            )
        ]
    )
    email = serializers.EmailField(required=False, allow_blank=True)
    date = serializers.DateField()
    reason = serializers.CharField(max_length=255)
    
    def validate_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("La date ne peut pas être dans le passé.")
        return value

class PublicDonorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    phone = serializers.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Le numéro de téléphone doit être au format: '+999999999'."
            )
        ]
    )
    email = serializers.EmailField(required=False, allow_blank=True)
    blood_group = serializers.ChoiceField(choices=[
        ('A+', 'A+'), ('A-', 'A-'), 
        ('B+', 'B+'), ('B-', 'B-'), 
        ('AB+', 'AB+'), ('AB-', 'AB-'), 
        ('O+', 'O+'), ('O-', 'O-')
    ])
    region = serializers.CharField(max_length=50, required=False)
    preferred_date = serializers.DateField(required=False)
    
    def validate_preferred_date(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("La date ne peut pas être dans le passé.")
        return value


class DiseaseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseCategory
        fields = ['id', 'name', 'slug', 'description', 'icon']
        read_only_fields = ['slug']


class DiseaseResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseResource
        fields = ['id', 'title', 'resource_type', 'url', 'description']


class DiseaseListSerializer(serializers.ModelSerializer):
    category = DiseaseCategorySerializer(read_only=True)
    symptoms = serializers.SerializerMethodField()
    
    class Meta:
        model = Disease
        fields = [
            'id', 'name', 'slug', 'category', 'short_description', 
            'main_symptoms', 'severity', 'is_emergency', 'symptoms'
        ]
    
    def get_symptoms(self, obj):
        # Retourne les symptômes principaux sous forme de liste
        return [s.strip() for s in obj.main_symptoms.split('\n') if s.strip()]


class DiseaseDetailSerializer(DiseaseListSerializer):
    resources = DiseaseResourceSerializer(many=True, read_only=True)
    prevention = serializers.SerializerMethodField()
    complications = serializers.SerializerMethodField()
    when_to_see_doctor = serializers.SerializerMethodField()
    
    class Meta(DiseaseListSerializer.Meta):
        fields = DiseaseListSerializer.Meta.fields + [
            'scientific_name', 'description', 'causes', 'risk_factors',
            'diagnosis', 'treatment', 'prevention', 'prevention_details',
            'when_to_see_doctor', 'prognosis', 'other_symptoms', 
            'created_at', 'updated_at', 'resources', 'complications',
            'useful_links'
        ]
    
    def get_prevention(self, obj):
        # Retourne les mesures de prévention sous forme de liste
        if not obj.prevention:
            return []
        return [p.strip() for p in obj.prevention.split('\n') if p.strip()]
    
    def get_complications(self, obj):
        # Extrait les complications du champ prognosis
        if not obj.prognosis:
            return []
        # On suppose que les complications sont listées après "Complications possibles :"
        import re
        match = re.search(r'Complications possibles[\s\:]+(.*?)(?=\n\n|$)', obj.prognosis, re.DOTALL)
        if match:
            complications = match.group(1).strip()
            return [c.strip() for c in complications.split('\n') if c.strip()]
        return []
    
    def get_when_to_see_doctor(self, obj):
        # Extrait les indications de consultation du champ prognosis
        if not obj.when_to_see_doctor:
            return []
        return [i.strip() for i in obj.when_to_see_doctor.split('\n') if i.strip() and not i.strip().startswith('-')]
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Formate les liens utiles si le champ existe
        if 'useful_links' in representation and representation['useful_links']:
            links = []
            for line in representation['useful_links'].split('\n'):
                if line.strip():
                    parts = line.split(' - ', 1)
                    if len(parts) == 2:
                        links.append({
                            'title': parts[0].strip(),
                            'url': parts[1].strip()
                        })
                    else:
                        links.append({
                            'title': line.strip(),
                            'url': '#'
                        })
            representation['useful_links'] = links
        return representation

class PublicContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Le numéro de téléphone doit être au format: '+999999999'."
            )
        ]
    )
    subject = serializers.CharField(max_length=200)
    message = serializers.CharField(max_length=1000)
