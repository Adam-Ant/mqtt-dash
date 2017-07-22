from backports import configparser
import os
import paho.mqtt.client as mqtt
import logging
import argparse
from time import sleep
import ssl

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

mqttc = mqtt.Client()

defaultconfig = '''[MQTT]
# The hostname or IP of the MQTT Server
host =
# The Port of the MQTT Server (Default: 1883)
#port =
# Is a Username and Password required? (Default: false)
#auth = True
# Username (If required)
#user =
# Password (if required)
#pass =
# SSL required? (Default: False)
# Uses TLSv1.2
#ssl = True
# CA Cert location (Default: /etc/ssl/certs/ca-certificates.crt)
# This is sufficient for brokers using LetsEncrypt
#certpath =

[Buttons]
# For every line, list the MAC of the button, and the MQTT topic to publish to.
01:23:45:67:89:ab = example/example_topic'''

def arp_display(pkt):
    topic = ''
    foundmac = None
    if pkt.haslayer(ARP):
        if pkt[ARP].op == 1: #who-has (request)
            i = 0
            for j in macs:
                if (macs[i] == pkt[ARP].hwsrc):
                    foundmac = i
                i += 1
    if not (foundmac == None): # If we have actually found a matching mac
        print 'Found ARP for MAC %s, sending to topic %s' % (macs[foundmac], topics[foundmac])
        mqttc.publish(topics[foundmac], "ON") # Both to simulate button press
        mqttc.publish(topics[foundmac], "OFF")


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(prog='MQTT-Dash',description='Send MQTT events when dash nuttons are pressed.')
    argparser.add_argument('-c','--config',help='Specify directory for config file and database')
    cmdargs = argparser.parse_args()

    if not (cmdargs.config):
        filepath = '.'
    else:
        filepath = cmdargs.config

    if not (os.path.isdir(filepath)):
        print('Error: Config directory does not exist. Exiting...')
        exit(1)

    if not (os.path.isfile(filepath + '/dash.cfg')):
        print('Warn: Config file does not exist, writing example config. Please configure and try again.')
        c = open(filepath + '/dash.cfg', 'w')
        c.write(defaultconfig)
        c.close()
        exit(1)


    config = configparser.ConfigParser(delimiters=('='))
    config.read(filepath + '/dash.cfg')
    hostname = config['MQTT'].get('host')
    port = config['MQTT'].get('port')
    authrequired = config['MQTT'].getboolean('auth', False)
    sslrequired = config['MQTT'].getboolean('ssl', False)
    ca_certs = config['MQTT'].get('certpath', "/etc/ssl/certs/ca-certificates.crt")
    if (authrequired):
        username = config['MQTT'].get('user')
        password = config['MQTT'].get('pass')

    macs = []
    topics = []
    for option, value in config.items('Buttons'):
        macs.append(option)
        topics.append(value)
        print 'Importing mac %s with topic %s' % (option,value)

    if (authrequired):
        mqttc.username_pw_set(username,password=password)
    if (sslrequired):
        mqttc.tls_set( ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2 )
    mqttc.connect(hostname)
    mqttc.loop_start()
    sniff(prn=arp_display, filter="arp", store=0, count=0)
