### utils.py

import os
import math
import folium
import webbrowser
from folium import plugins


def haversine(lat1, lon1, lat2, lon2):
    R = 6373.0

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def createHeatMap(mapOptions):
    myMap = folium.Map(mapOptions["center"], zoom_start=mapOptions["zoom"])
    mapfilename = mapOptions["filename"] + ".html"

    plugins.HeatMap(mapOptions["coords"]).add_to(myMap)
    myMap.save(mapfilename)

    if mapOptions["open"]:
        webbrowser.open("file://" + os.path.abspath(os.getcwd()) + "/" + mapfilename)
