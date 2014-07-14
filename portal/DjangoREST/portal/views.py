from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from portal.models import Sensors, SensorData
from portal.serializers import SensorDataSerializer
import iso8601
import re


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

    # From YYYYMMDDTHHMMSSZ to YYYY-MM-DDTHH:MM:SSZ
    begin_re = re.search("(\d\d\d\d)(\d\d)(\d\d)(T)(\d\d)(\d\d)(\d\d)(Z)", begin)
    begin = str(begin_re.group(1))+"-"+str(begin_re.group(2))+"-"+str(begin_re.group(3))+str(begin_re.group(4)) +\
        str(begin_re.group(5))+":"+str(begin_re.group(6))+":"+str(begin_re.group(7))

    end_re = re.search("(\d\d\d\d)(\d\d)(\d\d)(T)(\d\d)(\d\d)(\d\d)(Z)", end)
    end = str(end_re.group(1))+"-"+str(end_re.group(2))+"-"+str(end_re.group(3))+str(end_re.group(4)) +\
        str(end_re.group(5))+":"+str(end_re.group(6))+":"+str(end_re.group(7))

    if request.method == 'GET':
        sensor_type = Sensors.objects.get(sensor_type=sensor_type_name).id
        sensor_data = SensorData.objects.filter(sensor_id=sensor_type, timestamp__gte=iso8601.parse_date(begin),
                                                timestamp__lte=iso8601.parse_date(end))[offset:offset+count]
        sensor_data = iso8601_formatter(sensor_data)
        serializer = SensorDataSerializer(sensor_data, many=True)
        return serializer


def iso8601_formatter(sensor_data):
    # From YYYY-MM-DDTHH:MM:SSZ to YYYYMMDDTHHMMSSZ
    size = len(sensor_data)
    for i in range(0, size):
        utc_time = sensor_data[i].timestamp
        utc_time = re.split('\.', str(utc_time))[0]
        utc_time = re.split('-', utc_time)
        utc_time = "".join(utc_time)
        utc_time = re.split(':', utc_time)
        utc_time = "".join(utc_time)
        utc_time = re.split(' ', utc_time)
        utc_time[0] += "T"
        utc_time[1] += "Z"
        utc_time = "".join(utc_time)
        sensor_data[i].timestamp = utc_time
    return sensor_data


@csrf_exempt
def sensor_data_list(request):
    if request.method == 'GET':
        sensor_data = SensorData.objects.all()
        sensor_data = iso8601_formatter(sensor_data)
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
