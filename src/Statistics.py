### Statistics.py

from Log import Log
from utils import utils

log = Log()

class Statistics:
    def __init__(self, prefs):
        self.prefs = prefs
        self.dataFrame = utils.getDataFrameFromExcel(prefs["INPUT"], prefs["COLS"])
        log.info("Excel loaded successfully")

    def getDataFrame(self):
        return self.dataFrame

    def hasColumn(self, column):
        return column in self.dataFrame

    def getVariance(self, column):
        if not self.hasColumn(column): return "Invalid Column"
        return self.dataFrame.var()[column]

    def getStd(self, column):
        if not self.hasColumn(column): return "Invalid Column"
        return self.dataFrame.std()[column]

    def getCV(self, column):
        if not self.hasColumn(column): return "Invalid Column"
        return self.getStd(column) / self.dataFrame.mean()[column]

    def getKurtosis(self, column):
        if not self.hasColumn(column): return "Invalid Column"
        return self.dataFrame.kurtosis()[column]

    def getSkew(self, column):
        if not self.hasColumn(column): return "Invalid Column"
        return self.dataFrame.skew()[column]

    def createExcel(self, data):
        variables = self.prefs["VARS"]
        
        for var in variables:
            data[var] = []
            data[var].append(self.getVariance(var))
            data[var].append(self.getStd(var))
            data[var].append(self.getCV(var))
            data[var].append(self.getKurtosis(var))
            data[var].append(self.getSkew(var))
        
        utils.writeExcel(data, "metrics.xlsx")
        