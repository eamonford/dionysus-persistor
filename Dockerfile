FROM resin/rpi-raspbian
RUN apt-get update && apt-get install -y python-pip && pip install paho-mqtt && pip install influxdb
RUN mkdir /persistor
COPY main.py /persistor/main.py
RUN cd /persistor && sqlite3 sensors.db < db/0.1_create_initial_tables.sql
CMD ["python", "/ingestor/main.py"]
