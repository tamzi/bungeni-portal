#
import datetime
from zope import interface
from zope.publisher.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile

from ore.alchemist import Session
from sqlalchemy.orm import eagerload, lazyload
import sqlalchemy.sql.expression as sql

from ploned.ui.interfaces import IViewView
from bungeni.models import domain, schema

class WhatsOnBrowserView(BrowserView):
    __call__ = ViewPageTemplateFile("templates/whatson.pt")
    interface.implements(IViewView)
    start_date = datetime.date.today()
    end_date = datetime.date.today() + datetime.timedelta(10)
    
    def get_date_range(self):
        start = self.request.form.get( 'start', None)
        end = self.request.form.get( 'end', None)
        if (start != None) and (end != None):
            try:
                start_date = datetime.datetime.strptime(start,"%Y-%m-%d")
                end_date  = datetime.datetime.strptime(end,"%Y-%m-%d")
                self.start_date = start_date.date()
                self.end_date = end_date.date()
            except:
                pass
        start_end = (self.start_date.strftime("%A %d %B %Y - ") +
            self.end_date.strftime("%A %d %B %Y"))
        self.get_items()            
        return start_end            
        
    def get_sittings(self):
        session = Session()        
        query = session.query(domain.GroupSitting).filter(
            sql.between(
                schema.sittings.c.start_date,   
                self.start_date,
                self.end_date)).order_by(
                    schema.sittings.c.start_date).options(
                    eagerload('group'))
        sittings = query.all()
        day = u''
        day_list = []
        s_dict = {}
        for sitting in sittings:
            sday = sitting.start_date.strftime("%A %d %B %Y")
            if sday != day:
                s_list = []
                day = sday
                if s_dict:
                    day_list.append(s_dict)
                s_dict = {}
            s_list.append({
                'start': sitting.start_date.strftime("%H:%M"),
                'end' : sitting.end_date.strftime("%H:%M"),
                'type' : sitting.group.type,
                'name' : sitting.group.short_name })
            s_dict['day'] = day
            s_dict['sittings'] = s_list                               
                                
        return day_list

    def get_items(self):
        session = Session()
        start = self.start_date.strftime("%Y-%m-%d")
        end = self.end_date.strftime("%Y-%m-%d")
        where_clause = "start_date BETWEEN '%s' AND '%s'" % (start, end)
        query = session.query(domain.ItemSchedule).filter( 
            where_clause).order_by('start_date').options(
                    eagerload('sitting'), eagerload('item'),
                    lazyload('item.owner'))
        self.itemschedules = query.all()                            
                
    def get_items_by_type(self, item_type):
        day = u''
        day_list = []
        s_dict = {}
        for schedule in self.itemschedules:
            if type(schedule.item) == item_type:
                sday = schedule.sitting.start_date.strftime("%A %d %B %Y")
                if sday != day:
                    s_list = []
                    day = sday
                    if s_dict:
                        day_list.append(s_dict)
                    s_dict = {}
                s_list.append({
                    'name': schedule.item.short_name,
                    'status' : schedule.item.status,
                    'url' : ('/business/' + schedule.item.type + 's/obj-' + 
                        str(schedule.item.parliamentary_item_id))
                     })
                s_dict['day'] = day
                s_dict['items'] = s_list     
        if s_dict:
            day_list.append(s_dict)                           
        return day_list
        
    def get_questions(self):
        return self.get_items_by_type(domain.Question)
        
    def get_bills(self):
        return self.get_items_by_type(domain.Bill)
        
    def get_motions(self):
        return self.get_items_by_type(domain.Motion)                
        
                
                        
                        

