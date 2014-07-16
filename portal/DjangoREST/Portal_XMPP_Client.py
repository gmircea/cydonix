__author__ = 'alex'
import logging

from sleekxmpp import ClientXMPP

from datetime import datetime

import sqlite3
import re

import threading

import ConfigParser
from optparse import OptionParser
import sys
import os


class PortalXMPP(ClientXMPP):
    def __init__(self, jid, password, sensor_bot_jid, sqlite3_DB_path, polling):
        ClientXMPP.__init__(self, jid, password)

        # Setting the sender jid and the receiver jid
        self.sender_jid = jid
        self.sensor_bot_jid = sensor_bot_jid

        # The path to the sqlite3 database
        self.DB_path = sqlite3_DB_path

        # The sensor value polling interval in seconds
        self.polling = polling

        # Setting the session_start event handler to a method that prints "Started" at session start
        self.add_event_handler("session_start", self.session_start)

        # Connecting bot
        self.connect()

        # Sending bot presence
        self.send_presence()

        # Adding "message" event handler
        self.add_event_handler("message", self.receive_m)

        try:
            # Creating and starting first send thread
            t = threading.Timer(1, self.send_m)
            t.start()

            # Starting to process incoming messages
            self.process(block=True)

        except KeyboardInterrupt:
            self.send_thread.cancel()

    def send_m(self):
        self.connection = sqlite3.connect(self.DB_path)
        self.cursor = self.connection.cursor()

        self.cursor.execute("SELECT sensor_type FROM portal_sensors")
        sensor_types = self.cursor.fetchall()

        s = ''

        for s_type in sensor_types:
            str_s_type = str(s_type[0])
            s += str_s_type+' '

        s = s.strip()

        # Sending custom 'get' requests for sensor data
        self.send_message(mto=self.sensor_bot_jid,
                          mbody='GET '+s, mtype='normal', mfrom=self.sender_jid)

        print("Sent 'GET "+s+"'")
        self.process(block=False)

        try:
            # Creating and starting the next send thread before the current one terminates
            self.send_thread = threading.Timer(self.polling, self.send_m)
            self.send_thread.start()
        except KeyboardInterrupt:
            self.send_thread.cancel()

    def receive_m(self, msg):
        self.connection = sqlite3.connect(self.DB_path)
        self.cursor = self.connection.cursor()

        print("Received '"+str(msg['body'])+"'")

        # Parsing the received message, with regular expressions
        s_sensor_type_names = re.split(' ', str(msg['body']))

        for s_sensor_type_name_item in s_sensor_type_names:
            s_sensor_type_name = re.search("([\w]+(?==))", s_sensor_type_name_item).group(1)
            re_value = re.search("((?<==)[\w]+)", s_sensor_type_name_item).group(1)
            if re_value == 'True':
                value = 1
            elif re_value == 'False':
                value = 0
            else:
                value = float(re_value)

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
                utc_time = datetime.utcnow().isoformat(' ')  # UTC date and time in ISO 8601 format

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
                print("Not commited")

    def session_start(self, event):
        print("Started")



# Setting up the command line arguments
optp = OptionParser()

optp.add_option('-c', '--config=FILE', dest="conf_file", help='configuration FILE')
optp.add_option('-d', '--debug', help='set logging to DEBUG', action='store_const',
                dest='loglevel', const=logging.DEBUG, default=logging.disable('INFO'))
optp.add_option('-l', '--log=FILE', dest="log_file", help='log messages to FILE')

opts, args = optp.parse_args()

logging.basicConfig(level = opts.loglevel,
					format = '%(levelname)-8s %(message)s', filename='log.txt', filemode='a')

# If configuration file does not exist the script will terminate
if not (os.path.isfile(str(opts.conf_file))):
    print "The configuration file does not exist"
    sys.exit()

# Reading data from the configuration file
conf = ConfigParser.ConfigParser()
conf.read(opts.conf_file)

sender_jid = conf.get("XMPP", "sender_jid")
sender_pass = conf.get("XMPP", "sender_pass")
receiver_jid = conf.get("XMPP", "receiver_jid")
sqlite3_DB_path = conf.get("XMPP", "sqlite3_DB_path")
polling = int(conf.get("XMPP", "polling"))

# Initializing the XMPP bot
xmpp = PortalXMPP(sender_jid, sender_pass, receiver_jid, sqlite3_DB_path, polling)