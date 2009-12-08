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
from bungeni.core.globalsettings import getCurrentParliamentId

from bungeni.ui.utils import get_wf_state

class WhatsOnBrowserView(BrowserView):
    __call__ = ViewPageTemplateFile("templates/whatson.pt")
    interface.implements(IViewView)
    start_date = datetime.date.today()
    end_date = datetime.date.today() + datetime.timedelta(10)
    end_date = datetime.datetime(end_date.year, end_date.month, end_date.day, 23, 59)
            
    def __init__(self, context, request):
        super(WhatsOnBrowserView, self).__init__(context, request)
        parliament_id = getCurrentParliamentId()
        if parliament_id:
            session = Session()
            parliament = session.query(domain.Parliament).get(parliament_id)
            self.context = parliament
            self.context.__parent__ = context
            self.context.__name__ = ""    
        
    def get_end_date(self):
        self.get_items()                   
        end = self.request.form.get( 'end', None)
        if end:
            try:
                end_date  = datetime.datetime.strptime(end,"%Y-%m-%d")
                end_date = datetime.datetime(end_date.year, end_date.month, end_date.day, 23, 59)
                self.end_date = end_date
            except:
                pass
        return self.end_date.strftime("%A %d %B %Y")


    def get_start_date(self):
        start = self.request.form.get( 'start', None)
        if start:
            try:
                start_date = datetime.datetime.strptime(start,"%Y-%m-%d")
                self.start_date = start_date.date()
            except:
                pass
        return self.start_date.strftime("%A %d %B %Y")                                
        
    def get_sittings(self):
        session = Session()   
        query = session.query(domain.GroupSitting).filter(
            sql.and_( schema.sittings.c.status != 'draft',
            sql.between(
                schema.sittings.c.start_date,   
                self.start_date,
                self.end_date))).order_by(
                    schema.sittings.c.start_date).options(
                    eagerload('group'), eagerload('sitting_type'))
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
            if sitting.group.type == 'parliament':
                url = '/archive/browse/parliaments/obj-%i/sittings/obj-%i' % (
                    sitting.group.group_id, sitting.sitting_id)
            elif sitting.group.type == 'committee':
                url = '/archive/browse/parliaments/obj-%i/committees/obj-%i/sittings/obj-%i' % (
                    sitting.group.parent_group_id, sitting.group.group_id, 
                    sitting.sitting_id)                    
            else:
                url ='#'                                    
            s_list.append({
                'start': sitting.start_date.strftime("%H:%M"),
                'end' : sitting.end_date.strftime("%H:%M"),
                'type' : sitting.group.type,
                'name' : sitting.group.short_name,
                'url' : url })
            s_dict['day'] = day
            s_dict['sittings'] = s_list                 
        else:
            if s_dict:
                day_list.append(s_dict)                                                                      
        return day_list

    def get_items(self):
        session = Session()
        start = self.start_date.strftime("%Y-%m-%d")
        end = self.end_date.strftime("%Y-%m-%d 23:59")
        where_clause = "start_date BETWEEN '%s' AND '%s' AND group_sittings_1.status <> 'draft-agenda' " % (start, end)
        query = session.query(domain.ItemSchedule).filter( 
            where_clause).order_by('start_date').options(
                    eagerload('sitting'), eagerload('item'),
                    eagerload('sitting.sitting_type'),
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
                    'status' : get_wf_state(schedule.item),
                    'url' : ('/business/' + schedule.item.type + 's/obj-' + 
                        str(schedule.item.parliamentary_item_id)),  
                    'group_type': schedule.sitting.group.type,
                    'group_name' : schedule.sitting.group.short_name,
                    'sitting_type' : schedule.sitting.sitting_type.sitting_type,
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
        
                
class WhatsOnPortletBrowserView (WhatsOnBrowserView):       
    max_items = 5
    def get_sittings(self):
        return super(WhatsOnPortletBrowserView,
                self).get_sittings()[:self.max_items]
    
    def get_items_by_type(self, item_type):
        return super(WhatsOnPortletBrowserView,
                self).get_items_by_type(item_type)[:self.max_items]
    
    
            
                 
                        

