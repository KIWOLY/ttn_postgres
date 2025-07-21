from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SensorData
from rest_framework import generics
from .serializers import SensorDataSerializer

@csrf_exempt
@require_POST
def webhook_receiver(request):
    try:
        payload = json.loads(request.body)
        device_id = payload.get('end_device_ids', {}).get('device_id', 'unknown')
        uplink_message = payload.get('uplink_message', {})
        measurements = uplink_message.get('decoded_payload', {}).get('measurements', [])
        port = uplink_message.get('f_port')
        wisdom = uplink_message.get('decoded_payload', {}).get('wisdom')

             # Extract common fields
        data = {'device_id': device_id, 'measurements': measurements, 'port': port, 'wisdom': wisdom}
        for measurement in measurements:
            name = measurement.get('name')
            value = measurement.get('value')
            if name == 'Temperature' or name == 'RawTemperature':
                data['temperature'] = value
            elif name == 'Humidity' or name == 'RawHumidity':
                data['humidity'] = value
            elif name == 'Pressure':
                data['pressure'] = value

             # Save to PostgreSQL
        SensorData.objects.create(**data)
        return HttpResponse('Success', status=200)
    except Exception as e:
        print(f"Error: {e}")
        return HttpResponse(f'Error: {e}', status=400)

class SensorDataList(generics.ListAPIView):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer

    def get_queryset(self):
        device_id = self.request.query_params.get('device_id')
        start_time = self.request.query_params.get('start_time')
        if device_id:
            self.queryset = self.queryset.filter(device_id=device_id)
        if start_time:
            self.queryset = self.queryset.filter(received_at__gte=start_time)
        return self.queryset