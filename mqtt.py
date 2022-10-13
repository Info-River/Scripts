import os
import time
import sys
import paho.mqtt.client as mqtt
import json
import random

THINGSBOARD_HOST = 'localhost'
ACCESS_TOKEN = 'E58EVOuWP0p9i0O7On6i'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=0.5

sensor_data = {'longitude': 0, 'latitude': 0}

next_reading = time.time()

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 8081, 60)

client.loop_start()

#lat: 	40.641841 - 40.6246665863825
#long: 	-8.656439 - -8.65726089425152

lat_intial = 40.641841
lat_final = 40.6246665863825
long_intial = -8.656439
long_final = -8.65726089425152
steps = 50

lat_incr = (lat_final- lat_intial)/steps
long_incr = (long_final- long_intial)/steps

longitude = long_intial
latitude = lat_intial

try:
    while True:
        longitude+=long_incr
        latitude+=lat_incr

        print(f"lat: {latitude}, long: {longitude}")
        sensor_data['latitude'] = latitude
        sensor_data['longitude'] = longitude

        if latitude == lat_final:
            latitude = lat_intial
        if longitude == long_final:
            longitude = long_intial

        # Sending humidity and temperature data to ThingsBoard
        client.publish('v1/devices/ambulance/telemetry', json.dumps(sensor_data), 1)

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
