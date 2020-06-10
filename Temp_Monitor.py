import os
import time
import sys

celc = False
fare = False
keep_running = False
overheat = 0
maxC = 0
minC = 1000
maxF = 0
minF = 1000
ticks = 0
counter = 0
overheat_temp = 80


args = sys.argv

for index, a in enumerate(args):
	if a == "-c":
		celc = True
	if a == "-f":
		fare = True
	if a == "-h" or a == "--help":
		print("-c	for celcieus")
		print("-f	for ferenhight")
		print("-k	to continusly run")
		print("-t	designate how hot should be considered overheating")
		#print("only 3 flags -c for celcieus, -f for ferenhight, and -k to continusly run")
		exit()
	if a == "-k":
		keep_running = True
	if a == "-t":
		overheat_temp = args[index + 1]
while True:
	os.system('clear')
	#this temp file is where the RPI stores its internal CPU sensor reading
	file = open("/sys/class/thermal/thermal_zone0/temp", "r")

	raw = int(file.readline())
	file.close()

	cel = raw/1000
	far = (cel * 1.8) + 32

	counter += cel
	ticks += 1

	if cel > maxC:
		maxC = cel
	if cel < minC:
		minC = cel
	if far > maxF:
		maxF = far
	if far < minF:
		minF = far

	if cel > 80:
		overheat += 1

	if celc == False and fare == False:
		print(str(cel) + "C" " or " + str(far) + "F")
		if keep_running:
			print("\nHottest recorded temp is " + str(maxC) + "'C or " + str(maxF) + "'F")
			print("\nColdest recorded temp is " + str(minC) + "'C or " + str(minF) + "'F")
			print("\nAverage: " + str(counter/ticks) + "C or " + str(((counter/ticks) * 1.8) + 32) + "F")
	elif celc and fare:
		print("only pick -c or -f")
		exit()
	elif fare:
		print(str(far) + " F'")
		if keep_running:
			print("\nHottest recorded temp is " + str(maxF) + "'F")
			print("\nColdest recorded temp is " + str(minF) + "'F")
			print("Average: "  + str(((counter/ticks) * 1.8) + 32) + "F")
	elif celc:
		print(str(cel) + "C") 
		if keep_running:
			print("\nHottest recorded temp is " + str(maxC) + "'C")
			print("\nColdest recorded temp is " + str(minC) + "'C")
			print("Average: " + str(counter/ticks) + "C")
	if overheat > 0:
		print("\nCPU has gone over " + str(overheat_temp) + "'C " + str(overheat) + " times!")
	if keep_running == False:
		exit()
	else:
		print("\nPress Ctrl + C to quit")
	time.sleep(1)
