# encoding: utf-8
# Calendar for scheduling sittings
# at the top the committees and sessions available for scheduling are displayed,
# below you have a calendar that displays the sittings
# to schedule the sitting to be scheduled to the date
import datetime
import calendar

from zope.viewlet import viewlet
from zope.publisher.browser import BrowserView
from zope.viewlet.manager import WeightOrderedViewletManager
import zope.interface
from zope.app.pagetemplate import ViewPageTemplateFile

import sqlalchemy.sql.expression as sql

from ore.alchemist import Session

import bungeni.core.schema as schema
import bungeni.core.domain as domain
import bungeni.core.globalsettings as prefs

from bungeni.ui.utils import getDisplayDate

import interfaces

class ScheduleCalendarViewletManager( WeightOrderedViewletManager ):
    """
    manage the viewlets that make up the calendar view
    """
    zope.interface.implements(interfaces.IScheduleSittingCalendar) 
    

class Calendar(BrowserView):
    __call__ = ViewPageTemplateFile("templates/schedule_sittings.pt")

class ScheduleSittingCalendar( viewlet.ViewletBase ):
    # sessions and committees are query results
    sessions = None
    committees = None
    sittings = None
    # initialize some variables
    Date = None
    monthcalendar = None
    monthname =""
    weekcalendar = None
    
    def getStartDate(self):
        return self.weekcalendar[0]
        
    def getEndDate(self):
        return self.weekcalendar[-1]        
      
    def getWeek(self):
        for week in self.monthcalendar:
            if self.Date in week:
                return week

    def formatDay(self, day):
        return  datetime.date.strftime(day, '%a, %d %b %y')

    def getScheduledCommitteeSittings( self, day, committee_id ):
        """
        get the scheduled sittings for that committee and date
        """
        #TODO: test what is faster- query per committee and day
        # or loop thru the resultset
        data_list = []
        for sitting in self.sittings:
            if ((sitting.start_date.date() == day) 
                and (sitting.group_id == committee_id)):
                data ={}
                data['sittingid']= ('sid_' + str(sitting.sitting_id) )  
                #data['url']= ( path + 'obj-' + str(result.sitting_id) )                         
                data['short_name'] = ( datetime.datetime.strftime(sitting.start_date,'%H:%M')
                                        + ' - ' + datetime.datetime.strftime(sitting.end_date,'%H:%M'))
                #data['start_date'] = str(result.start_date)
                #data['end_date'] = str(result.end_date)
                #data['day'] = result.start_date.date()
                #data['did'] = ('dlid_' +  datetime.datetime.strftime(result.start_date,'%Y-%m-%d') +
                #               '_stid_' + str( result.sitting_type))  
                data['sid'] = sitting.sitting_id                         
                data_list.append(data)                               
        return data_list
    
    def getScheduledParliamentSittings( self, day, session_id ):     
        """
        get the sittings scheduled for that day and parliamentary session
        """
        data_list = []
        for sitting in self.sittings:
            if ((sitting.start_date.date() == day) 
                and (sitting.session_id == session_id)):
                
                data ={}
                data['sittingid']= ('sid_' + str(sitting.sitting_id) )  
                #data['url']= ( path + 'obj-' + str(result.sitting_id) )                         
                data['short_name'] = ( datetime.datetime.strftime(sitting.start_date,'%H:%M')
                                        + ' - ' + datetime.datetime.strftime(sitting.end_date,'%H:%M'))
                #data['start_date'] = str(result.start_date)
                #data['end_date'] = str(result.end_date)
                #data['day'] = result.start_date.date()
                #data['did'] = ('dlid_' +  datetime.datetime.strftime(result.start_date,'%Y-%m-%d') +
                #               '_stid_' + str( result.sitting_type))  
                data['sid'] = sitting.sitting_id                         
                data_list.append(data)
        return data_list
        
    def _getSittings( self ):
        firstday = self.getStartDate()    
        lastday = self.getEndDate()
        start_time = datetime.datetime(firstday.year, firstday.month, firstday.day, 0, 0, 0)
        end_time = datetime.datetime(lastday.year, lastday.month, lastday.day, 23, 59, 59)
        session = Session()        
        sittings = session.query( domain.GroupSitting ).filter(
                schema.sittings.c.start_date.between(start_time, end_time)).order_by(schema.sittings.c.start_date)                
        return sittings.all()
        
    def _getCommittees( self ):
        """
        get all committees that are active in this period
        """
        date = self.Date
        session = Session()            
        cdfilter = sql.or_(
            sql.between(date, schema.groups.c.start_date, schema.groups.c.end_date),
            sql.and_( schema.groups.c.start_date <= date, schema.groups.c.end_date == None)
            )
        try:    
            query = session.query(domain.Committee).filter(cdfilter).all()
        except:
            #No current committees
            query = None
        return query
        
    def _getSessions(self):
        """
        get all sessions that are active in this period
        """
        date = self.Date
        session = Session()            
        cdfilter = sql.or_(
            sql.between(date, schema.parliament_sessions.c.start_date, schema.parliament_sessions.c.end_date),
            sql.and_( schema.parliament_sessions.c.start_date <= date, schema.parliament_sessions.c.end_date == None)
            )
        try:    
            query = session.query(domain.ParliamentSession).filter(cdfilter).all()
        except:
            #No current session
            query = None
        return query
        
    def update(self):
        """
        update the queries, get all sessions, sittings, 
        """
        self.errors = []
        #if self.request.form:
        #    if not self.request.form.has_key('cancel'):
        #        self.insert_items(self.request.form) 
                
        self.Date = getDisplayDate(self.request)
        if not self.Date:
            self.Date=datetime.date.today()                                           
        self.request.response.setCookie('display_date', datetime.date.strftime(self.Date,'%Y-%m-%d') )
        self.monthcalendar = calendar.Calendar(prefs.getFirstDayOfWeek()).monthdatescalendar(self.Date.year,self.Date.month)         
        self.monthname = datetime.date.strftime(self.Date,'%B %Y')
        #self.Data = self.getData()
        self.weekcalendar = self.getWeek()
        self.sessions = self._getSessions()
        self.committees = self._getCommittees()
        self.sittings = self._getSittings()
    
    
    
    
    
    render = ViewPageTemplateFile ('templates/schedule_sitting_calendar_viewlet.pt')
    
    
