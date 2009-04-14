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

import sqlalchemy.sql.expression as sql
from ore.alchemist import Session

import bungeni.core.globalsettings as prefs
from bungeni.models import domain, schema
from bungeni.ui.i18n import _



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
    return d < day
    
def nth_weekday_in_month(day):
    dd = {1 : _(u'1st'),
          2 : _(u'2nd'),
          3 : _(u'3rd'),
          4 : _(u'4th'),
          5 : _(u'5th'),
          -1 : _(u'last')}


    d = day.day
    md = [{ 'daynum' : (((d - 1)/7) + 1), 'name' : dd[((d - 1)/7) + 1]}]
    if last_weekday_in_month(day):
        md.append({ 'daynum' : -1 , 'name' : dd[-1]})
    return md

def make_date_time( date, time ):
    """ combines the date(portion) of date and time(portion) of time 
    to a datetime object"""
    return datetime.datetime(date.year, date.month, date.day,
            time.hour, time.minute)
    
    

def create_recurrent_sittings(datelist, sitting):
    """ create sittings on the dates given in datelist
    and the data from sitting """
    
    session = Session()
    sitting.recurring_id = sitting.sitting_id
    for date in datelist:
        r_sitting = domain.GroupSitting()
        r_sitting.recurring_id = sitting.sitting_id
        r_sitting.group_id = sitting.group_id
        r_sitting.short_name = sitting.short_name
        r_sitting.start_date = make_date_time(date, sitting.start_date)
        r_sitting.end_date = make_date_time(date, sitting.end_date)
        r_sitting.sitting_type_id = sitting.sitting_type_id
        session.add(r_sitting) 
                
def delete_recurring_sittings(sitting, del_cmd ):
    """Delete recurring sittings
    you may choose to delete all, 
    the current one only
    or future sittings
    """
    session = Session()
    connection = session.connection(domain.GroupSitting)    
    if del_cmd == "FUTURE":
        query = schema.sittings.delete(
            sql.and_( schema.sittings.c.start_date >= sitting.start_date,
                schema.sittings.c.recurring_id ==sitting.recurring_id))      
        connection.execute(query)
    elif del_cmd == "CURRENT":
        session.delete(sitting)
    elif del_cmd == "ALL":
        query = schema.sittings.delete(
            schema.sittings.c.recurring_id == sitting.recurring_id)
        connection.execute(query)                      
    elif del_cmd == "CANCEL":
        pass
    else:
        raise NotImplementedError        

    
    



