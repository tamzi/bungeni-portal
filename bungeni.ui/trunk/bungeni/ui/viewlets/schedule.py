# encoding: utf-8
# Calendar for scheduling questions
# at the top the questions available for scheduling are displayed,
# below you have a calendar that displays the sittings
# to schedule drag the question to be scheduled to the sitting

import calendar
import datetime
from types import *

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.publisher.browser import BrowserView
from zope.viewlet.manager import WeightOrderedViewletManager
from zope.viewlet import viewlet
import zope.interface
from zope.security import proxy
from zope.formlib import form
from ore.alchemist.container import stringKey
from zc.resourcelibrary import need
from ore.alchemist import Session
from ore.workflow.interfaces import IWorkflowInfo

from interfaces import IScheduleCalendar
from bungeni.ui.utils import getDisplayDate
import bungeni.core.schema as schema
import bungeni.core.domain as domain
from bungeni.ui.browser import container
from bungeni.core.workflows.question import states

import sqlalchemy.sql.expression as sql

import pdb

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
  
def current_sitting_query(date):
    """
    get the current session and return all sittings for that session.
    """    
    session=Session()
    cdfilter = sql.or_(
        sql.between(date, schema.parliament_sessions.c.start_date, schema.parliament_sessions.c.end_date),
        sql.and_( schema.parliament_sessions.c.start_date <= date, schema.parliament_sessions.c.end_date == None)
        )
    try:    
        query = session.query(domain.ParliamentSession).filter(cdfilter)[0]
    except:
        #No current session
        query = None
    results = query
    if results:
        # we are in a session
        session_id = results.session_id
    else:
        # no current session, get the next one
        try:                    
            query = session.query(domain.ParliamentSession
                            ).filter(
                            schema.parliament_sessions.c.start_date >= date
                            ).order_by(
                            schema.parliament_sessions.c.start_date)[0]
        except:
            #No next session
            query = None
        results = query                              
        if results:
            session_id = results.session_id
            date = results.start_date
        else:
            #no current and no next session so just get the last session
            try:                                
                query = session.query(domain.ParliamentSession
                                ).order_by(
                                schema.parliament_sessions.c.end_date.desc())[0]  
            except:
                #No last Session
                query = None
            results = query                            
            if results:
                session_id = results.session_id
                date = results.start_date
            else:
                # No session found
                date = datetime.date.today()
                session_id = -1 # None is not an option because group sittings (committees) do not have sessions                
    gsfilter = sql.and_(
                schema.sittings.c.start_date.between(start_DateTime( date ), end_DateTime( date )),
                schema.sittings.c.session_id == session_id)                                        
    gsquery =  session.query(domain.GroupSitting).filter(gsfilter).order_by(schema.sittings.c.start_date)      
    return gsquery, date        
            

class Calendar(BrowserView):
    __call__ = ViewPageTemplateFile("templates/schedule.pt")


class ScheduleCalendarViewletManager( WeightOrderedViewletManager ):
    """
    manage the viewlets that make up the calendar view
    """
    zope.interface.implements(IScheduleCalendar) 


class YUIDragDropViewlet( viewlet.ViewletBase ):
    """
    get the javascript for the YUI Drag and Drop
    """    
    approved_question_ids = []
    postponed_question_ids =[]
    scheduled_question_ids = []
    sitting_ids =[]
    
    
    
    def update(self):
        """
        refresh the query
        """
        self.approved_question_ids = []
        self.postponed_question_ids =[]
        self.scheduled_question_ids = []
        self.sitting_ids =[]
        self.Date = getDisplayDate(self.request)
        if not self.Date:
            self.Date=datetime.date.today()                
        session = Session()
        approved_questions = session.query(domain.Question).filter(schema.questions.c.status == states.admissible).distinct()
        results = approved_questions.all()
        for result in results:
            self.approved_question_ids.append(result.question_id)
        sittings, self.Date = current_sitting_query(self.Date)    
        results = sittings.all()     
        for result in results:
            self.sitting_ids.append(result.sitting_id)        
        scheduled_questions = session.query(domain.Question).filter(schema.questions.c.sitting_id.in_(self.sitting_ids)).distinct()
        results = scheduled_questions.all()
        for result in results:
            self.scheduled_question_ids.append(result.question_id)    
            
    
    def render(self):
        need('yui-dragdrop')
        need( 'yui-animation')        
        JScript = """
<div id="user_actions">
 
</div>

<form name="make_schedule" method="POST" action="" enctype="multipart/form-data">
  <input type="button" id="saveButton" value="Save" />
 <input id="form.actions.cancel" class="context" type="submit" value="Cancel" name="cancel"/>
</form>
        
<script type="text/javascript">
(function() {

var Dom = YAHOO.util.Dom;
var Event = YAHOO.util.Event;
var DDM = YAHOO.util.DragDropMgr;

//////////////////////////////////////////////////////////////////////////////
// example app
//////////////////////////////////////////////////////////////////////////////
YAHOO.example.DDApp = {
    init: function() {

        //var rows=3,cols=2,i,j;
        //for (i=1;i<cols+1;i=i+1) {
        //    new YAHOO.util.DDTarget("ul"+i);
        //}

        //for (i=1;i<cols+1;i=i+1) {
        //    for (j=1;j<rows+1;j=j+1) {
        //        new YAHOO.example.DDList("li" + i + "_" + j);
        //    }
        //}

        %(DDTarget)s
        %(DDList)s

        Event.on("saveButton", "click", this.showOrder);        
    },

    showOrder: function() {
        var parseList = function(ul) {
            if (ul != null) {
                var el_option;
                var items = ul.getElementsByTagName("li");
                var el_select = document.createElement('select');
                el_select.multiple = "multiple";  
                el_select.name = ul.id;                                 
                
                for (i=0;i<items.length;i=i+1) {
                   
                    el_option=document.createElement("option");
                    el_option.selected = "selected";
                    el_option.value = items[i].id;
                    el_select.appendChild(el_option);
                }
               
                document.make_schedule.appendChild(el_select)
                return;            
            }
        };

       
        var %(targetList)s;       
         %(parseList)s           
        document.make_schedule.submit("form.actions.save");
    },


};

//////////////////////////////////////////////////////////////////////////////
// custom drag and drop implementation
//////////////////////////////////////////////////////////////////////////////

YAHOO.example.DDList = function(id, sGroup, config) {

    YAHOO.example.DDList.superclass.constructor.call(this, id, sGroup, config);

    this.logger = this.logger || YAHOO;
    var el = this.getDragEl();
    Dom.setStyle(el, "opacity", 0.67); // The proxy is slightly transparent

    this.goingUp = false;
    this.lastY = 0;
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

        // Show the proxy element and animate it to the src element's location
        Dom.setStyle(proxy, "visibility", "");
        var a = new YAHOO.util.Motion( 
            proxy, { 
                points: { 
                    to: Dom.getXY(srcEl)
                }
            }, 
            0.2, 
            YAHOO.util.Easing.easeOut 
        )
        var proxyid = proxy.id;
        var thisid = this.id;

        // Hide the proxy and show the source element when finished with the animation
        a.onComplete.subscribe(function() {
                Dom.setStyle(proxyid, "visibility", "hidden");
                Dom.setStyle(thisid, "visibility", "");
            });
        a.animate();
    },

    onDragDrop: function(e, id) {

        // If there is one drop interaction, the li was dropped either on the list,
        // or it was dropped on the current location of the source element.
        if (DDM.interactionInfo.drop.length === 1) {

            // The position of the cursor at the time of the drop (YAHOO.util.Point)
            var pt = DDM.interactionInfo.point; 

            // The region occupied by the source element at the time of the drop
            var region = DDM.interactionInfo.sourceRegion; 

            // Check to see if we are over the source element's location.  We will
            // append to the bottom of the list once we are sure it was a drop in
            // the negative space (the area of the list without any list items)
            if (!region.intersect(pt)) {
                var destEl = Dom.get(id);
                var destDD = DDM.getDDById(id);
                destEl.appendChild(this.getEl());
                destDD.isEmpty = false;
                DDM.refreshCache();
            }

        }
    },

    onDrag: function(e) {

        // Keep track of the direction of the drag for use during onDragOver
        var y = Event.getPageY(e);

        if (y < this.lastY) {
            this.goingUp = true;
        } else if (y > this.lastY) {
            this.goingUp = false;
        }

        this.lastY = y;
    },

    onDragOver: function(e, id) {
    
        var srcEl = this.getEl();
        var destEl = Dom.get(id);

        // We are only concerned with list items, we ignore the dragover
        // notifications for the list.
        if (destEl.nodeName.toLowerCase() == "li") {
            var orig_p = srcEl.parentNode;
            var p = destEl.parentNode;

            if (this.goingUp) {
                p.insertBefore(srcEl, destEl); // insert above
            } else {
                p.insertBefore(srcEl, destEl.nextSibling); // insert below
            }

            DDM.refreshCache();
        }
    }
});

Event.onDOMReady(YAHOO.example.DDApp.init, YAHOO.example.DDApp, true);

})();

        
</script>         
        """
        DDList = ""
        for qid in self.approved_question_ids:            
            #new YAHOO.example.DDList("li" + i + "_" + j);
            DDList = DDList + 'new YAHOO.example.DDList("q_' + str(qid) +'"); \n'
        for qid in self.postponed_question_ids:
            DDList = DDList + 'new YAHOO.example.DDList("q_' + str(qid) +'"); \n'
        for qid in self.scheduled_question_ids:
            DDList = DDList + 'new YAHOO.example.DDList("q_' + str(qid) +'"); \n'
        DDTarget = ""    
        for sid in self.sitting_ids:
            #new YAHOO.util.DDTarget("ul"+i);
            DDTarget = DDTarget + 'new YAHOO.util.DDTarget("sid_'  + str(sid) +'"); \n'
        #add the hardcoded targets for postponed and admissable list
        DDTarget = DDTarget + 'new YAHOO.util.DDTarget("admissible_questions"); \n'
        #DDTarget = DDTarget + 'new YAHOO.util.DDTarget("postponed_questions"); \n'
        t_list = ""
        for sid in self.sitting_ids:
            # var ul1=Dom.get("ul1"), ul2=Dom.get("ul2"); 
            t_list = t_list + ' sid_'+ str(sid) +'=Dom.get("sid_' + str(sid) + '"),'
        t_list = t_list + 'admissible_questions=Dom.get("admissible_questions")'
        parseList =""
        for sid in self.sitting_ids:
            #parseList(ul1, "List 1") +
            parseList = parseList + 'parseList(sid_'+ str(sid) + '); \n'
        parseList = parseList +  'parseList(admissible_questions);'   
        js_inserts= {
            'DDList':DDList,
            'DDTarget':DDTarget,
            'targetList': t_list,
            'parseList': parseList }
        return JScript % js_inserts           
        
        
        
        
class PostponedQuestionViewlet( viewlet.ViewletBase ):
    """
    display the postponed questions
    """    
    name = states.postponed
    render = ViewPageTemplateFile ('templates/schedule_question_viewlet.pt')    
    list_id = "postponed_questions"
    def getData(self):
        """
        return the data of the query
        """      
        results = self.query.all()
        for result in results:            
            data ={}
            data['id']= ( path + 'q-' + str(result.question_id) )                         
            data['subject'] = result.subject
            data_list.append(data)            
        return data_list
    
    
    def update(self):
        """
        refresh the query
        """
        session = Session()
        questions = session.query(domain.Question).filter(schema.questions.c.status == states.postponed)
        self.query = questions
    
    
class AdmissibleQuestionViewlet( viewlet.ViewletBase ):
    """
    display the admissible questions
    """    
    name = states.admissible
    render = ViewPageTemplateFile ('templates/schedule_question_viewlet.pt')    
    list_id = "admissible_questions"
    def getData(self):
        """
        return the data of the query
        """      
        data_list = []
        results = self.query.all()
        for result in results:            
            data ={}
            data['qid']= ( 'q_' + str(result.question_id) )                         
            data['subject'] = result.subject
            data_list.append(data)            
        return data_list
    
    
    def update(self):
        """
        refresh the query
        """
        session = Session()
        questions = session.query(domain.Question).filter(schema.questions.c.status == states.admissible)
        self.query = questions
    
    
    
class ScheduleCalendarViewlet( viewlet.ViewletBase, form.FormBase ):
    """
    display a calendar with all sittings in a month
    """
    
    @form.action((u"Save"), condition = None)                     
    def handleSaveAction(self, action, data):
        pdb.set_trace()    
        
    @form.action((u"Cancel"))                     
    def handleSaveAction(self, action, data):
        pdb.set_trace()          
    
    
    
        
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
        if the session start date is prior to the current month
        """            
        return ''
        
    def next(self):
        """
        return link to the next month if the end date
        of the session is after the 1st of the next month
        """        
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
        path = ''       
        results = self.query.all()
        for result in results:            
            data ={}
            data['sittingid']= ('sid_' + str(result.sitting_id) )     
            data['sid'] =  result.sitting_id                   
            data['short_name'] = ( datetime.datetime.strftime(result.start_date,'%H:%M')
                                    + ' (' + sit_types[result.sitting_type] + ')')
            data['start_date'] = str(result.start_date)
            data['end_date'] = str(result.end_date)
            data['day'] = int(result.start_date.day)
            data_list.append(data)            
        return data_list

    def getSittingQuestions(self, sitting_id):
        """
        return all questions assigned to that sitting
        """
        session = Session()
        questions = session.query(domain.Question).filter(schema.questions.c.sitting_id == sitting_id)
        data_list=[] 
        results = questions.all()
        for result in results:            
            data ={}
            data['qid']= ( 'q_' + str(result.question_id) )                         
            data['subject'] = result.subject
            data['status'] = result.status
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
       
       
    def schedule_question(self, question_id, sitting_id):
        print question_id, sitting_id
        session = Session()
        question = session.query(domain.Question).get(question_id)
        question.context = self.context
        if question:
            if sitting_id:
                sitting = session.query(domain.GroupSitting).get(sitting_id)
            else:
                sitting = None                
            if sitting:
                if question.sitting_id != sitting_id:
                    question.sitting_id = sitting_id
                elif question.sitting_id is None:    
                    #XXX check_security=True
                    question.sitting_id = sitting_id
                    IWorkflowInfo(question).fireTransition('schedule', check_security=True)
                else:
                    #sitting stays the same
                    print question.sitting_id == sitting_id
            else:
                if question.sitting_id is not None: 
                    #question.sitting_id = sitting_id
                    if IWorkflowInfo(question).state().getState() == states.scheduled:
                        IWorkflowInfo(question).fireTransition('postpone', check_security=True)
                    
    def insert_questions(self, form):
        for sitting in form.keys():
            if sitting[:4] == 'sid_':
                qids = form[sitting]
                sitting_id = long(sitting[4:])                
                if type(qids) == ListType:
                    for qid in qids:
                        if qid[:2] == 'q_':
                            question_id = long(qid[2:])
                            self.schedule_question(question_id, sitting_id)
                if type(qids) in StringTypes:
                    if qids[:2] == 'q_':
                        question_id = long(qids[2:])
                        self.schedule_question(question_id, sitting_id)
            else:
                if sitting == 'admissible_questions':
                    qids = form['admissible_questions']
                    if type(qids) == ListType:
                        for qid in qids:
                            if qid[:2] == 'q_':
                                question_id = long(qid[2:])
                                self.schedule_question(question_id, None)
                    if type(qids) in StringTypes:
                        if qids[:2] == 'q_':
                            question_id = long(qids[2:])
                            self.schedule_question(question_id, None)
       
    def update(self):
        """
        refresh the query
        """
    
        if self.request.form:
            if not self.request.form.has_key('cancel'):
                self.insert_questions(self.request.form) 
                
        self.Date = getDisplayDate(self.request)
        if not self.Date:
            self.Date=datetime.date.today()            
                
        self.query, self.Date = current_sitting_query(self.Date)        
        #print str(query)
        self.request.response.setCookie('display_date', datetime.date.strftime(self.Date,'%Y-%m-%d') )
        self.monthcalendar = calendar.monthcalendar(self.Date.year, self.Date.month)
        self.monthname = datetime.date.strftime(self.Date,'%B %Y')
        self.Data = self.getData()
    
    render = ViewPageTemplateFile ('templates/schedule_calendar_viewlet.pt')
    
