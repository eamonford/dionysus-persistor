# import psycopg2
import sqlite3
import os
import time
import getopt
import logging

class Borg:
	_shared_state = {}
	def __init__(self):
		self.__dict__ = self._shared_state

class Configuration(Borg):
	def __init__(self):
		Borg.__init__(self)
		self.influxdbHost = os.getenv('INFLUXDB_HOST', "localhost")
		self.influxdbUsername = os.getenv('INFLUXDB_USERNAME', "root")
		self.influxdbPassword = os.getenv('INFLUXDB_PASSWORD', "root")
		self.mqttHost = os.getenv('MQTT_HOST', 'localhost')
