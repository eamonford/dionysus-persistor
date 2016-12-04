import paho.mqtt.client as mqtt
import json
from influxdb import InfluxDBClient


def on_connect(client, userdata, flags, rc):
    print("Connected to mosquitto with result code "+str(rc))

def on_message(client, userdata, msg):
        print msg
    	print(msg.topic+" "+str(msg.payload))
        messageDict = json.loads(str(msg.payload))

def main():
    print "hello world"

    influxClient = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')
    influxClient.create_database('dionysus')

    mqttClient = mqtt.Client()
    mqttClient.on_connect = on_connect
    mqttClient.on_message = on_message
    mqttClient.connect("eamonford.hopto.org", 1883, 60)
    mqttClient.subscribe("dionysus/moisture")

    mqttClient.loop_forever()


main()
