#!/usr/bin/env python
# -*- coding:utf-8 -*-

from echobot_module import *
from pubsub_module import *
from option_parser_module import *
from gpio_pubsub_module import *
from multiprocessing import Process



def echobot():
    echo = XmppClass(opts.jid, opts.password)
    if echo.connect():
        echo.process(block=True)
        print("Ok")
    else :
        print("Nu se poate conecta")

def pubsub():
    psgp = PubsubGpio(opts.jid,opts.password,opts.pubsub_server,opts.node)
    psgp.notify()

echo_process = Process(target=echobot)
pubsub_process = Process(target=pubsub)

echo_process.start()
pubsub_process.start()

echo_process.join()
pubsub_process.join()
