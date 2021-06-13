### main.py

import os
import folium
from folium import plugins
import webbrowser
import pandas as pd
from usr.prefs import prefs

'''

try:
    df = pd.read_csv("data/" + prefs["fileName"], header=None, delimiter="|")
    lat = prefs["latitudeKey"]
    lon = prefs["longitudeKey"]
    numCols = len(df.columns)

    for key in prefs["columns"].keys():
        colHeader = prefs["columns"][key]
        if key < numCols:
            df[colHeader] = df.apply(lambda row: str(row[key]).split("=")[1], axis=1)
        else:
            raise Exception("Error, please check the columns")

    myMap = folium.Map(prefs["center"], zoom_start=prefs["zoom"])
    mapfilename = "maps/" + prefs["mapfilename"] + ".html"

    df[lat] = df[lat].astype(float)
    df[lon] = df[lon].astype(float)

    hd = [[row[lat], row[lon]] for i, row in df.iterrows()]

    plugins.HeatMap(hd).add_to(myMap)
    myMap.save(mapfilename)
    webbrowser.open("file://" + os.path.abspath(os.getcwd()) + "/" + mapfilename)

except Exception as e:
    print(e)

'''