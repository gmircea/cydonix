#!/usr/bin/env python

import RPi.GPIO as GPIO
import Adafruit_BMP.BMP085 as BMP085
import commands
sensor = BMP085.BMP085(busnum=0)

class Raspberry_GPIO:
    '''  This represents a class which sets up GPIO pins,
       gets data from sensors and controls other peripherals
    '''

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.OUT)

    def get_bmp_data(self):
        temperature = sensor.read_temperature()
        pressure = sensor.read_pressure()
        altitude = sensor.read_altitude()
        press_sealevel = sensor.read_sealevel_pressure()
        return (temperature, pressure ,altitude,press_sealevel)

    def turn_on_light(self):
        GPIO.output(7,True)


    def turn_off_light(self):
        GPIO.output(7,False)


    def get_rpi_data(self):

        cpu_temp = commands.getoutput('/opt/vc/bin/vcgencmd measure_temp'
                                      ).replace( 'temp=', '').replace('\'C','')
        cpu_voltage = commands.getoutput('/opt/vc/bin/vcgencmd measure_volts'
                                         ).replace('volt=','').replace('V','')
        arm_speed = commands.getoutput('/opt/vc/bin/vcgencmd measure_clock arm'
                                       ).replace('frequency(45)=','')
        core_speed = commands.getoutput('/opt/vc/bin/vcgencmd measure_clock core'
                                        ).replace('frequency(1)=','')
        mem_speed = commands.getoutput('/opt/vc/bin/vcgencmd get_config sdram_freq'
                                       ).replace('sdram_freq=','')
        arm_mem = commands.getoutput('/opt/vc/bin/vcgencmd get_mem arm'
                                     ).replace('arm=','').replace('M','')
        gpu_mem = commands.getoutput('/opt/vc/bin/vcgencmd get_mem gpu'
                                     ).replace('gpu=','').replace('M','')

        arm_speed = float(arm_speed)
        arm_speed=arm_speed/1000000

        core_speed = float(core_speed)
        core_speed=core_speed/1000000

        return (cpu_temp,cpu_voltage,arm_speed,core_speed,mem_speed,arm_mem,
                gpu_mem)
