# encoding: utf-8
import calendar
import datetime

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.publisher.browser import BrowserView
from zope.viewlet.manager import WeightOrderedViewletManager
from zope.viewlet import viewlet
import zope.interface
from zope.security import proxy


from ore.alchemist import Session

from interfaces import ISittingCalendar
from bungeni.ui.utils import getDisplayDate
import bungeni.core.schema as schema
import bungeni.core.domain as domain


def start_DateTime( Date ):
    """
    return the start datetime for the query
    i.e. first of month 00:00
    """
    return datetime.datetime(Date.year, Date.month, 1, 0, 0, 0)
    
    
def end_DateTime( Date ):
    """
    return the end datetime for the query
    i.e. last of month 23:59
    """
    if Date.month == 12:
        month = 1
        year = Date.year + 1
    else:
        month = Date.month + 1
        year = Date.year    
    return datetime.datetime(year, month, 1, 0, 0, 0)  - datetime.timedelta(seconds=1)                
                

class Calendar(BrowserView):
    __call__ = ViewPageTemplateFile("sittings.pt")


class SittingCalendarViewletManager( WeightOrderedViewletManager ):
    """
    manage the viewlets that make up the calendar view
    """
    zope.interface.implements(ISittingCalendar) 
    
class SittingCalendarViewlet( viewlet.ViewletBase ):
    """
    display a calendar with all sittings in a month
    """
    def get_parent_endDate(self):
        """
        get the end date of the parent object
        """
        if self.context.__parent__ is not None:
            return self.context.__parent__.end_date
        else:
            return datetime.date.today()
        
    def get_filter(self):
        """
        show only the sessions in the selected month
        """
                
        return schema.sittings.c.start_date.between(start_DateTime( self.Date ), end_DateTime( self.Date ))
            
        
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.query = None
        self.Date=datetime.date.today()
        self.Data = []
        session = Session()
        self.type_query = session.query(domain.SittingType)
        
    def previous(self):
        """
        return link to the previous month 
        if the parent start date is prior to the current month
        """    
        if self.context.__parent__ is not None:
            psd = self.context.__parent__.start_date
            if psd:
                if psd < datetime.date(self.Date.year, self.Date.month, 1):
                    if self.Date.month == 1:
                        month = 12
                        year = self.Date.year - 1
                    else:
                        month = self.Date.month -1
                        year = self.Date.year  
                    try:
                        prevdate = datetime.date(year,month,self.Date.day)
                    except:
                        # in case we try to move to Feb 31st (or so)                      
                        prevdate = datetime.date(year,month,15)
                    return ('<a href="?date=' 
                            + datetime.date.strftime(prevdate,'%Y-%m-%d') 
                            + '"> &lt;&lt; </a>' )
            else:
                return ''    
        else:
            return ''
        
    def next(self):
        """
        return link to the next month if the end date
        of the parent is after the 1st of the next month
        """
        if self.context.__parent__ is not None:        
            ped = self.context.__parent__.end_date
            if self.Date.month == 12:
                month = 1
                year = self.Date.year + 1
            else:
                month = self.Date.month + 1
                year = self.Date.year
            if ped:               
                if ped >= datetime.date(year, month, 1):
                    try:
                        nextdate = datetime.date(year,month,self.Date.day)
                    except:
                        # if we try to move from 31 of jan to 31 of feb or so
                        nextdate = datetime.date(year,month,15)
                    return ('<a href="?date=' 
                            + datetime.date.strftime(nextdate,'%Y-%m-%d') 
                            + '"> &gt;&gt; </a>' )
                else:
                    return ''                
            else:
                try:
                    nextdate = datetime.date(year,month,self.Date.day)
                except:
                    # if we try to move from 31 of jan to 31 of feb or so
                    nextdate = datetime.date(year,month,15)            
                return ('<a href="?date=' 
                        + datetime.date.strftime(nextdate,'%Y-%m-%d' )
                        + '"> &gt;&gt; </a>' )
        else:
            return ''

    def getData(self):
        """
        return the data of the query
        """
        sit_types ={}
        type_results = self.type_query.all()
        for sit_type in type_results:
            sit_types[sit_type.sitting_type_id] = sit_type.sitting_type
        data_list=[]                
        results = self.query.all()
        for result in results:            
            data ={}
            data['url']= ('obj-' + str(result.sitting_id) )                         
            data['short_name'] = ( datetime.datetime.strftime(result.start_date,'%H:%M')
                                    + ' (' + sit_types[result.sitting_type] + ')')
            data['start_date'] = str(result.start_date)
            data['end_date'] = str(result.end_date)
            data['day'] = int(result.start_date.day)
            data_list.append(data)            
        return data_list

    def GetSittings4Day(self, day):
        """
        return the sittings for that day
        """
        day_data=[]
        for data in self.Data:
            if data['day'] == int(day):
                day_data.append(data)
        return day_data                
       
       
    def update(self):
        """
        refresh the query
        """
        session = Session()
        context = proxy.removeSecurityProxy( self.context )         
        self.Date = getDisplayDate(self.request)
        if not self.Date:
            self.Date = self.get_parent_endDate() 
            if not self.Date:
                self.Date=datetime.date.today()            
            self.request.response.setCookie('display_date', datetime.date.strftime(self.Date,'%Y-%m-%d') )       
        query=context._query
        self.query=query.filter(self.get_filter()).order_by('start_date')
        #print str(query)
        self.monthcalendar = calendar.monthcalendar(self.Date.year, self.Date.month)
        self.monthname = datetime.date.strftime(self.Date,'%B %Y')
        self.Data = self.getData()
    
    render = ViewPageTemplateFile ('sitting_calendar_viewlet.pt')
    
