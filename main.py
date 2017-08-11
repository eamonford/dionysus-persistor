import paho.mqtt.client as mqtt
import json
from influxdb import InfluxDBClient
import os
import Config
import logging

logging.basicConfig()
Logger = logging.getLogger(__name__)
Logger.setLevel(20)

TOPIC_NAME = "dionysus/readings"

print ("Connecting to influxdb host " + Config.Configuration().influxdbHost)
influxClient = InfluxDBClient(
    Config.Configuration().influxdbHost,
    8086,
    Config.Configuration().influxdbUsername,
    Config.Configuration().influxdbPassword,
    'dionysus_readings')

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT at host " + Config.Configuration().mqttHost)

def on_message(client, userdata, msg):
    try:
        messageDict = json.loads(str(msg.payload))
        json_body = [
               {
                   "measurement": messageDict["metric"],
                   "time": messageDict["time"],
                   "fields": {
                       "value": messageDict["value"],
                       "battery": messageDict["battery"]
                   },
                   "tags": {
                        "device_id": messageDict["device_id"],
                        "name": messageDict["name"]
                   }
               }
           ]
        print("Persisting to influxdb: " + json.dumps(json_body))
        influxClient.write_points(points=json_body)
    except KeyError as e:
        Logger.exception("Could not parse message: " + msg.payload)
    except:
        Logger.exception("There was a problem parsing and storing message: " + msg.payload)

def main():
    mqttClient = mqtt.Client()
    mqttClient.on_connect = on_connect
    mqttClient.on_message = on_message
    mqttClient.connect(Config.Configuration().mqttHost, 1883, 60)
    mqttClient.subscribe(TOPIC_NAME)

    mqttClient.loop_forever()


main()
