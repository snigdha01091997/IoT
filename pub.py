import paho.mqtt.client as mqttClient
import time
import ast
import random
import json

def car_to_park():
    corr=random.randint(1,20)
    return corr

def on_message(client, userdata, message):   #callback method to print the slot status
    slot=str(message.payload)
    if slot =="b'0'":
	    print("sorry!!No slots are empty")
    else:
	    print("your car is in the slot:"+slot)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("Connection failed Return Code : ",rc)


Connected = False  # global variable for the state of the connection
client_name="pub"
broker_address = "127.0.0.1"  # Broker address
port = 1883  # Broker port
i=1
curr=1
x=1

client = mqttClient.Client(client_name)  # create new instance


client.on_connect = on_connect  # attach function to callback
client.on_message = on_message

client.connect(broker_address, port=port)  # connect to broker

client.loop_start()  # start the loop


while Connected != True:  # Wait for connection
    time.sleep(0.1)
try:
	while True:
		var=input("enter 1 for parking  and 0 for exit: ")     #to check if customer wants to park or take car from lot
		if var == '1':											#if customer wants to park
			client.publish(topic="vehicle/car",payload=var+","+str(curr),qos=1,retain=False) #publish the car id which is assigned at slot to broker
			time.sleep(5)
			client.subscribe("vehicle/location")      #subscribe to the location of slot where car is parked
			i += 1
			curr=i

		elif var=='0':                     #when customer wants to take his car
			car_num=int(input("enter your slot number: "))      # he has to give the slot number
			client.publish(topic="vehicle/car",payload=var+","+str(car_num),qos=1,retain=False) #publish the slot number
			y=x*10
			msg=f'your charge: {y}'
			print(msg)
			x+=1
			

except KeyboardInterrupt:
	print("excepted")
	client.loop_stop()
	client.disconnect()




