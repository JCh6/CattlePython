### Cow.py

import pandas as pd

class Cow:
    def __init__(self, filename):
        self.filename = filename

    def getFilename(self):
        return self.filename
    
    def setDataFrame(self, hasHeader=None, delimiter=","):
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
            return None
        return '"{}" column does not exist'.format(key)
    
    def setLongitudeKey(self, key):
        if key in self.dataFrame:
            self.Lon = key
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
