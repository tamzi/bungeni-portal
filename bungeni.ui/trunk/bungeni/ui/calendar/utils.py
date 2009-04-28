from datetime import datetime
from datetime import time
from datetime import date
from time import mktime

marker = object()

def timestamp_from_date(date):
    return mktime(date.timetuple())

def pack_date_range(start, end):
    return ";".join(map(
        lambda date: (date and str(int(timestamp_from_date(date))) or ""),
        (start, end)))

def unpack_date_range(value):
    start, end = value.split(';')
    try:
        start = date.fromtimestamp(int(start))
    except (TypeError, ValueError):
        start = None
    try:
        end = date.fromtimestamp(int(end))
    except (TypeError, ValueError):
        end = None

    return start, end

class join_dicts(object):
    def __init__(self, *dicts):
        self.dicts = dicts

    def __getitem__(self, key):
        for d in self.dicts:
            value = d.get(key, marker)
            if value is not marker:
                return value
        raise KeyError(key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
            
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

    
