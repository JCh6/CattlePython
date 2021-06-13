### main.py

from Cow import Cow
from Log import Log
import pandas as pd
from utils import utils
from usr.prefs import prefs


class CowsHandler:
    def __init__(self, prefs):
        self.prefs = prefs
        self.cows = []
        self.dfCows = None
        self.Lat = prefs["LAT_KEY"]
        self.Lon = prefs["LON_KEY"]

    def getCows(self):
        return self.cows

    def getDataFrame(self):
        return self.dfCows

    def loadCows(self):
        for name, filename in self.prefs["FILES"].items():
            newCow = Cow(name, "data/" + filename)

            err = newCow.setDataFrame(None, "|")
            if err != None: log.fatal(err)

            err = newCow.setNewColumns(self.prefs["COLUMNS"])
            if err != None: log.fatal(err)
            
            err = newCow.setLatitudeKey(self.Lat)
            if err != None: log.fatal(err)

            err = newCow.setLongitudeKey(self.Lon)
            if err != None: log.fatal(err)

            self.cows.append(newCow)
        
        log.info("Cows loaded successfully")

    def heatMapByEachCow(self):
        for cow in self.cows:
            cow.createHeatMap({
                "center"   : self.prefs["CENTER"],
                "zoom"     : self.prefs["ZOOM"],
                "filename" : "maps/" + self.prefs["MAP_FILENAME"] + "_" + cow.getName(),
                "open"     : False
            })

        log.info("Maps created successfully")

    def concatDataFrames(self):
        dfs = []

        if len(self.cows) < 2:
            return

        for cow in self.cows:
            dfs.append(cow.getDataFrame())

        log.info("Dataframes concatenated successfully")
        self.dfCows = pd.concat(dfs)

    def getDistanceTraveled(self):
        totalDistance = 0
        cows = []

        for cow in self.cows:
            distance = cow.getDistanceTraveled()
            totalDistance += distance
            cows.append({
                "name"     : cow.getName(),
                "distance" : distance
            })
        
        return {
            "cows"    : cows,
            "total" : totalDistance
        }
    
    def heatMap(self):
        utils.createHeatMap({
            "center"   : self.prefs["CENTER"],
            "zoom"     : self.prefs["ZOOM"],
            "filename" : "maps/" + self.prefs["MAP_FILENAME"],
            "open"     : False,
            "coords"   : [[row[self.Lat], row[self.Lon]] for _, row in self.dfCows.iterrows()]
        })

# Main func
def main():
    ch = CowsHandler(prefs)
    ch.loadCows()
    ch.concatDataFrames()
    ch.heatMapByEachCow()
    ch.heatMap()

if __name__ == "__main__":
    log = Log()
    log.info("Log ready!")
    main()
