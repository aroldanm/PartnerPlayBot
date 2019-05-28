import time
import calendar

class Utils():
    @staticmethod
    def currentTimestamp():
        return calendar.timegm(time.gmtime())
