from django.db import models


class Sensors(models.Model):
    sensor_type = models.CharField(max_length=200)


class SensorData(models.Model):
    sensor = models.ForeignKey(Sensors)
    value = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
