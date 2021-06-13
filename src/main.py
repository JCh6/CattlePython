### main.py

from Cow import Cow
from Log import Log
import pandas as pd
from usr.prefs import prefs


def loadCows(cows):
    for name, filename in prefs["FILES"].items():
        newCow = Cow(name, "data/" + filename)

        err = newCow.setDataFrame(None, "|")
        if err != None: log.fatal(err)

        err = newCow.setNewColumns(prefs["COLUMNS"])
        if err != None: log.fatal(err)
        
        err = newCow.setLatitudeKey(prefs["LAT_KEY"])
        if err != None: log.fatal(err)

        err = newCow.setLongitudeKey(prefs["LON_KEY"])
        if err != None: log.fatal(err)

        cows.append(newCow)
    
    log.info("Cows loaded successfully")

def heatMapByCow(cows):
    for cow in cows:
        cow.createHeatMap({
            "center"   : prefs["CENTER"],
            "zoom"     : prefs["ZOOM"],
            "filename" : "maps/" + prefs["MAP_FILENAME"] + "_" + cow.getName(),
            "open"     : False
        })
    log.info("Maps created successfully")

def concatDataFrames(cows):
    dfs = []

    if len(cows) < 2:
        return None

    for cow in cows:
        dfs.append(cow.getDataFrame())

    return pd.concat(dfs)

def main():
    cows = []
    dfCows = None
    
    loadCows(cows)
    dfCows = concatDataFrames(cows)
    heatMapByCow(cows)


if __name__ == "__main__":
    log = Log()
    log.info("Log ready!")
    main()
