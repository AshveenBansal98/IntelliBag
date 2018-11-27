import json
#code for setting schedule, the code is self explanatory
schedule = {}

while 1:
	day = raw_input("Enter the day\n")
	if(day == "-1"):
		break

	list = []
	while 1:
		item = raw_input("Enter the item name(-1 to exit):\n")
		if(item == "-1"):
			break
		else:
			if item in list:
				print("already added")
			else:
				list.append(item)

	schedule[day] = list

json = json.dumps(schedule)
f = open("schedule.json","w")
f.write(json)
f.close()