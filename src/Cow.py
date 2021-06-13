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
    
    def setNewColumns(self, columns):
        numCols = len(self.dataFrame.columns)

        for key in columns.keys():
            colHeader = columns[key]
            if key < numCols:
                self.dataFrame[colHeader] = self.dataFrame.apply(lambda row: str(row[key]).split("=")[1], axis=1)
            else:
                return "Error, please check the columns"

        return None

    def createHeatMap(self, mapOptions):
        mapOptions["coords"] = [[row[self.Lat], row[self.Lon]] for _, row in self.dataFrame.iterrows()]
        utils.createHeatMap(mapOptions)
        
    def getDistanceTraveled(self):
        distance = 0

        for i in range(len(self.dataFrame) - 1):
            row1 = self.dataFrame.iloc[i]
            row2 = self.dataFrame.iloc[i + 1]
            distance += utils.haversine(row1[self.Lat], row1[self.Lon], row2[self.Lat], row2[self.Lon])

        return distance
