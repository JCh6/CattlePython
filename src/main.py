### main.py

from Log import Log
from usr.prefs import prefs
from CowManager import CowManager

# Main func
def main():
    cm = CowManager(prefs)
    cm.loadCows()
    cm.concatDataFrames()
    cm.heatMap(False)
    print(cm.getDistanceTraveled())
    print(cm.getDistanceTraveledPerDay())

if __name__ == "__main__":
    log = Log()
    log.info("Log ready!")
    main()
