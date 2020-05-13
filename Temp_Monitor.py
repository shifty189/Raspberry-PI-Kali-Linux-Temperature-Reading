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


args = sys.argv
for a in args:
	if a == "-c":
		celc = True
	if a == "-f":
		fare = True
	if a == "-h" or a == "--help":
		print("only 3 flags -c for celcieus, -f for ferenhight, and -k to continusly run")
		exit()
	if a == "-k":
		keep_running = True
while True:
	os.system('clear')
	#this temp file is where the RPI stores its internal CPU sensor reading
	file = open("/sys/class/thermal/thermal_zone0/temp", "r")

	raw = int(file.readline())
	file.close()
	
	#convert the raw data to celsius
	cel = raw/1000
	far = (cel * 1.8) + 32

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
		print("\nHottest recorded temp is " + str(maxC) + "'C or " + str(maxF) + "'F")
		print("\nColdest recorded temp is " + str(minC) + "'C or " + str(minF) + "'F")
	elif celc and fare:
		print("only pick -c or -f")
		exit()
	elif fare:
		print(str(far) + " F'")
		print("\nHottest recorded temp is " + str(maxF) + "'F")
		print("\nColdest recorded temp is " + str(minF) + "'F")
	elif celc:
		print(str(cel) + "C") 
		print("\nHottest recorded temp is " + str(maxC) + "'C")
		print("\nColdest recorded temp is " + str(minC) + "'C")
	if overheat > 0:
		print("\nCPU has gone over 80'C " + str(overheat) + " times!")
	#if -k was not specified, exit after taking a single reading
	if keep_running == False:
		exit()
	else:
		print("\nPress Ctrl + C to quit")
	#set the system to pause for 1 second
	time.sleep(1)
