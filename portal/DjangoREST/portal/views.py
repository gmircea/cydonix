from django.http import HttpResponse
from django.utils.timezone import utc
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from portal.models import Sensors, SensorData
from portal.serializers import SensorDataSerializer
import datetime


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def sensor_value_list(request, sensor_type_name):
    begin = request.GET.get('begin')
    end = request.GET.get('end')
    offset = request.GET.get('offset')
    count = request.GET.get('count')

    begin = iso8601_to_datetime(begin)
    end = iso8601_to_datetime(end)

    if request.method == 'GET':
        sensor_type = Sensors.objects.get(sensor_type=sensor_type_name).id
        sensor_data = SensorData.objects.filter(sensor_id=sensor_type, timestamp__gte=begin,
                                                timestamp__lte=end)[offset:offset+count]
        sensor_data = datetime_to_iso8601(sensor_data)
        serializer = SensorDataSerializer(sensor_data, many=True)
        return serializer


def iso8601_to_datetime(datetime_string):
    # From YYYYMMDDTHHMMSSZ to datetime
    dt = datetime.datetime.strptime(datetime_string, "%Y%m%dT%H%M%SZ").replace(tzinfo=utc)
    return dt


def datetime_to_iso8601(sensor_data):
    # From datetime to YYYYMMDDTHHMMSSZ
    size = len(sensor_data)
    for i in range(0, size):
        #utc_time = sensor_data[i].timestamp.strftime("%Y%m%dT%H%M%SZ")
        sensor_data[i].timestamp = sensor_data[i].timestamp.strftime("%Y%m%dT%H%M%SZ")
    return sensor_data


@csrf_exempt
def sensor_data_list(request):
    if request.method == 'GET':
        sensor_data = SensorData.objects.all()
        sensor_data = datetime_to_iso8601(sensor_data)
        serializer = SensorDataSerializer(sensor_data, many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
def temperature_list(request):
    serializer = sensor_value_list(request, 'temperature')
    return JSONResponse(serializer.data)


@csrf_exempt
def pressure_list(request):
    serializer = sensor_value_list(request, 'pressure')
    return JSONResponse(serializer.data)


@csrf_exempt
def altitude_list(request):
    serializer = sensor_value_list(request, 'altitude')
    return JSONResponse(serializer.data)


@csrf_exempt
def switch_list(request):
    serializer = sensor_value_list(request, 'switch')
    return JSONResponse(serializer.data)


@csrf_exempt
def soc_temp_list(request):
    serializer = sensor_value_list(request, 'soc_temp')
    return JSONResponse(serializer.data)


@csrf_exempt
def arm_freq_list(request):
    serializer = sensor_value_list(request, 'arm_freq')
    return JSONResponse(serializer.data)


@csrf_exempt
def core_freq_list(request):
    serializer = sensor_value_list(request, 'core_freq')
    return JSONResponse(serializer.data)


@csrf_exempt
def core_volt_list(request):
    serializer = sensor_value_list(request, 'core_volt')
    return JSONResponse(serializer.data)


@csrf_exempt
def sdram_volt_list(request):
    serializer = sensor_value_list(request, 'sdram_volt')
    return JSONResponse(serializer.data)
