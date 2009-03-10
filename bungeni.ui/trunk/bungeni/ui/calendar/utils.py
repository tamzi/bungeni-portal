from time import mktime
from datetime import datetime

class datetimedict(datetime):
    @classmethod
    def fromdatetime(self, dt):
        return datetimedict(
            dt.year, dt.month, dt.day,
            dt.hour, dt.minute, dt.second)

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

    def __add__(self, other):
        return datetimedict.fromdatetime(datetime.__add__(self, other))

    def __sub__(self, other):
        return datetimedict.fromdatetime(datetime.__sub__(self, other))

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def totimestamp(self):
        return mktime(self.timetuple())

    
