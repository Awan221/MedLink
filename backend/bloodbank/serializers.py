from rest_framework import serializers
from .models import BloodDonationCenter, BloodInventory, BloodDonation
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point

class BloodDonationCenterSerializer(serializers.ModelSerializer):
    distance_km = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    
    class Meta:
        model = BloodDonationCenter
        fields = [
            'id', 'name', 'address', 'city', 'region', 'country',
            'phone', 'email', 'latitude', 'longitude', 'is_active',
            'distance_km', 'created_at', 'updated_at', 'location'
        ]
        read_only_fields = ('created_at', 'updated_at', 'distance_km')
        extra_kwargs = {
            'location': {'write_only': True}
        }
        
    def get_latitude(self, obj):
        return obj.latitude
        
    def get_longitude(self, obj):
        return obj.longitude
    
    def get_distance_km(self, obj):
        """Retourne la distance en kilomètres si une position de référence est fournie"""
        user_location = self.context.get('user_location')
        if user_location and hasattr(obj, 'distance') and obj.distance is not None:
            # Convertir la distance en kilomètres (Django renvoie la distance en mètres)
            return round(obj.distance.km, 2)
        return None

class BloodDonationCenterWithDistanceSerializer(BloodDonationCenterSerializer):
    """Sérialiseur qui inclut la distance calculée"""
    distance_km = serializers.FloatField()
    
    class Meta(BloodDonationCenterSerializer.Meta):
        fields = BloodDonationCenterSerializer.Meta.fields + ['distance_km']

class BloodInventorySerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display', read_only=True)
    center_name = serializers.CharField(source='center.name', read_only=True)
    center_city = serializers.CharField(source='center.city', read_only=True)
    
    class Meta:
        model = BloodInventory
        fields = [
            'id', 'center', 'center_name', 'center_city', 'blood_type',
            'quantity_ml', 'minimum_required_ml', 'status', 'last_updated'
        ]
        read_only_fields = ('status', 'last_updated')
    
    def validate_quantity_ml(self, value):
        if value < 0:
            raise serializers.ValidationError("La quantité ne peut pas être négative")
        return value

class BloodDonationSerializer(serializers.ModelSerializer):
    donor_name = serializers.CharField(source='donor_name', required=True)
    donor_blood_type = serializers.ChoiceField(
        choices=BloodInventory.BLOOD_TYPES,
        required=True
    )
    donation_center_name = serializers.CharField(
        source='donation_center.name', 
        read_only=True
    )
    created_by_name = serializers.CharField(
        source='created_by.get_full_name', 
        read_only=True
    )
    
    class Meta:
        model = BloodDonation
        fields = [
            'id', 'donor_name', 'donor_blood_type', 'donor_phone',
            'donation_center', 'donation_center_name', 'donation_date',
            'quantity_ml', 'is_processed', 'notes', 'created_by',
            'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ('is_processed', 'created_by', 'created_at', 'updated_at')
    
    def validate_quantity_ml(self, value):
        if value <= 0:
            raise serializers.ValidationError("La quantité doit être supérieure à zéro")
        if value > 500:  # 500ml est le don maximum standard
            raise serializers.ValidationError("La quantité ne peut pas dépasser 500ml par don")
        return value
    
    def create(self, validated_data):
        # S'assurer que l'utilisateur connecté est enregistré comme créateur
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class BloodDonationProcessSerializer(serializers.Serializer):
    """Sérialiseur pour le traitement d'un don"""
    is_processed = serializers.BooleanField(required=True)
    
    def validate(self, data):
        # Vérifier que le don n'a pas déjà été traité
        if self.instance and self.instance.is_processed and data.get('is_processed', False):
            raise serializers.ValidationError("Ce don a déjà été traité")
        return data

class BloodInventoryAlertSerializer(serializers.Serializer):
    """Sérialiseur pour les alertes de stock"""
    blood_type = serializers.CharField()
    current_ml = serializers.IntegerField()
    required_ml = serializers.IntegerField()
    status = serializers.CharField()
    centers_needed = serializers.IntegerField()
    
    def to_representation(self, instance):
        # Ajouter des informations supplémentaires pour l'affichage
        representation = super().to_representation(instance)
        representation['percent'] = round((instance['current_ml'] / instance['required_ml']) * 100, 1)
        return representation
