#! /usr/bin/env python

from optparse import OptionParser
import logging
import getpass

optp=OptionParser()

optp.add_option('-q', '--quiet', help='set logging to ERROR',
                action='store_const',dest='loglevel',
                const=logging.ERROR,default=logging.INFO)
optp.add_option('-d','--debug', help='set logging to DEBUG',
                action='store_const',dest='loglevel',
                const=logging.DEBUG,default=logging.INFO)
optp.add_option('-v','--verbose',help='set logging to COMM',
                action='store_const',dest='loglevel',
                const=5,default=logging.INFO)
optp.add_option("-j", "--jid", dest="jid", help="JID to use")
optp.add_option("-p", "--password", dest="password",
                help="password to use")
optp.add_option("-s",'--pubsub_server',dest='pubsub_server',
                help="Pub Sub Server to use ")
optp.add_option("-n","--node",dest="node",help="pubsub node")


opts, args = optp.parse_args()

logging.basicConfig(level=opts.loglevel,
                    format='%(levelname)-8s %(message)s')

if opts.jid is None:
    opts.jid=raw_input(" Username : ")

if opts.password is None:
    opts.password = getpass.getpass(" Password : ")

if opts.pubsub_server is None:
    opts.pubsub_server = raw_input(" PubSub Server : ")

if opts.node is None:
    opts.node = raw_input(" PubSub node : ")
