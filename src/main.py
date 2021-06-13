### main.py

import os
from Cow import Cow
from Log import Log
from usr.prefs import prefs
import folium
from folium import plugins
import webbrowser

def loadCows(cows):
    for filename in prefs["FILES"]:
        newCow = Cow("data/" + filename)
        err = newCow.setDataFrame(None, "|")
        
        if err != None:
            log.fatal(err)

        err = newCow.setNewColumns(prefs["COLUMNS"])

        if err != None:
            log.fatal(err)
        
        errLat = newCow.setLatitudeKey(prefs["LAT_KEY"])

        if err != None:
            log.fatal(err)

        err = newCow.setLatitudeKey(prefs["LON_KEY"])

        if err != None:
            log.fatal(err)

        cows.append(newCow)
    
    log.info("Cows loaded successfully")


def main():
    cows = []
    loadCows(cows)
    


if __name__ == "__main__":
    log = Log()
    main()



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