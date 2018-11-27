YOUTUBE LINK
https://www.youtube.com/watch?v=DyaReYhgGUA

The pi and arduino need to be connected together as there is exchange of information between them. 
RFID and wifi module and connected to pi. 
Light sensor, buzzer, bluetooth, zip checker are connected to arduino. 

Digital_Light_Sensor.ino: This files does following things:
If zip is open and outside light is low, turn on LED inside bag
If someone is wearing bag (detect by Force Resistor) and zip is opened, raise the buzzer
If bluetooth receives "1", send signal to pi to check schedule
If bluetooth receives "2", raise the buzzer (for finding bag)
Transmits present location of bag by Bluetooth beacon
Sends the force value to Pi for MQTT

add_schedule:
Add schedule for all the days by entering stored names

set_cards:
save rfid tags as customised name (like Science nb, Maths nb)

mqtt.py
Receives force value from pi, by USB, and publish it into mosquitto server (test.mosquitto.org, 1883, fsr_bag)
We publish start time, end time and exponential average of force detected.

rfid.py
Detects when a particular item is inserted/removed by its RFID. Stores it into log. 
If schedule check is called, make sure all the items of present day are present in the bag, else tells arduino to raise buzzer.

schedule.json
Stores schedule of all days

cards.json
Store customised names of rfid tags

item_log.csv
Log of all item inserted and removed
