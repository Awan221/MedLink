from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import BloodBankCenter, BloodStock, BloodDonation, BloodRequest

class BloodBankCenterSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)
    
    class Meta:
        model = BloodBankCenter
        fields = ['id', 'name', 'address', 'region', 'phone', 'email', 
                 'location', 'latitude', 'longitude', 'opening_hours', 
                 'manager', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Inclure les coordonnées dans un format standard
        if instance.location:
            representation['location'] = {
                'type': 'Point',
                'coordinates': [instance.location.x, instance.location.y]
            }
            representation['latitude'] = instance.location.y
            representation['longitude'] = instance.location.x
        else:
            # Valeurs par défaut pour Dakar
            representation['location'] = {
                'type': 'Point',
                'coordinates': [-17.4677, 14.7167]
            }
            representation['latitude'] = 14.7167
            representation['longitude'] = -17.4677
        return representation
        
    def create(self, validated_data):
        latitude = validated_data.pop('latitude', 14.7167)  # Dakar par défaut
        longitude = validated_data.pop('longitude', -17.4677)  # Dakar par défaut
        
        center = BloodBankCenter.objects.create(
            **validated_data,
            location=Point(float(longitude), float(latitude), srid=4326)
        )
        
        if latitude is not None and longitude is not None:
            center.location = Point(longitude, latitude)
            center.save()
        
        return center
    
    def update(self, instance, validated_data):
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if latitude is not None and longitude is not None:
            instance.location = Point(longitude, latitude)
        
        instance.save()
        return instance

class BloodStockSerializer(serializers.ModelSerializer):
    center_name = serializers.CharField(source='center.name', read_only=True)
    
    class Meta:
        model = BloodStock
        fields = ['id', 'center', 'center_name', 'blood_group', 
                 'units_available', 'last_updated', 'updated_by']
        read_only_fields = ['id', 'updated_by', 'last_updated']

class BloodDonationSerializer(serializers.ModelSerializer):
    center_name = serializers.CharField(source='center.name', read_only=True)
    
    class Meta:
        model = BloodDonation
        fields = ['id', 'center', 'center_name', 'donor_name', 
                 'donor_email', 'donor_phone', 'blood_group', 
                 'donation_date', 'status', 'created_at', 
                 'updated_at', 'completed_by']
        read_only_fields = ['id', 'created_at', 'updated_at', 'completed_by']

class BloodRequestSerializer(serializers.ModelSerializer):
    center_name = serializers.CharField(source='center.name', read_only=True)
    requesting_doctor_name = serializers.CharField(source='requesting_doctor.full_name', read_only=True)
    
    class Meta:
        model = BloodRequest
        fields = ['id', 'center', 'center_name', 'requesting_doctor', 
                 'requesting_doctor_name', 'blood_group', 'units_requested', 
                 'priority', 'patient_name', 'reason', 'status', 
                 'created_at', 'updated_at', 'approved_by', 'fulfilled_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'approved_by', 'fulfilled_at']