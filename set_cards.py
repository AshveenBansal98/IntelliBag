import serial
import json
# For PiB+ 2, Zero use:
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
# For Pi3 use
#ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

cards = {}

def set_card(card_id): #set name of this card 
    name = raw_input("Please enter name of the item:")
    cards[card_id] = name
 
while len(cards) < 2: #bag is assumed to have 2 items as we only had 2 tags
    string = ser.read(12)
    if len(string) == 0:
        print("Please wave a tag")
    else:
        print(string)
        if(string in cards.keys()):
            print(cards[string])
        else:
            set_card(string)

json = json.dumps(cards) #storing the list in json file
f = open("cards.json","w")
f.write(json)
f.close()