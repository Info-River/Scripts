import paho.mqtt.client as mqtt
import time
from random import randrange, uniform

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))

mqttBroker ='mednat.ieeta.pt'

client = mqtt.Client()
client.connect(mqttBroker, 8793)

while True:
    randNumber = uniform(20.0, 21.0)
    client.publish("incident/created", randNumber)
    print("Just published " + str(randNumber) + " to topic TEMPERATURE")
    time.sleep(1)