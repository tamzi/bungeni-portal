from time import mktime
from datetime import datetime
from datetime import time

class base:
    def __getitem__(self, key):
        """Standard `strftime()` substitutions."""

        try:
            key = str(key)
        except UnicodeDecodeError:
            raise KeyError(key)
        
        result = self.strftime("%"+str(key))
        
        if result == "":
            raise KeyError(key)

        return result    

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

class timedict(time, base):
    pass

class datetimedict(datetime, base):
    @classmethod
    def fromdatetime(self, dt):
        return datetimedict(
            dt.year, dt.month, dt.day,
            dt.hour, dt.minute, dt.second)

    @classmethod
    def fromdate(self, dt):
        return datetimedict(
            dt.year, dt.month, dt.day)

    def __add__(self, other):
        return datetimedict.fromdatetime(datetime.__add__(self, other))

    def __sub__(self, other):
        return datetimedict.fromdatetime(datetime.__sub__(self, other))

    def totimestamp(self):
        return mktime(self.timetuple())

    
