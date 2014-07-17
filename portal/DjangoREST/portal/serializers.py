from rest_framework import serializers
from portal.models import SensorData


class SensorDataSerializer(serializers.Serializer):
    #sensor = serializers.IntegerField()
    timestamp = serializers.DateTimeField(format=None, input_formats=None)
    value = serializers.IntegerField()


    def restore_object(self, attrs, instance=None):
        if instance:
            # Update existing instance
            #instance.sensor = attrs.get('sensor', instance.sensor)
            instance.timestamp = attrs.get('timestamp', instance.timestamp)
            instance.value = attrs.get('value', instance.value)
            return instance

        # Create new instance
        return SensorData(**attrs)
