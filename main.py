import paho.mqtt.client as mqtt
import json
import datetime
from influxdb import InfluxDBClient


def on_connect(client, userdata, flags, rc):
    print("Connected to mosquitto with result code "+str(rc))

def on_message(client, userdata, msg):
        messageDict = json.loads(str(msg.payload))
        json_body = [
               {
                   "measurement": "moisture",
                   "time": datetime.datetime.now().isoformat(),
                   "fields": {
                       "value": messageDict["value"]
                   }
               }
           ]
        print json_body
        

def main():
    influxClient = InfluxDBClient('db', 8086, 'root', 'root', 'example')
    mqttClient = mqtt.Client()
    mqttClient.on_connect = on_connect
    mqttClient.on_message = on_message
    mqttClient.connect("eamonford.hopto.org", 1883, 60)
    mqttClient.subscribe("dionysus/moisture")

    mqttClient.loop_forever()


main()
