import paho.mqtt.client as mqttClient
import time
import json
import re

#for now we have taken only lot of six slots
v=0  
      
d={k:v for k in range(1,7)}  # dictionary to keep track of slot,initialy it will be empty so initialized to 0


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("Connection failed")

x=1
def on_message(client, userdata, message):
    info = str( message.payload)  #receives the car id to be parked
    info = info.split(",")
    
    i=0    #variable to keep track whether the lot is full or not
    if info[0] == "b'1":  #indicates that customer want to park car in the lot
        for key,val in d.items():
            if val==0:     #look for the empty slot
                d[key]=info[1]
                i = 1
                client.publish("vehicle/location",key)   #publish the slot number
                break
        if i == 0:
            client.publish("vehicle/location",i)  #if slots are full ,publish 0
        print("*************CURRENT SLOT STATE************")
        print(d)

    elif info[0] == "b'0":    #if customer want to take out his car
        for key,val in d.items():
            if val == info[1]:    #look for the slot and set it to 0
                d[key]=0
                break
        print(d)        
        print("car exit")
    






Connected = False  # global variable for the state of the connection
client_name="sub" #client name should be unique

broker_address = "127.0.0.1"  # Broker address
port = 1883  # Broker port
user = "admin"  # Connection username
password = "hivemq"  # Connection password


client = mqttClient.Client(client_name)  # create new instance

client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback

client.connect(broker_address, port=port)  # connect to broker

client.loop_start()  # start the loop
#Task1 : Write your code here
client.subscribe("vehicle/car")

while Connected != True:  # Wait for connection
    time.sleep(0.1)


try:
    while True:
        time.sleep(0.1)


except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()

