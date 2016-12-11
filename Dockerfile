FROM resin/rpi-raspbian
RUN apt-get update && apt-get install -y python-pip && pip install paho-mqtt && pip install influxdb
RUN mkdir /persistor
COPY . /persistor
CMD ["python", "-u", "/persistor/main.py"]
