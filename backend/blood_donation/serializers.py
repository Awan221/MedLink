from rest_framework import serializers
from .models import BloodCenter, BloodDonationAlert

class BloodCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodCenter
        fields = [
            'id', 'name', 'address', 'latitude', 'longitude',
            'phone', 'email', 'stock_level', 'is_critical',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class BloodDonationAlertSerializer(serializers.ModelSerializer):
    center = BloodCenterSerializer(read_only=True)
    center_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BloodDonationAlert
        fields = [
            'id', 'center', 'center_id', 'is_active',
            'created_at', 'last_notification'
        ]
        read_only_fields = ['created_at', 'last_notification'] 