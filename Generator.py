### Generator.py

from datetime import time, timedelta, datetime, date
from random import randint, uniform
import pandas as pd

# --------------------- Constants ---------------------
SECONDS_DAY = 86400
SECONDS_HOUR = 3600
DELTA = 0.01
LAT_LON = 1.570311382
LAT = 1.112298332
LON = 1.108462054
FORMAT = "%I:%M:%S %p"

# --------------------- Parameters ---------------------
lat = 4.76994
lon = -74.23248
days = 18
interval = 31

def genHours(): 
    return uniform(4, 6)

def genKms(): 
    return uniform(2, 4)

def genTime(): 
    return time(randint(10, 12), randint(0, 59), randint(0, 59))

def getCoin(): 
    return randint(0, 1)

def genProbability(): 
    return randint(-1, 1)

def getDelta(coord, prob, add, kms, num_rows):
    delta = 0

    if prob == 0:
        delta = ((kms * DELTA) / LAT_LON) / num_rows
    elif prob == -1 and coord == "LAT":
        delta = ((kms * DELTA) / LAT) / num_rows
    elif prob == 1 and coord == "LON":
        delta = ((kms * DELTA) / LON) / num_rows

    return delta if add else -delta 

def addSeconds(current_time, seconds):
    delta = timedelta(seconds=seconds)
    d = datetime.combine(date.today(), current_time) + delta
    return d.time()

# --------------------- Main ---------------------
data = []

for j in range(1, days + 1):
    hours = genHours()
    kms = genKms()
    curr_lat = lat
    curr_lon = lon
    curr_time = genTime()
    
    num_rows = int((hours * SECONDS_HOUR) / interval)

    for _ in range(num_rows):
        row = []
        prob = genProbability()
        add = True if getCoin() == 1 else False

        curr_lat += getDelta("LAT", prob, add, kms, num_rows)
        curr_lon += getDelta("LON", prob, add, kms, num_rows)
        curr_time = addSeconds(curr_time, interval)

        row.append(curr_lat)
        row.append(curr_lon)
        row.append(curr_time.strftime(FORMAT))
        row.append(j)

        data.append(row)

df = pd.DataFrame(data)
df.to_csv("data/clean/Cow1.txt", header=False, index=False)
