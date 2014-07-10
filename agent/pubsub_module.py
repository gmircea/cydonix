#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import logging
import sleekxmpp
from sleekxmpp.xmlstream import ET, tostring


if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input

class PubsubClass(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, server,
                       node=None, action='list', data=''):
        super(PubsubClass, self).__init__(jid, password)
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0059')
        self.register_plugin('xep_0060')

        self.actions = ['nodes', 'create', 'delete',
                        'publish', 'get', 'retract',
                        'purge', 'subscribe', 'unsubscribe']

        self.action = action
        self.node = node
        self.data = data
        self.pubsub_server = server

        self.add_event_handler('session_start', self.start, threaded=True)

    def start(self,event):
        self.get_roster()
        self.send_presence()

        try:
            getattr(self, self.action)()
        except:
            logging.error('Could not execute the following action : %s'
                          % self.action)
        self.disconnect()


    def nodes(self):
        try:
            result = self['xep_0060'].get_nodes(self.pubsub_server, self.node)
            for item in result['disco_items']['items']:
                print('Nod  - %s' % str(item))
        except:
            logging.error('Nu s-a putut afisa lista cu noduri.')

    def create(self):
        try:
            self['xep_0060'].create_node(self.pubsub_server, self.node)
            print ("nod creat %s " % self.node)
        except:
            logging.error('Nu s-a putut crea nodul: %s' % self.node)

    def delete(self):
        try:
            self['xep_0060'].delete_node(self.pubsub_server, self.node)
            print('Nod sters: %s' % self.node)
        except:
            logging.error('Nu s-a putut sterge nodul: %s' % self.node)

    def publish(self):
        payload = ET.fromstring("<test xmlns='test'>%s</test>" % self.data)
        try:
            result = self['xep_0060'].publish(self.pubsub_server, self.node, payload=payload)
            id = result['pubsub']['publish']['item']['id']
            print('Published at item id: %s' % id)
            print "\n %s" % self.data
        except:
            logging.error('Could not publish to: %s' % self.node)

    def get(self):
        try:
            result = self['xep_0060'].get_item(self.pubsub_server, self.node, self.data)
            for item in result['pubsub']['items']['substanzas']:
                print('Retrieved item %s: %s' % (item['id'], tostring(item['payload'])))
        except:
            logging.error('Could not retrieve item %s from node %s' % (self.data, self.node))

    def retract(self):
        try:
            result = self['xep_0060'].retract(self.pubsub_server, self.node, self.data)
            print('Retracted item %s from node %s' % (self.data, self.node))
        except:
            logging.error('Could not retract item %s from node %s' % (self.data, self.node))

    def purge(self):
        try:
            result = self['xep_0060'].purge(self.pubsub_server, self.node)
            print('Purged all items from node %s' % self.node)
        except:
            logging.error('Could not purge items from node %s' % self.node)
