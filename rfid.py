import serial, time, json, csv
import datetime
import RPi.GPIO as gpio


# For PiB+ 2, Zero use:
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
gpio.setmode(gpio.BCM)
A_Pin = 16
gpio.setup(A_Pin, gpio.IN)
B_Pin = 26
gpio.setup(B_Pin, gpio.OUT)


cards = {}
with open('cards.json', 'r') as f:
    cards = json.load(f)

items_inside = []
now = datetime.datetime.now()

def check_schedule(): #this function checks whether all the items as per schedule are in the bag
    cur_day = now.strftime("%a")
    schedule = {}
    with open('schedule.json', 'r') as f:
        schedule = json.load(f)
    flag = 0
    for item in schedule[cur_day]:
        if item in items_inside:
            continue
        else:
            print(item + " missing")
            flag = 1
    if flag:
        gpio.output(B_Pin, True)
        time.sleep(5);
        gpio.output(B_Pin, False)
    
while 1:
    string = ser.read(12)
    Sel_A = gpio.input(A_Pin)
    print(Sel_A)
    if len(string) != 0:
        if string in cards.keys():
            item = cards[string]
            row = [] #for maintaing a log of insertion and removal times and item name
            row.append(datetime.datetime.now())
            row.append(item)
            if item in items_inside: #if an item already in the list of current item is read, it means it has been removed
                items_inside.remove(item)
                print(item + " removed")
                row.append("removed")
            else: #else a new item is being added to the list
                items_inside.append(item)
                print(item + " inserted")
                row.append("inserted")
            
            with open('item_log.csv', 'a') as csvFile: #for maintaing a log of insertion and removal times and item name
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
    
    if Sel_A: #if a signal is received for checking schedule
        check_schedule()
