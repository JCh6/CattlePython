### TakeLatLon.py

import serial
import string
import pynmea2
from datetime import datetime, timedelta
from time import sleep

## Variables
# Sleeptime in minutes
sleepTime = 0.5

# EndTime in hours
endHour = 0.5
endTime = datetime.now() + timedelta(hours=endHour)

# Open or create file
fileName = "output.txt"
file = open(fileName, "a")


while datetime.now() < endTime:
	port = "/dev/ttyAMA0"
	ser = serial.Serial(port, baudrate=9600, timeout=0.5)
	dataout = pynmea2.NMEAStreamReader()
	newdata = ser.readline()

	if newdata[0:6] == "$GPRMC":
		newmsg = pynmea2.parse(newdata)
		lat = newmsg.latitude
		lng = newmsg.longitude
		now = datetime.now()
		date = now.strftime("%d/%m/%y")
		current_time = now.strftime("%H:%M:%S")
		gps = "LAT=" + str(lat) + "|LON=" + str(lng) + "|DATE=" + str(date) + "|TIME=" + str(current_time)

		print(gps)
		file.write(gps + "\n")
		sleep(sleepTime * 60)

# Close file
file.close()
