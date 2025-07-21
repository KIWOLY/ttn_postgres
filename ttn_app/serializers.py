from rest_framework import serializers
from .models import SensorData

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = ['id', 'device_id', 'temperature', 'humidity', 'pressure', 'measurements', 'port', 'wisdom', 'received_at']