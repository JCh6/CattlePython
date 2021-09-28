### Cow.py

import pandas as pd
from utils import utils


class Cow:
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename

    def getName(self):
        return self.name

    def getFilename(self):
        return self.filename
    
    def setDataFrame(self, hasHeader=0, delimiter=","):
        try:
            self.dataFrame = pd.read_csv(self.filename, header=hasHeader, delimiter=delimiter)
            return None
        except Exception as e:
            return e

    def getDataFrame(self):
        return self.dataFrame

    def setLatitudeKey(self, key):
        if key in self.dataFrame:
            self.Lat = key
            self.dataFrame[key] = self.dataFrame[key].astype(float)
            return None
        return '"{}" column does not exist'.format(key)
    
    def setLongitudeKey(self, key):
        if key in self.dataFrame:
            self.Lon = key
            self.dataFrame[key] = self.dataFrame[key].astype(float)
            return None
        return '"{}" column does not exist'.format(key)
    
    def setDateKey(self, key):
        if key in self.dataFrame:
            self.Date = key
            return None
        return '"{}" column does not exist'.format(key)
    
    def setNewColumns(self, columns):
        numCols = len(self.dataFrame.columns)

        for key in columns.keys():
            colHeader = columns[key]
            if key < numCols:
                self.dataFrame[colHeader] = self.dataFrame.apply(lambda row: str(row[key]), axis=1)
            else:
                return "Error, please check the columns"

        return None

    def createHeatMap(self, mapOptions):
        mapOptions["coords"] = [[row[self.Lat], row[self.Lon]] for _, row in self.dataFrame.iterrows()]
        utils.createHeatMap(mapOptions)
        
    def getDistanceTraveled(self):
        distance = 0
        lastRow = self.dataFrame.iloc[0] if len(self.dataFrame) > 0 else None

        for i in range(1, len(self.dataFrame)):
            currentRow = self.dataFrame.iloc[i]
            distance += utils.haversine(lastRow[self.Lat], lastRow[self.Lon], currentRow[self.Lat], currentRow[self.Lon])
            lastRow = currentRow

        return distance
    
    def getDistanceTraveledPerDay(self):
        lastRow = self.dataFrame.iloc[0] if len(self.dataFrame) > 0 else None
        resp = {lastRow[self.Date] : lastRow}
        dist = {lastRow[self.Date] : 0}

        for i in range(1, len(self.dataFrame)):
            currentRow = self.dataFrame.iloc[i]
            currDate = currentRow[self.Date]

            if currDate not in resp:
                dist[currDate] = 0
                resp[currDate] = currentRow                

            lastRow = resp[currDate]
            dist[currDate] += utils.haversine(lastRow[self.Lat], lastRow[self.Lon], currentRow[self.Lat], currentRow[self.Lon])
            resp[currDate] = currentRow
        
        return dist
