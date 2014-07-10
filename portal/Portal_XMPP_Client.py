__author__ = 'alex'
#import logging

from sleekxmpp import ClientXMPP

from multiprocessing import Process
import time

from datetime import datetime

import sqlite3
import re


class BotXMPP:
    def __init__(self, sender_jid, sender_password, receiver_jid, receiver_password, sensor_bot_jid):
        # Initializing sender and receiver XMPP clients
        self.sender = PortalXMPP(sender_jid, sender_password, 'sender', sensor_bot_jid)
        self.receiver = PortalXMPP(receiver_jid, receiver_password, 'receiver')

        # Connecting sender and receiver
        self.sender.connect()
        self.receiver.connect()

        # Adding receiver "message" event handler
        self.receiver.add_event_handler("message", self.receiver.receive_m)

        # Creating separate processes for sender and receiver
        self.sender_process = Process(target=self.sender.send_m)
        self.receiver_process = Process(target=self.receiver.receive_m)

        # Starting sender and receiver processes
        self.sender_process.start()
        self.receiver_process.start()

        # Starting to process incoming messages
        self.receiver.process(block=True)

        # Wait for child processes to terminate
        self.sender_process.join()
        self.receiver_process.join()


class PortalXMPP(ClientXMPP):
    def __init__(self, jid, password, name, sensor_bot_jid=''):
        ClientXMPP.__init__(self, jid, password)

        # Setting the XMPP client name
        self.name = name

        # Setting the session_start event handler to a method that prints the XMPP client's name
        self.add_event_handler("session_start", self.session_start)

        # Setting different priorities for the XMPP clients so that all messages sent to the main jid, go to 'receiver'
        if self.name == 'sender':
            self.sender_jid=jid
            self.sensor_bot_jid=sensor_bot_jid
            self.send_presence(ppriority=-1)
        elif self.name == 'receiver':
            self.send_presence(ppriority=1)

    def send_m(self):
        # Sending custom 'get' requests for sensor data
        while True:
            time.sleep(10)
            self.send_message(mto=self.sensor_bot_jid,
                              mbody='get pressure', mtype='normal', mfrom=self.sender_jid)
            self.send_message(mto=self.sensor_bot_jid,
                              mbody='get temperature', mtype='normal', mfrom=self.sender_jid)
            self.send_message(mto=self.sensor_bot_jid,
                              mbody='get altitude', mtype='normal', mfrom=self.sender_jid)
            print("Sent 'get pressure'")
            print("Sent 'get temperature'")
            print("Sent 'get altitude'")
            self.process(block=False)

    def receive_m(self, msg):
        self.connection = sqlite3.connect('DB.sqlite3')
        self.cursor = self.connection.cursor()

        print("Received '"+str(msg['body'])+"'")

        # Parsing the received message, with regular expressions
        s_sensor_type_name = re.search("([\w]+(?==))", str(msg['body'])).group(1)
        value = int(re.search("((?<==)[\w]+)", str(msg['body'])).group(1))

        print("sensor_type = '"+s_sensor_type_name+"' value = '"+str(value)+"'")

        # Fetching the id of the sensor_type with the name = s_sensor_type_name if it exists
        self.cursor.execute("SELECT id FROM portal_sensors WHERE sensor_type='"+s_sensor_type_name+"'")
        sensor_type = self.cursor.fetchone()

        if str(sensor_type) != 'None':
            sensor_type = sensor_type[0]
            commit = 1
        else:
            print("There is no sensor of type '"+s_sensor_type_name+"'")
            commit = 0

        if commit > 0:
            utc_time = datetime.utcnow().isoformat()  # UTC date and time in ISO 8601 format

            s_sensor_type = str(sensor_type)
            s_value = str(value)
            s_time = "'"+str(utc_time)+"'"

            # Determining the last id value in order to provide the next one
            self.cursor.execute("SELECT id FROM portal_sensordata ORDER BY id DESC LIMIT 1")
            last_id = self.cursor.fetchone()

            if str(last_id) != 'None':
                last_id = last_id[0]
            else:
                last_id = 0

            new_id = str(last_id+1)

            print("INSERT INTO portal_sensordata "
                  "VALUES ( "+new_id+", " + s_sensor_type + ", " + s_value + ", " + s_time+")")

            # Adding the received sensor data to the appropriate table
            self.cursor.execute("INSERT INTO portal_sensordata "
                                "VALUES ( "+new_id+", " + s_sensor_type + ", " + s_value + ", " + s_time+")")
            self.connection.commit()

            print("Commited")
        else:
            print("Nothing commited")

    def session_start(self, event):
        print("Started "+self.name)

#logging.basicConfig(level=logging.disable('INFO'),
#                    format='%(levelname)-8s %(message)s')

# Initializing the XMPP bot
xmpp = BotXMPP('bot_jid@domain/sender', 'bot_password', 'bot_jid@domain/receiver', 'bot_password', 'sensor_bot_jid@domain')
