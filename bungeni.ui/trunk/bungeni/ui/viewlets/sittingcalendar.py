# encoding: utf-8
import calendar
import datetime, time

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.publisher.browser import BrowserView
from zope.viewlet.manager import WeightOrderedViewletManager
from zope.viewlet import viewlet
import zope.interface
from zope.security import proxy

from zc.resourcelibrary import need

import sqlalchemy.sql.expression as sql

from ore.alchemist.container import stringKey

from ore.alchemist import Session

from interfaces import ISittingCalendar
from bungeni.ui.utils import getDisplayDate
import bungeni.core.schema as schema
import bungeni.core.domain as domain
from bungeni.ui.browser import container
import bungeni.core.globalsettings as prefs
from schedule import makeList, ScheduledItems, ScheduledQuestionItems, ScheduledMotionItems, ScheduledBillItems


def start_DateTime( Date, context ):
    """
    return the start datetime for the query
    i.e. first of month 00:00
    """
    cal = calendar.Calendar(prefs.getFirstDayOfWeek())
    mcal = cal.monthdatescalendar(Date.year,Date.month)
    firstday = mcal[0][0]
    if context.__parent__:
        if context.__parent__.start_date:
            if firstday < context.__parent__.start_date:
                firstday = context.__parent__.start_date            
    return datetime.datetime(firstday.year, firstday.month, firstday.day, 0, 0, 0)
    
    
    
def end_DateTime( Date, context ):
    """
    return the end datetime for the query
    i.e. last of month 23:59
    """
    cal = calendar.Calendar(prefs.getFirstDayOfWeek())
    mcal = cal.monthdatescalendar(Date.year,Date.month)
    lastday = mcal[-1][-1]
    if context.__parent__:
        if context.__parent__.end_date:
            if lastday > context.__parent__.end_date:
                lastday = context.__parent__.end_date        
    return datetime.datetime(lastday.year, lastday.month, lastday.day, 23, 59, 59)
           
                

class Calendar(BrowserView):
    __call__ = ViewPageTemplateFile("templates/sittings.pt")


class SittingCalendarViewletManager( WeightOrderedViewletManager ):
    """
    manage the viewlets that make up the calendar view
    """
    zope.interface.implements(ISittingCalendar) 
    
class SittingSessionTypesViewlet( viewlet.ViewletBase ):    
    """
    display the available sitting types for scheduling
    """
    render = ViewPageTemplateFile ('templates/schedule_sittings_viewlet.pt')    
    session = Session()
    query = session.query(domain.SittingType)
    name = u"available sitting types"
    list_id = "sitting-types"
    
    def getData(self):
        results = self.query.all()
        data_list = []
        for result in results:
            data ={}
            data["stid"] = "stid_" + str(result.sitting_type_id)
            data["stname"] = result.sitting_type
            data_list.append(data)            
        return data_list
    
class SittingScheduleDDViewlet( viewlet.ViewletBase ):
    """
    returns the js for sitting schedule
    if a sitting is dropped on the calendar a li element 
    is created with the inner html of the dropped element + an input
    element of type checkbox with the value : date of sitting + sitting type id.
    name of the input element is sitting-schedule.
    id of the <li> is  const string + date of sitting + sitting type id.
    
    on update get the 1st and last day of the calendar
    add dd-targets for each day of the calendar
    
    on dragdrop check if an element of the same id as the above generated id exists, if yes
    do not allow drop, else create the element.    
    """
    Date = datetime.date.today() 
    
    def get_parent_endDate(self):
        """
        get the end date of the parent object
        """
        if self.context.__parent__ is not None:
            return self.context.__parent__.end_date
        else:
            return datetime.date.today()    
    
    def render(self):
        self.Date = getDisplayDate(self.request)
        if not self.Date:
            self.Date = self.get_parent_endDate() 
            if not self.Date:
                self.Date=datetime.date.today()    
        sitting_type_ids = []
        sitting_days = []
        need('yui-dragdrop')
        need('yui-animation')    
        need('yui-logger')    #debug
        session=Session()
        results = session.query(domain.SittingType).all()  
        for result in results:   
            sitting_type_ids.append(result.sitting_type_id)
        startDate = start_DateTime(self.Date,self.context).date()
        endDate = end_DateTime(self.Date, self.context).date()
        for day in calendar.Calendar(prefs.getFirstDayOfWeek()).itermonthdates(self.Date.year, self.Date.month):
            if startDate <= day <= endDate:
                sitting_days.append(day)
        js_string = """
<script type="text/javascript">
<!--
(function() {

var Dom = YAHOO.util.Dom;
var Event = YAHOO.util.Event;
var DDM = YAHOO.util.DragDropMgr;    
    
YAHOO.example.DDApp = {
    init: function() {


        %(DDTarget)s
        %(DDList)s     
          
        YAHOO.widget.Logger.enableBrowserConsole();   
    },      
    addLi: function(id) {
       new YAHOO.example.DDList(id); 
    },   
};

YAHOO.example.DDList = function(id, sGroup, config) {

    YAHOO.example.DDList.superclass.constructor.call(this, id, sGroup, config);

    this.logger = this.logger || YAHOO;
    var el = this.getDragEl();
    Dom.setStyle(el, "opacity", 0.67); // The proxy is slightly transparent


    
};



YAHOO.extend(YAHOO.example.DDList, YAHOO.util.DDProxy, {


    startDrag: function(x, y) {
        this.logger.log(this.id + " startDrag");
        // make the proxy look like the source element
        var dragEl = this.getDragEl();
        var clickEl = this.getEl();                                       
        Dom.setStyle(clickEl, "visibility", "hidden");
        dragEl.innerHTML = clickEl.innerHTML;    
        Dom.setStyle(dragEl, "color", Dom.getStyle(clickEl, "color"));
        Dom.setStyle(dragEl, "backgroundColor", Dom.getStyle(clickEl, "backgroundColor"));
        Dom.setStyle(dragEl, "border", "2px solid gray");      
        
    },
    
    endDrag: function(e) {
        var srcEl = this.getEl();
        var proxy = this.getDragEl();
        var proxyid = proxy.id;
        var thisid = this.id;      
        Dom.setStyle(proxyid, "visibility", "hidden");
        Dom.setStyle(thisid, "visibility", "");     
    },    

    onDragDrop : function(e,id) { 
            var srcEl = this.getEl();
            var srcPEl = srcEl.parentNode;
            var destEl = Dom.get(id);
            var destDD = DDM.getDDById(id);
            if (destEl.nodeName.toLowerCase() == "li") {
                    destEl = destEl.parentNode; 
                };                
            var proxy = this.getDragEl();               
            Dom.removeClass(id, 'dragover');
            var el = srcEl.cloneNode(true);
            generatedId = destEl.id + "_" + srcEl.id
            el.id = generatedId;
            el.innerHTML = '<input type="hidden" name="ssi" value="' + generatedId + '" /> ' + el.innerHTML;
            Dom.setStyle(el, "visibility", "");
            if (document.getElementById(generatedId) != null) {
                    var a = new YAHOO.util.Motion( 
                        proxy, { 
                            points: { 
                                to: Dom.getXY(srcEl)
                            }
                        }, 
                        0.2, 
                        YAHOO.util.Easing.easeOut 
                    )
                    Dom.addClass(id, 'invalid-dragover')
                    var proxyid = proxy.id;
                    var thisid = this.id;      
                    alert ("A sitting of this type is already scheduled for this day");
                    // Hide the proxy and show the source element when finished with the animation
                    a.onComplete.subscribe(function() {
                            Dom.setStyle(proxyid, "visibility", "hidden");
                            Dom.setStyle(thisid, "visibility", "");
                            Dom.removeClass(id, 'invalid-dragover');
                        });
                    a.animate();                                                    
                }
            else if ((destEl.id == 'sitting-types') &&
                     (srcEl.id.substr(0,5) == "stid_")) {    
                     DDM.refreshCache();
                     return;                 
                }           
            else if ((destEl.id == 'sitting-types') &&
                     (srcEl.id.substr(0,5) == "dlid_")) {
                     srcPEl.removeChild(srcEl);                      
                }            
            else if ((destEl.id.substr(0,5) == "dlid_") &&
                     (srcEl.id.substr(0,5) == "dlid_")) {
                     DDM.refreshCache();
                     return;
                }                                 
            else {     
                destEl.appendChild(el);
                YAHOO.example.DDApp.addLi(el.id);
                destDD.isEmpty = false; 
                };
            DDM.refreshCache(); 
    },
    


    onDragEnter: function(e, id) {        
        var destEl = Dom.get(id);

        if ((destEl.nodeName.toLowerCase() == "ol") ||
            (destEl.nodeName.toLowerCase() == "ul")) {            
            Dom.addClass(id, 'dragover');
            }            
        if (destEl.nodeName.toLowerCase() == "li") {
            var pEl = destEl.parentNode;
            if (pEl.nodeName.toLowerCase() == "ol") {                
                Dom.addClass(pEl.id, 'dragover');
                }
            }
        
    },

   
   
   onDragOut: function(e, id) {        
        var destEl = Dom.get(id);

         if ((destEl.nodeName.toLowerCase() == "ol")||
            (destEl.nodeName.toLowerCase() == "ul")) {
             Dom.removeClass(id, 'dragover');
             Dom.removeClass(id, 'invalid-dragover');
            }            
        if (destEl.nodeName.toLowerCase() == "li") {
            var pEl = destEl.parentNode;
            if (pEl.nodeName.toLowerCase() == "ol") {
                 //Dom.removeClass(pEl.id, 'dragover');
                }
            }        
    },

    });
Event.onDOMReady(YAHOO.example.DDApp.init, YAHOO.example.DDApp, true);
})();
-->        
</script>       
        """
        DDList = ""
        for qid in sitting_type_ids:            
            #new YAHOO.example.DDList("li" + i + "_" + j);
            DDList = DDList + 'new YAHOO.example.DDList("stid_' + str(qid) +'"); \n'
        DDTarget = ""    
        for day in sitting_days:
            #new YAHOO.util.DDTarget("ul"+i);
            DDTarget = DDTarget + 'new YAHOO.util.DDTarget("dlid_' + datetime.date.strftime(day,'%Y-%m-%d')  +'"); \n'
        
        currentDateId = '"tdid-' + datetime.date.strftime(datetime.date.today(),'%Y-%m-%d"')    
        js_inserts= {
            'DDList':DDList,
            'DDTarget':DDTarget,
            'currentDateId': currentDateId }
        return js_string % js_inserts        

class SittingCalendarViewlet( viewlet.ViewletBase ):
    """
    display a calendar with all sittings in a month
    """
    default_time_dict ={}
    
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
        show only the sittings in the selected month
        and session or group context, or if the calendar is
        called outside get all items for this month
        """
        try:
            session_id = self.context.__parent__.session_id        
            return sql.and_( schema.sittings.c.start_date.between(start_DateTime( self.Date, self.context ), end_DateTime( self.Date, self.context )),
                        schema.sittings.c.session_id == session_id)
        except:
            try:
                group_id  = self.context.__parent__.group_id  
                return sql.and_( schema.sittings.c.start_date.between(start_DateTime( self.Date, self.context ), end_DateTime( self.Date, self.context )),
                        schema.sittings.c.group_id == group_id)   
                
            except:
                return schema.sittings.c.start_date.between(start_DateTime( self.Date, self.context ), end_DateTime( self.Date, self.context )) 
        
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

    def fullPath(self):
        return container.getFullPath(self.context)   
        
    def getDefaults(self):
        """
            self.default_time_dict ={
                1:{'start': datetime.time(9,0), 'end':datetime.time(12,0) },
                2:{'start': datetime.time(13,0), 'end':datetime.time(18,0) },
                3:{'start': datetime.time(9,0), 'end':datetime.time(18,0) },
                }
        """
        self.sit_types ={}
        self.default_time_dict = {}
        type_results = self.type_query.all()
        for sit_type in type_results:
            self.sit_types[sit_type.sitting_type_id] = sit_type.sitting_type
            self.default_time_dict[sit_type.sitting_type_id] = {'start': sit_type.start_time,
                                                                'end': sit_type.end_time}
            
        
    def getData(self):
        """
        return the data of the query
        """            
        data_list=[]      
        path = self.fullPath()       
        results = self.query.all()
        for result in results:            
            data ={}
            data['sittingid']= ('sid_' + str(result.sitting_id) )  
            data['url']= ( path + 'obj-' + str(result.sitting_id) )                         
            data['short_name'] = ( datetime.datetime.strftime(result.start_date,'%H:%M')
                                    + ' (' + self.sit_types[result.sitting_type] + ')')
            data['start_date'] = str(result.start_date)
            data['end_date'] = str(result.end_date)
            data['day'] = result.start_date.date()
            data['did'] = ('dlid_' +  datetime.datetime.strftime(result.start_date,'%Y-%m-%d') +
                           '_stid_' + str( result.sitting_type))  
            data['sid'] = result.sitting_id                         
            data_list.append(data)            
        return data_list

    def GetSittings4Day(self, day):
        """
        return the sittings for that day
        """
        day_data=[]
        for data in self.Data:
            if data['day'] == day:
                day_data.append(data)
        return day_data                
       
    def getActiveSittingItems(self, sitting_id):
        """
        return all questions assigned to that sitting
        """
        session = Session()
        active_sitting_items_filter = sql.and_(schema.items_schedule.c.sitting_id == sitting_id, 
                                                schema.items_schedule.c.active == True)
        items = session.query(ScheduledItems).filter(active_sitting_items_filter).order_by(schema.items_schedule.c.order)
        data_list=[] 
        results = items.all()
        q_offset = datetime.timedelta(prefs.getNoOfDaysBeforeQuestionSchedule())
        for result in results:            
            data ={}
            #data['qid']= ( 'q_' + str(result.question_id) ) 
            data['schedule_id'] = ( 'isid_' + str(result.schedule_id) ) # isid for ItemSchedule ID 
            if type(result) == ScheduledQuestionItems:                       
                data['subject'] = u'Q ' + str(result.question_number) + u' ' +  result.subject[:10]
                data['title'] = result.subject
                data['type'] = "question"
                data['schedule_date_class'] = 'sc-after-' + datetime.date.strftime(result.approval_date + q_offset, '%Y-%m-%d')
                data['url'] = '/questions/obj-' + str(result.question_id)
            elif type(result) == ScheduledMotionItems:    
                data['subject'] = u'M ' + str(result.motion_number) + u' ' +result.title[:10]
                data['title'] = result.title
                data['type'] = "motion"                
                data['schedule_date_class'] = 'sc-after-' + datetime.date.strftime(result.approval_date, '%Y-%m-%d')
                data['url'] = '/motions/obj-' + str(result.motion_id)
            elif type(result) == ScheduledBillItems:    
                data['subject'] = u"B " + result.title[:10]  
                data['title'] = result.title             
                data['type'] = "bill"
                data['schedule_date_class'] = 'sc-after-' + datetime.date.strftime(result.publication_date + q_offset, '%Y-%m-%d')
                data['url'] = '/bills/obj-' + str(result.bill_id)
            data['status'] = result.status
            data_list.append(data)            
        return data_list       
       
       
    def getDayClass(self, day):
        """
        return the class settings for that calendar day
        """
        css_class = ""
        if self.Date.month != day.month:
            css_class = css_class + "other-month " 
        elif day < self.startDate or day > self.endDate:
             css_class = css_class + "other-month "                       
        if day < datetime.date.today():
            css_class = css_class + "past-date "    
        if day == datetime.date.today():
            css_class = css_class + "current-date "  
        if day.weekday() in prefs.getWeekendDays():
            css_class = css_class + "weekend-date "             
        session = Session()    
        query = session.query(domain.HolyDay).filter(schema.holydays.c.holyday_date == day)
        results = query.all()
        if results:        
            css_class = css_class + "holyday-date "          
        return css_class.strip()

    def getDayId(self, day):
        """
        return the id for that calendar day
        """
        return "dlid_" + datetime.date.strftime(day,'%Y-%m-%d')

    def getWeekNo(self, Date):
        """
        return the weeknumber for a given date
        """
        return Date.isocalendar()[1]


    def isSessionDate(self, day):
        return self.startDate <= day <= self.endDate
    
    def insert_items(self, form):   
        if form.has_key('ssi'): 
            item_ids = makeList(form['ssi'])                                    
            session=Session()
            for item_id in item_ids:
                values = item_id.split('_')
                assert( values[0] == 'dlid')
                assert( values[2] == 'stid')
                dt = time.strptime(values[1],'%Y-%m-%d')
                y = dt[0]
                m = dt[1]
                d = dt[2]
                st=long(values[3])
                sitting = domain.GroupSitting()
                sitting.start_date = datetime.datetime(y,m,d, self.default_time_dict[st]['start'].hour, 
                                                        self.default_time_dict[st]['start'].minute)
                sitting.end_date = datetime.datetime(y,m,d, self.default_time_dict[st]['end'].hour, 
                                                        self.default_time_dict[st]['end'].minute)
                sitting.sitting_type = long(values[3])
                try:
                    sitting.session_id = self.context.__parent__.session_id
                except:                    
                    sitting.group_id = self.context.__parent__.group_id   
                session.save(sitting)
                
       
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
        self.startDate = start_DateTime(self.Date,self.context).date()
        self.endDate = end_DateTime(self.Date, self.context).date() 
        self.getDefaults()
        if self.request.form:
            if self.request.form.has_key('save'):
                self.insert_items(self.request.form)         
        query=context._query
        self.query=query.filter(self.get_filter()).order_by('start_date')
        #print str(query)
        self.monthcalendar = calendar.Calendar(prefs.getFirstDayOfWeek()).monthdatescalendar(self.Date.year,self.Date.month)
        self.monthname = datetime.date.strftime(self.Date,'%B %Y')
        self.Data = self.getData()
    
    render = ViewPageTemplateFile ('templates/sitting_calendar_viewlet.pt')
    
