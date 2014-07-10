#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import sleekxmpp
from gpio_module import *

rgpio=Raspberry_GPIO()

if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else :
    raw_input = input

class XmppClass(sleekxmpp.ClientXMPP):
    def __init__(self,jid,password):

        super(XmppClass,self).__init__(jid,password)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0004')
        self.register_plugin('xep_0060')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0059')

        self.add_event_handler('session_start',self.start)
        self.add_event_handler('message',self.message)

    def start(self,event):
        self.send_presence()
        self.get_roster()

    def message(self,msg):
        if msg['type'] in ('normal','chat'):
            if msg['body']=="aprinde bec":
                rgpio.turn_on_light()
                msg.reply("Lights on!").send()
            elif msg['body']=="stinge bec":
                rgpio.turn_off_light()
                msg.reply("Lights off!").send()
            elif msg['body']=="get data":
                temperature,pressure,altitude,press_sealevel=rgpio.get_bmp_data()
                pressure=round(pressure,2)
                altitude=round(altitude,2)
                press_sealevel=round(press_sealevel,2)
                bmp_values=str(temperature)+ ' '+str(pressure)+' '+ str(
                               altitude)+' '+str(press_sealevel)
                msg.reply(bmp_values).send()
            elif msg['body']=="get pi state":
                temp_cpu,temp_v,arm_speed,core_speed,mem_speed,arm_mem,gpu_mem=rgpio.get_rpi_data()
                valori_cpu=str(temp_cpu)+ ' ' + str(temp_v)+ ' ' + str(arm_speed
                               ) + ' ' + str(core_speed) + ' ' + str(mem_speed
                               )+' ' + str(arm_mem) + ' ' + str(gpu_mem)
                msg.reply(valori_cpu).send()
