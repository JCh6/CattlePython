### Log.py

from datetime import datetime

class Log:

    def __init__(self):
        self.init = True

    def fatal(self, msg):
        print(self.getCurrTime(), msg)
        exit(1)
    
    def info(self, msg):
        print(self.getCurrTime(), msg)

    def getCurrTime(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]