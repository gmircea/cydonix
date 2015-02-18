from optparse import OptionParser
from sleekxmpp import ClientXMPP

import ConfigParser
import logging
import os
import sys
import threading


if sys.version_info < (3, 0) :
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input

class Workflow(ClientXMPP):
    def __init__(self, jid, password, sensor_bot_jid, pubsub_server_jid, node, trigger, action):
        ClientXMPP.__init__(self, jid, password)

        # Setting the sender jid and the receiver jid
        self.sender_jid = jid
        self.sensor_bot_jid = sensor_bot_jid
        self.trigger = trigger
        self.action = action
        self.stopped = threading.Event()
        self.action_thread = None

        # Setting the session_start event handler to a method that prints "Started" at session start
        self.add_event_handler("session_start", self.session_start)

        self.register_plugin('xep_0060')
        self.node = node
        self.pubsub_server = pubsub_server_jid
        self.add_event_handler('pubsub_publish', self._publish)

        try:
            # Connecting bot
            self.connect()

            # Sending bot presence
            self.send_presence()

            self.subscribe()

            # Starting to process incoming messages
            self.process(block=False)

        except KeyboardInterrupt:
            self.send_thread.cancel()

    def session_start(self, event):
        print("Started")

    def subscribe(self):
        try:
            result = self['xep_0060'].subscribe(self.pubsub_server, self.node, bare=False)
            print(result)
            print('Subscribed %s to node %s' % (self.boundjid.bare, self.node))
        except:
            logging.error('Could not subscribe %s to node %s' % (self.boundjid.bare, self.node))

    def _publish(self, msg):
        try:
            result = msg.xml.iter("{test}test").next().text
        except:
            logging.error('Could not retrieve test tag from message ' % (msg))
            return 

        results = result.split(" ")
        for result in results:
            print result
            result = result.split("=")
            received = {'label': result[0], 'value': result[1]}

            if received['label'] == self.trigger['start']['label']:
                if eval(received['value'] + self.trigger['start']['op'] + self.trigger['start']['value']):
                    if not self.action_thread:
                        logging.info('start action')
                        self.action_thread = threading.Thread(target=self.do_action, args=(self.action.split(";"), 0, ))
                        self.stopped.clear()
                        self.action_thread.start()
                        

            elif received['label'] == self.trigger['stop']['label']:
                if eval(received['value'] + self.trigger['stop']['op'] + self.trigger['stop']['value']):
                    if self.action_thread:
                        self.stopped.set()
                        self.action_thread = None
                        logging.info('end action')

    def do_action(self, actions, index):
        while not self.stopped.is_set():
            a = actions[index]
            x = a.split("=")
            if x[0] == "wait":
                logging.debug('waiting %s seconds', x[1])
                self.stopped.wait(float(x[1]))
                index += 1
            elif x[0] == "goto":
                logging.debug("go to instruction %s" , x[1])
                index = int(x[1])-1
            else:
                logging.debug("SET %s = %s", x[0], x[1])
                self.send_message(mto=self.sensor_bot_jid,
                          mbody='SET ' + x[0] + '=' + x[1], mtype='chat', mfrom=self.sender_jid)
                index += 1


if __name__ == '__main__':
    # Setting up the command line arguments
    optp = OptionParser()

    optp.add_option('-c', '--config=FILE', dest="conf_file", help='configuration FILE')
    optp.add_option('-d', '--debug', help='set logging to DEBUG', action='store_const',
                    dest='loglevel', const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-l', '--log=FILE', dest="log_file", help='log messages to FILE')

    opts, args = optp.parse_args()
#    print(opts.log_file)

    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    # If configuration file does not exist the script will terminate
    if not (os.path.isfile(str(opts.conf_file))):
        print "The configuration file does not exist"
        sys.exit()

    # Reading data from the configuration file
    conf = ConfigParser.ConfigParser()
    conf.read(opts.conf_file)

    ops = ["<=", ">=", "!=", "<", ">", "="]
    trigger_start = conf.get("Workflow", "trigger_start")
    trigger_stop = conf.get("Workflow", "trigger_stop")

    start_op = None
    stop_op = None
    #found_start_op, found_stop_op = False
    for i, o in enumerate(ops):
        if not start_op:
            if trigger_start.find(o) != -1:
                start_op = ops[i]
        if not stop_op:
            if trigger_stop.find(o) != -1:
                stop_op = ops[i]

    trigger_start = trigger_start.split(start_op)
    trigger_stop = trigger_stop.split(stop_op)

    trigger = {'start': {'label': trigger_start[0], 'value': trigger_start[1], 'op': start_op if start_op != "=" else "=="},
                'stop': {'label': trigger_stop[0], 'value': trigger_stop[1], 'op': stop_op if stop_op != "=" else "=="}}


    # Initializing the XMPP bot
    xmpp = Workflow(conf.get("XMPP", "sender_jid"), conf.get("XMPP", "sender_pass"), conf.get("XMPP", "receiver_jid"), conf.get("XMPP", "pubsub_jid"), conf.get("XMPP", "pubsub_node"), trigger, conf.get("Workflow", "action"))
