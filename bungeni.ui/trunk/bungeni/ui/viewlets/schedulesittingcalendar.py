# encoding: utf-8
# Calendar for scheduling sittings
# at the top the committees and sessions available for scheduling are displayed,
# below you have a calendar that displays the sittings
# to schedule the sitting to be scheduled to the date
import datetime
import calendar
import base64
from zope.viewlet import viewlet
from zope.publisher.browser import BrowserView
from zope.viewlet.manager import WeightOrderedViewletManager
import zope.interface
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.traversing.browser.absoluteurl import absoluteURL

from zc.resourcelibrary import need


import sqlalchemy.sql.expression as sql

from ore.alchemist import Session

import bungeni.models.schema as schema
import bungeni.models.domain as domain
import bungeni.core.globalsettings as prefs

from bungeni.ui.utils import getDisplayDate

import interfaces
from schedule import makeList, ScheduledItems, ScheduledQuestionItems, ScheduledMotionItems, ScheduledBillItems, ScheduledAgendaItems

import pdb


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
    # sitting types is a dict for ease of use
    sitting_types = {}
    # initialize some variables
    Date = None
    monthcalendar = None
    monthname =""
    weekcalendar = None
    no_of_columns = 0
    
    def getNextWeek(self):
        td = datetime.timedelta(7)
        return '?date=' + datetime.date.strftime((self.Date + td),'%Y-%m-%d')
        
    def getPrevWeek(self):
        td = datetime.timedelta(7)
        return '?date=' + datetime.date.strftime((self.Date - td),'%Y-%m-%d')        
    
    def getStartDate(self):
        return self.weekcalendar[0]
        
    def getEndDate(self):
        return self.weekcalendar[-1]        
      
    def getWeek(self):
        for week in self.monthcalendar:
            if self.Date in week:
                return week

    def formatDay(self, day):
        return  datetime.date.strftime(day, '%a, %d')

    
    def getSessionTdId( self, day, session_id):        
        return 'stdid_' + datetime.date.strftime(day,'%Y-%m-%d') + '_' + str(session_id)
        
    def getSessionTdClass( self, session_id):
        return 'stdclass_' + str(session_id)
            
    def getCommitteeTdId( self, day, session_id):    
        return 'ctdid_' + datetime.date.strftime(day,'%Y-%m-%d') + '_' + str(session_id)
        
    def getCommitteeTdClass( self,  session_id):    
        return 'ctdclass_' + str(session_id)
        
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
                data['s_type'] =  self.sitting_types[sitting.sitting_type]['type']                    
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
                data['s_type'] =  self.sitting_types[sitting.sitting_type]['type']                      
                data_list.append(data)
        return data_list
        
    def _getSittingTypes( self ):
        """
        returns a dictionary like:
                {
                1:{'start': datetime.time(9,0), 'end':datetime.time(12,0), 'type':'morning' },
                2:{'start': datetime.time(13,0), 'end':datetime.time(18,0), 'type':'afternoon' },
                3:{'start': datetime.time(9,0), 'end':datetime.time(18,0), 'type':'extraordinary' },
                }
        """
        session = Session()
        sitting_types = session.query( domain.SittingType ).all()
        data = {}
        for sitting_type in sitting_types:
            data[sitting_type.sitting_type_id] = {'start': sitting_type.start_time,
                                                  'end': sitting_type.end_time,
                                                  'type': sitting_type.sitting_type }
        return data                                                  
        
         
        
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
        self.week_no = self.Date.isocalendar()[1]                                         
        self.request.response.setCookie('display_date', datetime.date.strftime(self.Date,'%Y-%m-%d') )
        self.monthcalendar = calendar.Calendar(prefs.getFirstDayOfWeek()).monthdatescalendar(self.Date.year,self.Date.month)         
        self.monthname = datetime.date.strftime(self.Date,'%B %Y')
        #self.Data = self.getData()
        self.weekcalendar = self.getWeek()
        self.sessions = self._getSessions()
        self.committees = self._getCommittees()
        self.sittings = self._getSittings()
        self.sitting_types = self._getSittingTypes()
        if self.sessions:
            self.no_of_columns = len(self.sessions) 
        if self.committees:    
            self.no_of_columns = self.no_of_columns + len(self.committees)
    
    
    
    
    render = ViewPageTemplateFile ('templates/schedule_sitting_calendar_viewlet.pt')
    
class ScheduleSittingTypeViewlet ( viewlet.ViewletBase ):
    """
    returns the sitting types that may be scheduled
    with their default times
    """
    render = ViewPageTemplateFile ('templates/schedule_sittingtypes_viewlet.pt')    
    session = Session()
    query = session.query(domain.SittingType)
    name = u"available sitting types"
    list_id = "sitting-types"
    
    def getData(self):
        results = self.query.all()
        data_list = []
        for result in results:
            data ={}
            data["stid"] = "stid_" + str(result.sitting_type_id) + '_' + datetime.time.strftime(result.start_time,'%H-%M') + '_' + datetime.time.strftime(result.end_time,'%H-%M')
            data["stname"] = result.sitting_type            
            data_list.append(data)            
        return data_list

class SittingScheduleDDViewlet( ScheduleSittingCalendar ):
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
    def _isValidSittingDate(self, day, targetOb):
        """
        check if date is in range between start and end
        """        
        if targetOb.start_date:
           if day < targetOb.start_date:
                return False
        if targetOb.end_date:
            if day > targetOb.end_date:
                return False
        return True                                
    
    
    def _getTargets(self):
        targets = []
        for day in self.weekcalendar:
            for session in self.sessions:
                if self._isValidSittingDate(day,session):
                    targets.append( 'stdid_' + datetime.date.strftime(day,'%Y-%m-%d') + '_' + str(session.session_id))
            for committee in self.committees:
                if self._isValidSittingDate(day, committee):
                    targets.append('ctdid_' + datetime.date.strftime(day,'%Y-%m-%d') + '_' + str(committee.committee_id))
        return targets                
                
    def _getList(self):
        id_list = []
        for st_id in self.sitting_types.keys():
            id_list.append( "stid_" + str(st_id) + '_' + 
            datetime.time.strftime(self.sitting_types[st_id]['start'],'%H-%M') + '_' + 
            datetime.time.strftime(self.sitting_types[st_id]['end'],'%H-%M'))
        return id_list            

    def render(self):
        need('yui-dragdrop')
        need('yui-animation')    
        need('yui-logger')    #debug
        targets = self._getTargets()
        
        sitting_type_ids = self._getList()    
            
        DDList = ""
        for stid in sitting_type_ids:            
            #new YAHOO.example.DDList("li" + i + "_" + j);
            DDList = DDList + 'new YAHOO.example.DDList("' + stid +'"); \n'
            
        DDTarget = ""    
        for target in targets:
            #new YAHOO.util.DDTarget("ul"+i);
            DDTarget = DDTarget + 'new YAHOO.util.DDTarget("' + target +'"); \n'
        
        currentDateId = '"tdid-' + datetime.date.strftime(datetime.date.today(),'%Y-%m-%d"')    
        js_inserts= {
            'DDList':DDList,
            'DDTarget':DDTarget,
            'currentDateId': currentDateId }            
                
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
            var el = document.createElement('h5');
            generatedId = destEl.id + "_" + srcEl.id;
            el.id = generatedId;            
            /*el.innerHTML = '<input type="hidden" name="ssi" value="' + generatedId + '" /> ' + el.innerHTML + '<input name="' + generatedId + '_start" type="text" size="5" maxlength="5" value="00:00" /> - <input name="' + generatedId + '_end" type="text" size="5" maxlength="5" value="00:00" />';*/
            el.innerHTML =  proxy.innerHTML;
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
                     ((srcEl.id.substr(0,6) == "ctdid_") ||
                     (srcEl.id.substr(0,6) == "stdid_"))                     
                     ) {
                     var formEl = document.getElementById(srcEl.id + '_form');
                     srcPEl.removeChild(srcEl);                      
                     srcPEl.removeChild(formEl);
                }            
            else if (((destEl.id.substr(0,6) == "ctdid_") ||
                        (destEl.id.substr(0,6) == "stdid_"))
                        &&
                     ((srcEl.id.substr(0,6) == "stdid_") ||
                     (srcEl.id.substr(0,6) == "ctdid_"))) {
                     DDM.refreshCache();
                     return;
                }                                 
            else {     
                destEl.appendChild(el);
                Dom.addClass(el.id, 'dragable');
                YAHOO.example.DDApp.addLi(el.id);
                var formEl = document.createElement('span');                
                var idArr = new Array();
                idArr = el.id.split('_');

                formEl.id = el.id + '_form';                
                formEl.innerHTML = '<input type="hidden" name="ssi" value="' + generatedId + '" /> ' +
                                    '<input name="start_' + generatedId + '" type="text" size="5" maxlength="5" value="' + idArr[5].replace('-',':') + '" />' + 
                                    ' - <input name="end_' + generatedId + '" type="text" size="5" maxlength="5" value="' + idArr[6].replace('-',':') + '" />';
                destEl.appendChild(formEl);
                Dom.setStyle(formEl.id, "white-space", "nowrap");
                destDD.isEmpty = false; 
                };
            DDM.refreshCache(); 
    },
    


    onDragEnter: function(e, id) {        
        var destEl = Dom.get(id);

        if ((destEl.nodeName.toLowerCase() == "td") ||
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

         if ((destEl.nodeName.toLowerCase() == "td")||
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
        return js_string % js_inserts        


class ScheduleSittingSubmitViewlet ( viewlet.ViewletBase ):
    """
    this only gets the posted values and inserts them into the db           
    and reports any errors the might occur
    """
    errors = []
       
    def scheduleSitting(self, scstr, start, end):
        l = scstr.split('_')
        d = l[1].split('-')
        s = start.split(':')
        e = end.split(':')
        start_date = datetime.datetime(int(d[0]), int(d[1]), int(d[2]), int(s[0]), int(s[1]))
        end_date = datetime.datetime(int(d[0]), int(d[1]), int(d[2]), int(e[0]), int(e[1]))
        gsid = long(l[2])
        assert(l[3] == 'stid')  
        stid = long(l[4])  
        session = Session()              
        if l[0] == 'stdid':
            #TODO validate -> form validation
            sitting = domain.GroupSitting()
            sitting.group_id = None
            sitting.session_id = gsid
            sitting.start_date = start_date
            sitting.end_date = end_date
            sitting.sitting_type = stid
            session.save(sitting)
        elif l[0] == 'ctdid':  
            sitting = domain.GroupSitting()
            sitting.group_id = gsid
            sitting.session_id = None
            sitting.start_date = start_date
            sitting.end_date = end_date
            sitting.sitting_type = stid
            session.save(sitting)                    
        else:                       
            raise NotImplementedError    
        
    def insert_items(self, form):
        if form.has_key('ssi'):
            scheduleitems = makeList(form['ssi'])
            for k in scheduleitems:                
                start = form['start_' + k ]    
                end = form['end_' + k]
                self.scheduleSitting(k, start, end)               
                
    
    def update(self):
        if self.request.form:
            if self.request.form.has_key('save'):
                self.insert_items(self.request.form)   
        
    render =  ViewPageTemplateFile ('templates/schedule_sitting_submit_viewlet.pt')


class WeekCalendar(BrowserView):
    __call__ = ViewPageTemplateFile("templates/week_sittings.pt")

class WeekAtomCalendar(BrowserView):
    """
    an atom view of the calendar - just to display in plone
    """
    __call__ = ViewPageTemplateFile("templates/week_atom_sittings.pt")
    
    
    def feedtitle(self):            
        return "Weekly Calendar"
            
    def feedUid(self):
        return  absoluteURL( self.context, self.request ) + '.xml'
               
    def uid(self):     
        #XXX       
        return "urn:uuid:" + base64.urlsafe_b64encode('sitting-week-calendar:' + datetime.datetime.now().isoformat() )
        
    def url(self):    
        return absoluteURL( self.context, self.request )       
        
    def updated(self):
        return datetime.datetime.now().isoformat()    
            

class WeekCalendarViewletManager( WeightOrderedViewletManager ):
    """
    manage the viewlets that make up the calendar view
    """
    zope.interface.implements(interfaces.IWeekSittingCalendar) 


class SittingItemsWeekCalendar( ScheduleSittingCalendar ):
    """
    whats on: give an overview over all items scheduled for sittings that
    week
    """
    
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
                data['subject'] = u'Q ' + str(result.question_number) + u' ' +  result.subject[:10] + u'... '
                data['title'] = result.subject
                data['type'] = "question"
                data['schedule_date_class'] = 'sc-after-' + datetime.date.strftime(result.approval_date + q_offset, '%Y-%m-%d')
                data['url'] = '/questions/obj-' + str(result.question_id)
            elif type(result) == ScheduledMotionItems:    
                data['subject'] = u'M ' + str(result.motion_number) + u' ' +result.title[:10] + u'... '
                data['title'] = result.title
                data['type'] = "motion"                
                data['schedule_date_class'] = 'sc-after-' + datetime.date.strftime(result.approval_date, '%Y-%m-%d')
                data['url'] = '/motions/obj-' + str(result.motion_id)
            elif type(result) == ScheduledBillItems:    
                data['subject'] = u"B " + result.title[:10]  + u'... '
                data['title'] = result.title             
                data['type'] = "bill"
                data['schedule_date_class'] = 'sc-after-' + datetime.date.strftime(result.publication_date + q_offset, '%Y-%m-%d')
                data['url'] = '/bills/obj-' + str(result.bill_id)
            elif type(result) == ScheduledAgendaItems:    
                data['subject'] = u"" + result.title[:10]  + u'... '
                data['title'] = result.title             
                data['type'] = "agenda_item"
                data['schedule_date_class'] = 'sc-after-' + datetime.date.strftime(datetime.date.today(), '%Y-%m-%d')
                data['url'] = '/agendaitems/obj-' + str(result.agenda_item_id)                
                
            data['status'] = result.status
            data_list.append(data)            
        return data_list    
        
    render =  ViewPageTemplateFile ('templates/week_calendar_viewlet.pt')        
    
