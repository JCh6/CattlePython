### CowManager.py

from Log import Log
import pandas as pd
from Cow import Cow
from utils import utils

log = Log()

class CowManager:
    def __init__(self, prefs):
        self.prefs = prefs
        self.cows = []
        self.dfCows = None
        self.Lat = prefs["LAT_KEY"]
        self.Lon = prefs["LON_KEY"]
        self.Date = prefs["DATE_KEY"]

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

            err = newCow.setDateKey(self.Date)
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

    def concatDataFrames(self):
        dfs = []

        if len(self.cows) < 2:
            return

        for cow in self.cows:
            dfs.append(cow.getDataFrame())

        self.dfCows = pd.concat(dfs)
        log.info("Dataframes concatenated successfully")

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
            "cows"  : cows,
            "total" : totalDistance
        }
    
    def getDistanceTraveledPerDay(self):
        totalDistance = 0
        cows = []

        for cow in self.cows:
            distObj = cow.getDistanceTraveledPerDay()
            cows.append({
                "name" : cow.getName(),
                "data" : {
                    "dates" : distObj
                }
            })

        return cows
    
    def heatMap(self, allCows=False):
        utils.createHeatMap({
            "center"   : self.prefs["CENTER"],
            "zoom"     : self.prefs["ZOOM"],
            "filename" : "maps/" + self.prefs["MAP_FILENAME"],
            "open"     : False,
            "coords"   : [[row[self.Lat], row[self.Lon]] for _, row in self.dfCows.iterrows()]
        })

        if allCows: self.heatMapByEachCow()
        log.info("Maps created successfully")