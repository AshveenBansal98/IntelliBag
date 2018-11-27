#!/usr/bin/python

import time
import serial
import re
import paho.mqtt.client as mqtt
import datetime

MQTT_SERVER = "test.mosquitto.org"

mqttc = mqtt.Client("python_pub")
mqttc.connect(MQTT_SERVER, 1883)
 
ser = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=5)
alpha = 0.5 #parameter for exponential average.
st_time = ""
avg_wt = 0


while True:
    input = ser.readline()
    input = re.findall(r'\d+', input)[0] #this value is sent by Arduino and need to be trimmed to get actual integer value
    input = int(input)
    print(input)
    if(input):
        if(st_time == ""):  #bag is just worn by person, store current time
            st_time = str(datetime.datetime.now())
            avg_wt = input
        avg_wt = avg_wt * alpha + (1 - alpha) * input #we are taking exponential average with parameter alpha
    else:
        if(st_time != ""): #person has now took off the bag
            end_time = str(datetime.datetime.now()) #store current time
            data = st_time + " " + end_time + " " + str(avg_wt)
            mqttc.publish("fsr_bag", data) #publish both the times and exponential average to mqtt server
            avg_wt = 0
            st_time = ""