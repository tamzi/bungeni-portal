# encoding: utf-8
"""
Support for Recurring Events:

Events may repeat weekly or monthly.
On a weekly basis the weekdays can be selected.
On a monthly basis the day i.e the nth of month or the 
nth weekday of a month can be selected.
"""
import datetime
from dateutil import relativedelta, rrule

import bungeni.core.globalsettings as prefs

def getWeeklyScheduleDates(start, weekdays,  end=None, times=None, edates=[]):
    """
    Returns a dictionary of lists of the Dates that match
    the pattern and dates that were excluded
    
    parameters:
    start: The recurrence start
    weekdays is either an integer or a list of integers where Monday is 0 and Sunday is 6    
    end: date until this event is repeated
    times: integer how many times is this events to be repeated
    edates is a list of dates to exclude 
    
    either end or times must be given!
    """
    for d in edates:
        assert(type(d)==datetime.date)    
        
    assert((end is not None) or (times is not None))
    valid_dates = []
    invalid_dates = []          
    
    weekstart = prefs.getFirstDayOfWeek()
    
    rrule_result = rrule.rrule(rrule.WEEKLY, 
                        dtstart=start, 
                        until=end, 
                        count=times, 
                        byweekday=weekdays,
                        wkst=weekstart)
    for d in rrule_result:       
        if d.date() in edates:
            invalid_dates.append(d.date())
        else:
            valid_dates.append(d.date())
                                    
    return {'valid' : valid_dates,
            'invalid' : invalid_dates}                         
    
def getMonthlyScheduleDates(start, monthday=None, nth=None, weekday=None,  end=None, times=None, edates=[]):
    """
    Returns a dictionary of lists of the Dates that match
    the pattern and dates that were excluded 
    
    start: The recurrence start
    monthday: the day in the month when this event should be scheduled
    i.e 18th
    nth: together with weekdays the nth weekday of a month
    weekday: an integers where 
    Monday is 0 and Sunday is 6    
    end: date until this event is repeated
    times: integer how many times is this events to be repeated
    edates: a list of dates to exclude 
    
    either end or times must be given.
    either monthday or nth and weekdays must be given.
    """
    for d in edates:
        assert(type(d)==datetime.date)    
    assert((end is not None) or (times is not None))        
    assert((monthday is not None) or ((nth is not None) and (weekday is not None)))
    
    if nth is not None:       
        rweekday = rrule.weekdays[weekday](nth)
    else:
        rweekday = None    
    valid_dates = []
    invalid_dates = [] 
    weekstart = prefs.getFirstDayOfWeek()
    rrule_result = rrule.rrule(rrule.MONTHLY, 
                        dtstart=start, 
                        until=end, 
                        count=times, 
                        bymonthday=monthday,
                        byweekday=rweekday,
                        wkst=weekstart)
                        
    for d in rrule_result:       
        if d.date() in edates:
            invalid_dates.append(d.date())
        else:
            valid_dates.append(d.date())    
    
    return {'valid' : valid_dates,
            'invalid' : invalid_dates}             
                
def last_weekday_in_month(day):

    d = day + relativedelta.relativedelta(day=31) - datetime.timedelta(days=7)
    return d >= day
    
def first_weekday_in_month(day):

    d = day + relativedelta.relativedelta(day=1) + datetime.timedelta(days=7)
    return d <= day




