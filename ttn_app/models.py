from django.db import models

class SensorData(models.Model):
    device_id = models.CharField(max_length=100)
    received_at = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    pressure = models.FloatField(null=True, blank=True)
    measurements = models.JSONField(default=dict)  # Updated to use django.db.models.JSONField
    port = models.IntegerField(null=True, blank=True)  # For bme680
    wisdom = models.CharField(max_length=50, null=True, blank=True)  # For bme680

    class Meta:
        indexes = [models.Index(fields=['device_id', 'received_at'])]

    def __str__(self):
        return f"{self.device_id} - {self.received_at}"