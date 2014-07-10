#!/usr/bin/env python
# -*- coding:utf-8 -*-

from gpio_module import *
from pubsub_module import *
import time
gpio_obj = Raspberry_GPIO()

class PubsubGpio:

    def __init__(self,jid,password,pubsub_server,node):
        self.jid=jid
        self.password=password
        self.pubsub_server=pubsub_server
        self.node=node

    def notify(self):
        temp_t = press_t = alt_t = press_sl_t = 0
        while True:
            time.sleep(1)
            temperature,pressure,altitude,press_sealevel=gpio_obj.get_bmp_data()
            print "\n **********  Old values **********"
            print str(temp_t)+ ' '+str(press_t)+' '+ str(
                               alt_t)+' '+str(press_sl_t)
            print "\n ********** New values ********** "
            print str(temperature)+ ' '+str(pressure)+' '+ str(
                              altitude)+' '+str(press_sealevel)
            if ((temperature >= temp_t+0.1 or temperature <= temp_t-0.1)
                or  (pressure>=press_t+10 or pressure <= press_t-10) or
                (altitude >= alt_t+1 or altitude <= alt_t-1)) :
                pubsub_obj = PubsubClass(self.jid, self.password,
                                         self.pubsub_server,self.node,
                                         'publish',"Date modificate!")
                print "\n **********  Old values **********"
                print str(temp_t)+ ' '+str(press_t)+' '+ str(
                                   alt_t)+' '+str(press_sl_t)
                print "\n ********** New values ********** "
                print str(temperature)+ ' '+str(pressure)+' '+ str(
                                  altitude)+' '+str(press_sealevel)
                if pubsub_obj.connect() :
                    pubsub_obj.process(block=True)
                else :
                    print "Unable to connect."
            temp_t = temperature
            press_t = pressure
            alt_t = altitude
            press_sl_t = press_sealevel

