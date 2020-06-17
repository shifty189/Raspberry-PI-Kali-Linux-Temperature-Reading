# Small Python program to keep track of your Raspberry Pi's temperature. 
# This program has only been tested using Kali Linux and Lakka Linux, but i think it will work on most Linux distros
# Version 00.02

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
sec = 1


# check arguments
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
		print("-t	designate in celcieus how hot should be considered overheating, Default is 80")
		print("-s	Determine in seconds how often to check temperature. Default is once a second")
		exit()
	if a == "-k":
		keep_running = True
	if a == "-t":
		overheat_temp = int(args[index + 1])
	if a == "-s":
		if sec < 1:
			print("Must take at leaste one reading a second")
			exit()
		try:
			sec = int(args[index + 1])
		except ValueError:
			print("-s requires an Int (Hole Number)")
			exit()
		
while True:
	os.system('clear')
	#this temp file is where the RPI stores its internal CPU sensor reading, so we read it
	file = open("/sys/class/thermal/thermal_zone0/temp", "r")

	raw = int(file.readline())
	file.close()

# get a clean number
	cel = raw/1000
# convert our temp to fahrenhiet
	far = (cel * 1.8) + 32

# counter and ticks variables are used to calculate average later
	counter += cel
	ticks += 1

# check if current temp is a new high or low record
	if cel > maxC:
		maxC = cel
	if cel < minC:
		minC = cel
	if far > maxF:
		maxF = far
	if far < minF:
		minF = far

	if cel > overheat_temp:
		overheat += 1

	if celc == False and fare == False:
		print(str(cel) + "C" " or " + str(far) + "F")
		if keep_running:
			print("\nHottest recorded temp is " + str(maxC) + "'C or " + str(maxF) + "'F")
			print("\nColdest recorded temp is " + str(minC) + "'C or " + str(minF) + "'F")
			print("\nAverage: " + str(counter/ticks) + "C or " + str(((counter/ticks) * 1.8) + 32) + "F")
	elif celc and fare:
		print("only pick -c or -f or don't specify to get both")
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
# pause program for 1 second before continuing the main While loop
	time.sleep(sec)
