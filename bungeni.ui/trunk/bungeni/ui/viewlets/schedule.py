# encoding: utf-8
# Calendar for scheduling questions
# at the top the questions available for scheduling are displayed,
# below you have a calendar that displays the sittings
# to schedule drag the question to be scheduled to the sitting

import calendar
import datetime, time
from types import ListType, StringTypes

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

from interfaces import IScheduleCalendar, IScheduleItems, IScheduleHolydayCalendar, IPlenaryCalendar
from bungeni.ui.utils import getDisplayDate
import bungeni.core.schema as schema
import bungeni.core.domain as domain
from bungeni.ui.browser import container
from bungeni.core.workflows.question import states as question_wf_state
from bungeni.core.workflows.motion import states as motion_wf_state
from bungeni.core.workflows.bill import states as bill_wf_state
import bungeni.core.globalsettings as prefs



import sqlalchemy.sql.expression as sql
import sqlalchemy as rdb
from sqlalchemy.orm import mapper, polymorphic_union

import simplejson

### debug

import pdb

#Among the “admissible” questions the Speaker or the Clerk's office will select questions for scheduling for a specific sitting 
#(please note, in many parliaments only a fraction of the approved questions are scheduled to be addressed in a sitting).


#For scheduling purposes, the system will retrieve the “admissible” but not yet scheduled questions 
#according to the sequence they were approved by the Speaker's Office or by other criteria set by each parliament.

#The system should not allow questions to be scheduled:

#      on a day the House is not sitting or;

#      on n days after the week in which the question was presented (with an override option)

#      when a different question from the same MP has been scheduled for that particular House sitting 
#      (exception may apply to this rule).

#The system should also store the following parameters:

#      maximum number of days ‘d' that can elapse between the time a question is sent to the relevant Ministry 
#      and the time the question is placed on the Order Paper has to be parameterised;

#      maximum number of questions ‘n' that can be asked in the House per sitting. 
#     (i.e. appear on the Order Paper) will also be parameterised;

#      maximum number of days that may elapse between the days a Minister receives a question and the day a written response 
#      is submitted to the clerk;

#      maximum number of days that may elapse between the day a question by private notice 
#      (questions that in the opinion of the Speaker are of an urgent nature) is scheduled for reply.

#       All scheduled Questions need to be printed/exported to then be forwarded on paper or electronically 
#       to the various Ministries and the relevant offices informing them also of the day in which they are scheduled.
#       Notifications will be sent to the Speaker and the Clerk listing all questions that have exceeded the limits stated above. 


# some joins to get the scheduled items (bills, motions and question) 
# along with their scheduling information

class ScheduledItems ( object ):
    """
    all scheduled items 
    actually no items are returned by this query 
    as schema.items_schedule.c.item_id cannot be null
    we only need it as a base class to inherit from         
    """
    
_scheduled_items = rdb.select([schema.items_schedule], schema.items_schedule.c.item_id ==None).alias('no_scheduled_item')

class ScheduledQuestionItems( ScheduledItems ):
    """
    Questions scheduled for a sitting
    """
    
_scheduled_questions = rdb.join( schema.questions, schema.items_schedule, 
                                schema.questions.c.question_id == schema.items_schedule.c.item_id )
                                


class ScheduledMotionItems ( ScheduledItems ):
    """
    Motions scheduled for a sitting
    """
    
_scheduled_motions = rdb.join( schema.motions, schema.items_schedule, 
                                schema.motions.c.motion_id == schema.items_schedule.c.item_id )
                                


class ScheduledBillItems( ScheduledItems ):
    """
    Bills scheduled for a sitting
    """
    
_scheduled_bills = rdb.join( schema.bills, schema.items_schedule, 
                                schema.bills.c.bill_id == schema.items_schedule.c.item_id )
                                
class ScheduledAgendaItems( ScheduledItems ):
    """
    agenda items for a sitting
    """
_scheduled_agenda_items = rdb.join( schema.agenda_items, schema.items_schedule, 
                                schema.agenda_items.c.agenda_item_id == schema.items_schedule.c.item_id )


#polymorphic join for Concrete Inheritance
#to get all possible objects in one go.

join_scheduled_items = polymorphic_union({
    'items': _scheduled_items,
    'questions': _scheduled_questions,
    'motions': _scheduled_motions,
    'bills': _scheduled_bills,
    'agendaitems':_scheduled_agenda_items}, 
    'type', 'join_scheduled_items')

scheduled_items = mapper(ScheduledItems,  _scheduled_items, 
                        select_table=join_scheduled_items, 
                        polymorphic_on=join_scheduled_items.c.type, polymorphic_identity='items')

scheduled_questionss = mapper(ScheduledQuestionItems,  _scheduled_questions, inherits=scheduled_items, 
                        order_by=schema.questions.c.question_number,                        
                        concrete=True, polymorphic_identity='questions')                        
scheduled_bills = mapper(ScheduledBillItems, _scheduled_bills, inherits=scheduled_items, 
    concrete=True, polymorphic_identity='bills')
scheduled_motions = mapper(ScheduledMotionItems, _scheduled_motions, inherits=scheduled_items, 
    order_by= schema.motions.c.motion_number,
    concrete=True, polymorphic_identity='motions')
scheduled_agenda_items = mapper(ScheduledAgendaItems, _scheduled_agenda_items, inherits=scheduled_items, 
    order_by= schema.agenda_items.c.agenda_item_id,
    concrete=True, polymorphic_identity='agendaitems')


def makeList( itemIds ):

    if type(itemIds) == ListType:
        return itemIds            
    elif type(itemIds) in StringTypes:
        # only one item in this list
        return [itemIds,]
    else:
         raise TypeError ("Form values must be of type string or list")


def getScheduledItem( schedule_id ):
    """
    return the item for a given schedule_id
    """
    session = Session()
    scheduled_item = session.query(scheduled_items).filter(schema.items_schedule.c.schedule_id == schedule_id)[0]
    return scheduled_item


class QuestionJSONValidation( BrowserView ):
    """
    validate if a question can be scheduled for a sitting, 
    """
    def sittingBeforeMotionApproval(self, sitting, motion):
        if sitting.start_date.date() < motion.received_date:
            return "Motion cannot be scheduled before it was recieved"
            
    def sittingBeforeApproval(self, sitting, question ):
        """
        the sitting date is before the question was approved
        so it cannot be scheduled for this sitting
        """
        if sitting is None:
            return
        if sitting.start_date.date() < question.approval_date:
            return "Question cannot be scheduled before it was approved by the clerk"
    
    
    def sittingToEarly(self, sitting, question):
        """
        A question cannot be scheduled on n days after the week in which the question was presented
        """
        if sitting is None:
            return
        noOfDaysBeforeQuestionSchedule = prefs.getNoOfDaysBeforeQuestionSchedule()
        minScheduleDate = question.approval_date + datetime.timedelta(noOfDaysBeforeQuestionSchedule)
        if sitting.start_date.date() < minScheduleDate:
            return "The question may not be scheduled before %s" %( datetime.date.strftime(minScheduleDate,'%Y-%m-%d') )
    
    
    def sittingToManyQuestions(self, question_id, sitting_questions):
        """
        the maximum number of questions in this sitting is exceeded
        """
        maxNoOfQuestions = prefs.getMaxQuestionsPerSitting()
        if question_id in sitting_questions:
            noOfQuestions = len(sitting_questions)
        else:
            noOfQuestions = len(sitting_questions) + 1
        if noOfQuestions >  maxNoOfQuestions:
            return "Maximum number of questions (%s) for this sitting exceeded" % noOfQuestions           
                                    
    def sittingToManyQuestionsByMP(self, question, questions ):
        """
        Maximum number of questions by a certain MP is exceeded
        """      
        maxNoOfQuestions = prefs.getMaxQuestionsByMpPerSitting()   
        noOfQuestions = 0
        memberOfParliament = u""
        session = Session()
        user_id = None
        for q in questions:
            if question.question_id != q.question_id:
                # do not count self
                if question.owner_id == q.owner_id:
                    noOfQuestions = noOfQuestions + 1
                    user_id =  q.owner_id
        if noOfQuestions > maxNoOfQuestions:
            session = Session()
            user = session.query(domain.User).get(user_id)
            username = u"%s %s" %( user.first_name, user.last_name )
            return "%s asked %s questions, a maximum of %s questions is allowed per MP and sitting" % (username, noOfQuestions, maxNoOfQuestions)
        
    def QuestionScheduledInPast(self, sitting):
        """
        the question was dropped on a date in the past
        """        
        if sitting.start_date.date() < datetime.date.today():
            return "A question cannot be scheduled in the past"

    def MotionScheduledInPast(self, sitting):
        """
        the question was dropped on a date in the past
        """        
        if sitting.start_date.date() < datetime.date.today():
            return "A motion cannot be scheduled in the past"            

    def BillScheduledInPast(self, sitting):
        """
        the question was dropped on a date in the past
        """        
        if sitting.start_date.date() < datetime.date.today():
            return "A bill cannot be scheduled in the past"   
            
    def postponeQuestion(self, question):
        if type(question) == ScheduledQuestionItems:
            return "Questions cannot be postponed in the calendar, use the workflow of the question instead"     
        if type(question) == ScheduledQuestionItems or (type(question) == domain.Question):
            if question.status == question_wf_state.postponed:                
                return
            elif question.status == question_wf_state.scheduled:
                return
            else:
                return "You cannot postpone this question"    
        elif type(question) == ScheduledMotionItems or (type(question) == domain.Motion):
            return "To postpone a motion drag it to the 'postponed motions' area"
        else:
            return "Unknown Item Type - you cannot drag this thing here"
            
    def admitQuestion(self, question):
        if type(question) == ScheduledQuestionItems:
            return "Questions cannot be postponed in the calendar, use the workflow of the question instead" 
        if type(question) == ScheduledQuestionItems or (type(question) == domain.Question):
            if question.status == question_wf_state.postponed:                
                return "This question is postponed, you can schedule it by dropping it on a sitting"
            elif question.status == question_wf_state.scheduled:
                return "To postpone a question drag it to the 'postponed questions' area"
            elif question.status == question_wf_state.admissible:    
                return
            else:
                return "You cannot make this question admissible"    
        elif type(question) == ScheduledMotionItems or (type(question) == domain.Motion):
            return "To postpone a motion drag it to the 'postponed motions' area"
        else:
            return "Unknown Item Type - you cannot drag this thing here"
            
    def admitMotion(self, motion):
        if type(motion) == ScheduledMotionItems:
            return "Motions cannot be postponed in the calendar, use the workflow of the motion instead" 
        if type(motion) == ScheduledMotionItems or (type(motion) == domain.Motion):
            if motion.status == motion_wf_state.postponed:                
                return "This motion is postponed, you can schedule it by dropping it on a sitting"
            elif motion.status == motion_wf_state.scheduled:
                return "To postpone a motion drag it to the 'postponed motions' area"
            elif motion.status == motion_wf_state.admissible:  
                return  
            else:
                return "You cannot make this motion admissible"    
        elif type(motion) == ScheduledQuestionItems or (type(motion) == domain.Question):
            return "To postpone a question drag it to the 'postponed questions' area"
        else:
            return "Unknown Item Type - you cannot drag this thing here"            
        
    def postponeMotion(self, motion):  
        if type(motion) == ScheduledMotionItems:
            return "Motions cannot be postponed in the calendar, use the workflow of the motion instead"  
        if type(motion) == ScheduledMotionItems or (type(motion) == domain.Motion):
            if motion.status == motion_wf_state.postponed:                
                return 
            elif motion.status == motion_wf_state.scheduled:
                return
            else:
                return "You cannot postpone this motion"    
        elif type(motion) == ScheduledQuestionItems or (type(motion) == domain.Question):
            return "To postpone a Motion drag it to the 'postponed motions' area"
        else:
            return "Unknown Item Type - you cannot drag this thing here"
            
    def postponeAgendaItem(self, agendaitem):
        if type(agendaitem) ==ScheduledAgendaItems:
            return "AgendaItems cannot be postponed in the calendar"
        elif type(agendaitem) == domain.AgendaItem:
            return
        else:
            return "Unknown Item Type - you cannot drag this thing here"                        
             
    def postponeBill(self, bill):  
        if type(bill) == ScheduledBillItems:
            return "Bills cannot be postponed in the calendar, use the workflow of the bill instead"  
        if type(bill) == domain.Bill:
            return
        else:   
            return "Unknown Item Type - you cannot drag this thing here"
            
    def getDuplicateSchedule(self, item_id, sitting_items):
        """
        This item is already schedule for this sitting
        """        
        if item_id in sitting_items:
            return "This item is already scheduled for this sitting"
        
    def __call__( self ):
        """
        the sitting, questions in that sitting and the question to be scheduled for that sitting
        are passed as form parameters
        """
        errors = []
        warnings = []        
        data = {'errors': errors, 'warnings': warnings}
        form_data = self.request.form
        sitting_questions = []
        sitting_motions = []
        sitting_bills = []
        sitting_agenda_items = []
        motion_id = None
        question_id = None
        sitting_id = None
        schedule_id = None
        schedule_sitting_id = None
        item = None         
        session = Session()
        #pdb.set_trace()
        if form_data:            
            if form_data.has_key( 'question_id'): 
                qid =  form_data['question_id']
                if qid[:2] == 'q_': 
                    question_id = long(qid[2:].split('_')[0])
                    item =  session.query(domain.Question).get(question_id)
                elif qid[:5] == 'isid_':
                    schedule_id = long(qid[5:].split('_')[0])
                    item = getScheduledItem(schedule_id)
                    schedule_sitting_id = item.sitting_id
                elif qid[:2] == 'm_':                                         
                    motion_id = long(qid[2:].split('_')[0])
                    item = session.query(domain.Motion).get(motion_id)
                elif qid[:2] == 'b_':                                         
                    bill_id = long(qid[2:].split('_')[0])
                    item = session.query(domain.Bill).get(bill_id)  
                elif qid[:2] == 'a_':                                         
                    item_id = long(qid[2:].split('_')[0])
                    item = session.query(domain.AgendaItem).get(item_id)                                         
            if form_data.has_key( 'sitting_id' ):
                if (form_data['sitting_id'][:4] == "sid_"):
                    sitting_id = long(form_data['sitting_id'][4:])
                elif form_data['sitting_id'] == 'postponed_questions':  
                    result = self.postponeQuestion(item)  
                    if result:
                        errors.append(result)
                    data = {'errors': errors, 'warnings': warnings}                                    
                    return simplejson.dumps( data )
                elif form_data['sitting_id'] == 'admissible_questions': 
                    result = self.admitQuestion(item)  
                    if result:
                        errors.append(result)
                    data = {'errors': errors, 'warnings': warnings}                                    
                    return simplejson.dumps( data )                   
                   
                elif form_data['sitting_id'] == 'admissible_motions':           
                    result = self.admitMotion(item)  
                    if result:
                        errors.append(result)
                    data = {'errors': errors, 'warnings': warnings}                                    
                    return simplejson.dumps( data )                         
                    
                elif form_data['sitting_id'] == 'postponed_motions':        
                    result = self.postponeMotion(item)  
                    if result:
                        errors.append(result)
                    data = {'errors': errors, 'warnings': warnings}                                    
                    return simplejson.dumps( data )      
                elif form_data['sitting_id'] == 'schedule_bills':        
                    result = self.postponeBill(item)  
                    if result:
                        errors.append(result)
                    data = {'errors': errors, 'warnings': warnings}                                    
                    return simplejson.dumps( data )   
                elif form_data['sitting_id'] == 'schedule_agenda_items':        
                    result = self.postponeAgendaItem(item)  
                    if result:
                        errors.append(result)
                    data = {'errors': errors, 'warnings': warnings}                                    
                    return simplejson.dumps( data )                                                                                                          
                else:
                    raise NotImplementedError    
            if form_data.has_key('q_id'):
                sq_ids = makeList(form_data['q_id'])
                for qid in sq_ids:
                    if qid[:2] == 'q_' :
                        sitting_questions.append(long(qid[2:].split('_')[0]))
                    elif qid[:2] == 'm_' :
                        sitting_motions.append(long(qid[2:].split('_')[0]))
                    elif  qid[:2] == 'b_' :  
                        sitting_bills.append(long(qid[2:].split('_')[0]))
                    elif qid[:5] == 'isid_':
                        isid = long(qid[5:].split('_')[0])
                        s_item = getScheduledItem(isid)                        
                        if type(s_item) == ScheduledQuestionItems:
                            sitting_questions.append(s_item.question_id)
                        elif type(s_item) == ScheduledMotionItems:
                            sitting_motions.append(s_item.motion_id)
                        elif type(s_item) == ScheduledBillItems:                            
                            sitting_bills.append(s_item.bill_id)
                    elif qid[:2] == 'a_' :
                        sitting_agenda_items.append(long(qid[2:].split('_')[0]))        
                    elif qid ==  u'original_proxy_id':
                        pass        
                    else:
                        raise NotImplementedError  
                        
        if schedule_sitting_id and sitting_id:
            if schedule_sitting_id != sitting_id:
                #pdb.set_trace()
                errors.append("You cannot move scheduled items around the calendar") # %s %s" %( str(schedule_id), str(sitting_id)) )
        questions = session.query(domain.Question).filter(schema.questions.c.question_id.in_(sitting_questions)).distinct().all()
        if sitting_id:
            sitting = session.query(domain.GroupSitting).get(sitting_id)
        else:
            sitting = None    
        if (type(item) == ScheduledQuestionItems) or (type(item) == domain.Question):
            question = item                
                
            #result = self.moveScheduledQuestion ( sitting, question )    
            result = self.sittingBeforeApproval( sitting, question )    
            if result:
                errors.append(result)
            result = self.sittingToEarly( sitting, question)
            if result:
                warnings.append(result)
            result = self.sittingToManyQuestions( question.question_id, sitting_questions)
            if result:
                warnings.append(result)
            result = self.sittingToManyQuestionsByMP( question, questions )    
            if result:
                warnings.append(result)
            result = self.QuestionScheduledInPast(sitting)
            if result:
                errors.append(result)    
            result = self.getDuplicateSchedule(question.question_id, sitting_questions)
            if result:
                errors.append(result)
            #data = {'errors':['to many quesitions','question scheduled to early'], 'warnings': ['more than 1 question by mp...',]}
            data = {'errors': errors, 'warnings': warnings}
            return simplejson.dumps( data )
        elif (type(item) == ScheduledMotionItems) or (type(item) == domain.Motion):
            result = self.MotionScheduledInPast(sitting)
            if result:
                errors.append(result)  
            result = self.getDuplicateSchedule(item.motion_id, sitting_motions)
            if result:
                errors.append(result)
    
            #data = {'errors':['to many motions','motion scheduled to early'], 'warnings': ['more than 1 motion by mp...',]}
            data = {'errors': errors, 'warnings': warnings}
            return simplejson.dumps( data )
        elif (type(item) == ScheduledBillItems) or (type(item) == domain.Bill):
            result = self.BillScheduledInPast(sitting)
            if result:
                errors.append(result)  
            result = self.getDuplicateSchedule(item.bill_id, sitting_bills)
            if result:
                errors.append(result)    
            #data = {'errors':['to many motions','motion scheduled to early'], 'warnings': ['more than 1 motion by mp...',]}
            data = {'errors': errors, 'warnings': warnings}
            return simplejson.dumps( data )   
        elif (type(item) == ScheduledAgendaItems) or (type(item) == domain.AgendaItem):
            #result = self.BillScheduledInPast(sitting)
            #if result:
            #    errors.append(result)  
            #result = self.getDuplicateSchedule(item.bill_id, sitting_bills)
            #if result:
            #    errors.append(result)    
            #data = {'errors':['to many motions','motion scheduled to early'], 'warnings': ['more than 1 motion by mp...',]}
            data = {'errors': errors, 'warnings': warnings}
            return simplejson.dumps( data )               
        else: 
            return   simplejson.dumps({'errors':['Unknown Item',], 'warnings': []})
    
def start_DateTime( Date ):
    """
    return the start datetime for the query
    i.e. first day to be displayed in the calendar 00:00
    """    
    cal = calendar.Calendar(prefs.getFirstDayOfWeek())
    mcal = cal.monthdatescalendar(Date.year,Date.month)
    firstday = mcal[0][0]
    return datetime.datetime(firstday.year, firstday.month, firstday.day, 0, 0, 0)
    
    
def end_DateTime( Date ):
    """
    return the end datetime for the query
    i.e. last day to be displayed in the calendar 23:59
    """
    cal = calendar.Calendar(prefs.getFirstDayOfWeek())
    mcal = cal.monthdatescalendar(Date.year,Date.month)
    lastday = mcal[-1][-1]
    return datetime.datetime(lastday.year, lastday.month, lastday.day, 23, 59, 59)
    
    


    
    
  
           
    
             
  
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


class ScheduleCalendarItemsViewletManager( WeightOrderedViewletManager ):
    """
    manage the viewlets that make up the items to be scheduled view
    """
    zope.interface.implements(IScheduleItems) 

class HolydayCalendar(BrowserView):
    __call__ = ViewPageTemplateFile("templates/schedule_holyday.pt")
    
    
class ScheduleHolydayCalendarViewletManager( WeightOrderedViewletManager ):
    """
    manage the viewlets that make up the calendar view
    """
    zope.interface.implements(IScheduleHolydayCalendar) 




class YUIDragDropViewlet( viewlet.ViewletBase ):
    """
    get the javascript for the YUI Drag and Drop
    """    
    approved_question_ids = []
    postponed_question_ids =[]
    approved_motion_ids = []
    postponed_motion_ids =[] 
    bill_ids = []   
    scheduled_item_ids = []
    sitting_ids =[]
    table_date_ids = []
    
    
    def update(self):
        """
        refresh the query
        """
        self.approved_question_ids = []
        self.postponed_question_ids =[]
        self.scheduled_item_ids = []
        self.approved_motion_ids = []
        self.postponed_motion_ids = []        
        self.sitting_ids = []
        self.bill_ids = []
        self.table_date_ids = []
        self.agenda_item_ids =[]
        self.Date = getDisplayDate(self.request)
        if not self.Date:
            self.Date=datetime.date.today()                
        session = Session()
        approved_questions = session.query(domain.Question).filter(schema.questions.c.status == question_wf_state.admissible).distinct()
        results = approved_questions.all()
        for result in results:
            self.approved_question_ids.append(result.question_id)
        agenda_items = session.query(domain.AgendaItem)
        results = agenda_items.all()
        for result in results:
            self.agenda_item_ids.append(result.agenda_item_id)                
        postponed_questions = session.query(domain.Question).filter(schema.questions.c.status == question_wf_state.postponed).distinct()
        results = postponed_questions.all()
        for result in results:
            self.postponed_question_ids.append(result.question_id)  
        approved_motions = session.query(domain.Motion).filter(schema.motions.c.status == motion_wf_state.admissible).distinct()
        results = approved_motions.all()
        for result in results:
            self.approved_motion_ids.append(result.motion_id) 
        postponed_motions = session.query(domain.Motion).filter(schema.motions.c.status == motion_wf_state.postponed).distinct()
        results = postponed_motions.all()              
        for result in results:
            self.postponed_motion_ids.append(result.motion_id) 
        bills = session.query(domain.Bill).filter(schema.bills.c.status.in_( [bill_wf_state.submitted , 
                                                                                bill_wf_state.first_reading_postponed ,
                                                                                bill_wf_state.second_pending , 
                                                                                bill_wf_state.second_reading_postponed , 
                                                                                bill_wf_state.whole_house_postponed ,
                                                                                bill_wf_state.house_pending ,
                                                                                bill_wf_state.report_reading_postponed ,                                                                                
                                                                                bill_wf_state.report_reading_pending , 
                                                                                bill_wf_state.third_pending,
                                                                                bill_wf_state.third_reading_postponed ]
                                                                                ))  
        results = bills.all()
        for result in results:
            self.bill_ids.append(result.bill_id)                                                                                            
        sittings, self.Date = current_sitting_query(self.Date)    
        results = sittings.all()     
        for result in results:
            self.sitting_ids.append(result.sitting_id)     
       
        scheduled_items =  session.query(domain.ItemSchedule).filter( rdb.and_(schema.items_schedule.c.sitting_id.in_(self.sitting_ids), 
                                                                    schema.items_schedule.c.active == True))
        
        
        
        results = scheduled_items.all()
        for result in results:
            self.scheduled_item_ids.append(result.schedule_id)    
        cal = calendar.Calendar(prefs.getFirstDayOfWeek())    
        for t_date in cal.itermonthdates(self.Date.year, self.Date.month):
            self.table_date_ids.append('"tdid-' + datetime.date.strftime(t_date,'%Y-%m-%d"'))                 
    
    def render(self):
        need('yui-dragdrop')
        need('yui-animation')    
        need('yui-logger')    #debug
        need('yui-json')
        JScript = """
<div id="user_actions">
 
</div>
<form name="make_schedule" method="POST" action="" enctype="multipart/form-data">
  <input type="button" id="saveButton" value="Save" />
  <input id="form.actions.cancel" class="context" type="submit" value="Cancel" name="cancel"/>
</form>
        
<script type="text/javascript">
<!--
(function() {

var Dom = YAHOO.util.Dom;
var Event = YAHOO.util.Event;
var DDM = YAHOO.util.DragDropMgr;


//////////////////////////////////////////////////////////////////////////////
// example app
//////////////////////////////////////////////////////////////////////////////
YAHOO.example.DDApp = {
    init: function() {


        %(DDTarget)s
        %(DDList)s     
        
        Event.on("saveButton", "click", this.showOrder);     
        YAHOO.widget.Logger.enableBrowserConsole();   
    },

    addLi: function(id) {
       new YAHOO.example.DDList(id); 
    },


    showOrder: function() {
        var parseList = function(ul) {
            if (ul != null) {
                var el_option;
                var items = ul.getElementsByTagName("li");
                var el_select = document.createElement('select');
                el_select.multiple = "multiple";  
                el_select.name = ul.id;                                 
                Dom.setStyle(el_select, "display", "none");
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
    this.originalEl = document.createElement('li');
    this.originalEl.id = "original_proxy_id";
    
    this.tddArray =new Array(%(tddArray)s);
    
};

YAHOO.extend(YAHOO.example.DDList, YAHOO.util.DDProxy, {
        
    get_random: function() {
                var ranNum= Math.floor(Math.random()*1000);
                return ranNum;
            },
    
        
        
    getSchuleAfterId: function (obj) {
                        
                     if ( obj.className ) {
                        // the classes are just a space separated list, so first get the list
                        var arrList = obj.className.split(' ');
                        this.logger.log(obj.className.substr(0,9) + " Class");
                        for ( var i = 0; i < arrList.length; i++ ) {
                                if (arrList[i].substr(0,9) == "sc-after-") {
                                        return "tdid-" + arrList[i].substr(9,19)
                                    }
                            }
                        }                                                    
                    },
    markScheduleDates: function (id) {
                        var tdEl;                                      
                        for ( var i = 0; i < this.tddArray.length; i++ ) {
                            tdEl = document.getElementById(this.tddArray[i]);
                            if (tdEl != null) {                               
                                if (tdEl.id < id) {
                                    Dom.addClass(tdEl.id, 'invalid-date')                                    
                                }
                                else {
                                    Dom.removeClass(tdEl.id, 'invalid-date')                                
                                }    
                                    
                            }
                        }        
                    },
                    

     
    getQuestionValidation: function(url, passData) {
          this.logger.log("data :" + passData);
          if (window.XMLHttpRequest) {              
            AJAX=new XMLHttpRequest();              
          } else {                                  
            AJAX=new ActiveXObject("Microsoft.XMLHTTP");
          }
          if (AJAX) {
            // false for synchronus request!
            //AJAX.open("POST", url, false);
            AJAX.open("GET", url + "?"+passData, false);
            AJAX.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            //AJAX.send(passData);
            AJAX.send(null);
            return AJAX.responseText;                                         
          } else {
             return false;
          }                                             
        },

    
    
    startDrag: function(x, y) {
        this.logger.log(this.id + " startDrag");
        // make the proxy look like the source element
        var dragEl = this.getDragEl();
        var clickEl = this.getEl();
        var parentEl = clickEl.parentNode;    
        var scheduleAfterId = this.getSchuleAfterId(clickEl);
        var currentDateId = %(currentDateId)s;
        if (scheduleAfterId < currentDateId) {
            scheduleAfterId = currentDateId;
            };
        this.markScheduleDates(scheduleAfterId);      
        // sometimes the proxy for the original element does
        // not get removed properly onDragDrop :(
        if (document.getElementById(this.originalEl.id) != null) {
            var opEl = document.getElementById(this.originalEl.id);
            var p_opEl = opEl.parentNode;
            p_opEl.removeChild(opEl)
            }
        parentEl.insertBefore(this.originalEl, clickEl.nextSibling);         
                         
        Dom.setStyle(clickEl, "visibility", "hidden");

        dragEl.innerHTML = clickEl.innerHTML;
    
        Dom.setStyle(dragEl, "color", Dom.getStyle(clickEl, "color"));
        Dom.setStyle(dragEl, "backgroundColor", Dom.getStyle(clickEl, "backgroundColor"));
        Dom.setStyle(dragEl, "border", "2px solid gray");      
        
    },





    onInvalidDrop: function(e) {
        var srcEl = this.getEl();
        var srcPEl = this.originalEl.parentNode;
        srcPEl.insertBefore(srcEl, this.originalEl);                
        srcPEl.removeChild(this.originalEl); 
        },

    endDrag: function(e) {
        var srcEl = this.getEl();
        var proxy = this.getDragEl();
        //var srcPEl = this.originalEl.parentNode;
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
        //srcPEl.removeChild(this.originalEl); 
        this.markScheduleDates("tdid-0000-00-00");
    },

    onDragDrop: function(e, id) {

        // If there is one drop interaction, the li was dropped either on the list,
        // or it was dropped on the current location of the source element.
        if (DDM.interactionInfo.drop.length === 1) {

            // The position of the cursor at the time of the drop (YAHOO.util.Point)
            var pt = DDM.interactionInfo.point; 

            // The region occupied by the source element at the time of the drop
            var region = DDM.interactionInfo.sourceRegion; 

            //
            var srcEl = this.getEl();
            var destEl = Dom.get(id);
            var destDD = DDM.getDDById(id); 
            var srcPEl = this.originalEl.parentNode;
            var valObject = { errors: [], warnings: []};
            var hasErrors = false;
            if ((destEl.nodeName.toLowerCase() == "ol") || (destEl.nodeName.toLowerCase() == "ul")) {                    
                    var queryStr="";
                    var items = destEl.getElementsByTagName("li");
                    var sitting = {
                        sitting_id : destEl.id,
                        question_id : srcEl.id,
                        }
                    queryStr="sitting_id=" + destEl.id + "&question_id=" + srcEl.id    
                    var sitting_questions=new Array();
                    for (i=0;i<items.length;i=i+1) {
                        sitting_questions[i] = items[i].id;
                        if (sitting_questions[i] != srcEl.id) {
                            queryStr = queryStr + "&q_id=" + items[i].id;
                            }
                        }
                    sitting.questions = sitting_questions;  
                    var jsonStr = YAHOO.lang.JSON.stringify(sitting);
                    //alert(jsonStr); 
                    var Validation=YAHOO.lang.JSON.parse(this.getQuestionValidation('./@@json_validate_question', queryStr));
                    if (Validation.errors.length >0) {
                        var errors = "" ;
                        for (i=0;i<Validation.errors.length;i=i+1) {
                            errors = errors + "\\n" + Validation.errors[i]
                            }
                        alert (errors);
                        hasErrors = true;
                        }
                                               
                    if (!(hasErrors)) {                    
                        if (Validation.warnings.length >0) {
                            var errors = "" ;
                            for (i=0;i<Validation.warnings.length;i=i+1) {
                                errors = errors + "\\n" + Validation.warnings[i]
                                }
                            errors = errors + "\\n" + "schedule anyway?"    
                            hasErrors = !(confirm (errors));
                            }                      
                        }                        
                    Dom.removeClass(id, 'dragover');    
                    Dom.removeClass(id, 'invalid-dragover');                    
                }
                else {
                    alert( srcEl.id + " -> " + destEl.id);
                    }
            if (destEl.nodeName.toLowerCase() == "li") {
                var pEl = destEl.parentNode;
                alert( srcEl.id + " -> " + destEl.id);
                if (pEl.nodeName.toLowerCase() == "ol") {                   
                    Dom.removeClass(pEl.id, 'dragover');
                    Dom.removeClass(pEl.id, 'invalid-dragover');
                    }
                }
            if (hasErrors) {
                //alert ("invalid target");
                //this.onInvalidDrop(e)
                //this.invalidDropEvent.fire()
                this.logger.log("proxy parent: " + srcPEl.id);
                srcPEl.insertBefore(srcEl, this.originalEl);                
            }           
            else {
                // get the srcElement and clone it if the 
                // element can be scheduled multiple times
                if ((srcEl.id.substr(0,2) == "m_") ||
                    (srcEl.id.substr(0,2) == "b_")) {
                    if (srcPEl != destEl) {
                        // the element was NOT moved around (reordered) in the same list
                        if ((destEl.id.substr(0,4) == "sid_") && (srcPEl.id.substr(0,4) != "sid_")) {
                            // the destination is a sitting and the source is NOT a sitting
                            var schedEl = srcEl.cloneNode(true);
                            schedEl.id = srcEl.id + "_" + this.get_random();
                            srcPEl.insertBefore(schedEl, this.originalEl);  
                            //DDM.swapNode( srcEl, schedEl);    
                            //alert (schedEl.id);             
                            YAHOO.example.DDApp.addLi(schedEl.id);
                            Dom.setStyle(schedEl, "visibility", "");
                        }    
                    }
                }
                
                // Check to see if we are over the source element's location.  We will
                // append to the bottom of the list once we are sure it was a drop in
                // the negative space (the area of the list without any list items)
                if (!region.intersect(pt)) {               
                    destEl.appendChild(srcEl);
                    destDD.isEmpty = false;                
                } 
                var lnk = srcEl.getElementsByTagName("a");
                if (! lnk.length) {              
                    srcEl.innerHTML = (srcEl.innerHTML.substr(0,15) + '...');               
                    }
            }      
          srcPEl.removeChild(this.originalEl);        
        }        
        DDM.refreshCache(); 
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

/////////////////////////////////////////////////
/////////


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

////////////
///////////////////////////////////////////////

    onDragOver: function(e, id) {
        
        var srcEl = this.getEl();
        var destEl = Dom.get(id);
        
        // We are only concerned with list items, we ignore the dragover
        // notifications for the list.
        if (destEl.nodeName.toLowerCase() == "li") {
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

-->        
</script>         
        """
        DDList = ""
        for qid in self.approved_question_ids:            
            #new YAHOO.example.DDList("li" + i + "_" + j);
            DDList = DDList + 'new YAHOO.example.DDList("q_' + str(qid) +'"); \n'
        for qid in self.postponed_question_ids:
            DDList = DDList + 'new YAHOO.example.DDList("q_' + str(qid) +'"); \n'
        for mid in self.approved_motion_ids:            
            DDList = DDList + 'new YAHOO.example.DDList("m_' + str(mid) +'"); \n'
        for mid in self.postponed_motion_ids:
            DDList = DDList + 'new YAHOO.example.DDList("m_' + str(mid) +'"); \n'            
        for qid in self.scheduled_item_ids:
            DDList = DDList + 'new YAHOO.example.DDList("isid_' + str(qid) +'"); \n'
        for qid in self.bill_ids:
            DDList = DDList + 'new YAHOO.example.DDList("b_' + str(qid) +'"); \n'        
        for qid in self.agenda_item_ids:
            DDList = DDList + 'new YAHOO.example.DDList("a_' + str(qid) +'"); \n'                   
        DDTarget = ""    
        for sid in self.sitting_ids:
            #new YAHOO.util.DDTarget("ul"+i);
            DDTarget = DDTarget + 'new YAHOO.util.DDTarget("sid_'  + str(sid) +'"); \n'
        #add the hardcoded targets for postponed and admissable list
        DDTarget = DDTarget + 'new YAHOO.util.DDTarget("admissible_questions"); \n'
        DDTarget = DDTarget + 'new YAHOO.util.DDTarget("postponed_questions"); \n'
        DDTarget = DDTarget + 'new YAHOO.util.DDTarget("admissible_motions"); \n'
        DDTarget = DDTarget + 'new YAHOO.util.DDTarget("postponed_motions"); \n'
        DDTarget = DDTarget + 'new YAHOO.util.DDTarget("schedule_bills"); \n'
        DDTarget = DDTarget + 'new YAHOO.util.DDTarget("schedule_agenda_items"); \n'
        t_list = ""
        for sid in self.sitting_ids:
            # var ul1=Dom.get("ul1"), ul2=Dom.get("ul2"); 
            t_list = t_list + ' sid_'+ str(sid) +'=Dom.get("sid_' + str(sid) + '"),'
        t_list = t_list + 'admissible_questions=Dom.get("admissible_questions"),'
        t_list = t_list + 'postponed_questions=Dom.get("postponed_questions"),'
        t_list = t_list + 'admissible_motions=Dom.get("admissible_motions"),'
        t_list = t_list + 'postponed_motions=Dom.get("postponed_motions")'
        parseList =""
        for sid in self.sitting_ids:
            #parseList(ul1, "List 1") +
            parseList = parseList + 'parseList(sid_'+ str(sid) + '); \n'
        parseList = parseList +  'parseList(admissible_questions); \n'   
        parseList = parseList +  'parseList(postponed_questions); \n'
        parseList = parseList +  'parseList(admissible_motions); \n'   
        parseList = parseList +  'parseList(postponed_motions); \n'        
        maxQuestionsPerSitting = prefs.getMaxQuestionsPerSitting()
        tddArray = ", ".join(self.table_date_ids)
        currentDateId = '"tdid-' + datetime.date.strftime(datetime.date.today(),'%Y-%m-%d"')
        js_inserts= {
            'DDList':DDList,
            'DDTarget':DDTarget,
            'targetList': t_list,
            'parseList': parseList,
            'maxQuestionsPerSitting': maxQuestionsPerSitting,
            'tddArray' : tddArray,
            'currentDateId': currentDateId }
        return JScript % js_inserts           
        
        
class QuestionInStateViewlet( viewlet.ViewletBase ):
    name = state = None
    render = ViewPageTemplateFile ('templates/schedule_question_viewlet.pt')    
    list_id = "_questions"    
    def getData(self):
        """
        return the data of the query
        """    
        offset = datetime.timedelta(prefs.getNoOfDaysBeforeQuestionSchedule())  
        data_list = []       
        results = self.query.all()
        
        for result in results:            
            data ={}
            data['qid']= ( 'q_' + str(result.question_id) )                         
            data['subject'] = u'Q ' + str(result.question_number) + u' ' + result.subject
            data['title'] = result.subject
            data['schedule_date_class'] = 'sc-after-' + datetime.date.strftime(result.approval_date + offset, '%Y-%m-%d')
            data_list.append(data)            
        return data_list
    
    
    def update(self):
        """
        refresh the query
        """
        session = Session()
        qfilter = rdb.and_(schema.questions.c.response_type == u"O", 
                            schema.questions.c.status == self.state)
        
        questions = session.query(domain.Question).filter(qfilter)
        self.query = questions        
        
class PostponedQuestionViewlet( QuestionInStateViewlet ):
    """
    display the postponed questions
    """    
    name = state = question_wf_state.postponed   
    list_id = "postponed_questions"    
    
    
class AdmissibleQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = state = question_wf_state.admissible
    render = ViewPageTemplateFile ('templates/schedule_question_viewlet.pt')    
    list_id = "admissible_questions"
 
class MotionInStateViewlet( viewlet.ViewletBase ):  
    name = state = None
    render = ViewPageTemplateFile ('templates/schedule_question_viewlet.pt')    
    list_id = "_motions"    
    def getData(self):
        """
        return the data of the query
        """      
        data_list = []
        results = self.query.all()
       
        for result in results:            
            data ={}
            data['qid']= ( 'm_' + str(result.motion_id) )                         
            data['subject'] = u'M ' + str(result.motion_number) + u' ' +  result.title
            data['title'] = result.title
            data['schedule_date_class'] = 'sc-after-'  + datetime.date.strftime(result.approval_date, '%Y-%m-%d')
            data_list.append(data)            
        return data_list
    
    
    def update(self):
        """
        refresh the query
        """
        session = Session()
        motions = session.query(domain.Motion).filter(schema.motions.c.status == self.state)
        self.query = motions        
    
class AdmissibleMotionViewlet( MotionInStateViewlet ):   
    """
    display the admissible Motions
    """
    name = state = motion_wf_state.admissible
    list_id = "admissible_motions"
    

class PostponedMotionViewlet( MotionInStateViewlet ):   
    """
    display the admissible Motions
    """
    name = state = motion_wf_state.postponed
    list_id = "postponed_motions"

class BillItemsViewlet( viewlet.ViewletBase ): 
    """
    Display all bills that can be scheduled for a parliamentary sitting
    """  
    name  = u"Bills"
    render = ViewPageTemplateFile ('templates/schedule_question_viewlet.pt')    
    list_id = "schedule_bills"    
    def getData(self):
        """
        return the data of the query
        """      
        data_list = []
        results = self.query.all()
      
        for result in results:            
            data ={}
            data['qid']= ( 'b_' + str(result.bill_id) )                         
            data['subject'] = u'B ' + result.title
            data['title'] = result.title
            data['schedule_date_class'] = 'sc-after-'  + datetime.date.strftime(result.publication_date, '%Y-%m-%d')
            data_list.append(data)            
        return data_list
    
    
    def update(self):
        """
        refresh the query
        """
        session = Session()
        bills = session.query(domain.Bill).filter(schema.bills.c.status.in_( [bill_wf_state.submitted , 
                                                                                bill_wf_state.first_reading_postponed ,
                                                                                bill_wf_state.second_pending , 
                                                                                bill_wf_state.second_reading_postponed , 
                                                                                bill_wf_state.whole_house_postponed ,
                                                                                bill_wf_state.house_pending ,
                                                                                bill_wf_state.report_reading_postponed ,                                                                                
                                                                                bill_wf_state.report_reading_pending , 
                                                                                bill_wf_state.third_pending,
                                                                                bill_wf_state.third_reading_postponed ]
                                                                                ))
        self.query = bills            


class AgendaItemsViewlet( viewlet.ViewletBase ): 
    """
    Agenda Items that can be scheduled
    """    
    name  = u"Agenda Items"
    render = ViewPageTemplateFile ('templates/schedule_question_viewlet.pt')    
    list_id = "schedule_agenda_items"       

    def getData(self):
        """
        return the data of the query
        """      
        data_list = []
        results = self.query.all()
             
        for result in results:            
            data ={}
            data['qid']= ( 'a_' + str(result.agenda_item_id) )                         
            data['subject'] = u'' + result.title
            data['title'] = result.title
            data['schedule_date_class'] = 'sc-after-'  + datetime.date.strftime(datetime.date.today(), '%Y-%m-%d')
            data_list.append(data)            
        return data_list    
    
    
    def update(self):
        """
        refresh the query
        """
        session = Session()
        agendaitems = session.query(domain.AgendaItem).select_from(
                                sql.outerjoin(
                                    schema.agenda_items, schema.items_schedule, 
                                    schema.agenda_items.c.agenda_item_id == schema.items_schedule.c.item_id)).filter(
                                                    schema.items_schedule.c.schedule_id == None)       
        self.query = agendaitems    


class PlenaryCalendar(BrowserView):
    __call__ = ViewPageTemplateFile("templates/plenary.pt")


class PlenaryCalendarViewletManager( WeightOrderedViewletManager ):
    """
    manage the viewlets that make up the calendar view
    """
    zope.interface.implements(IPlenaryCalendar) 



class PlenarySittingCalendarViewlet( viewlet.ViewletBase ):
    """
    display a calendar with all sittings in a month
    """
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
        
    def next(self):
        """
        return link to the next month if the end date
        of the session is after the 1st of the next month
        """        
        if self.Date.month == 12:
            month = 1
            year = self.Date.year + 1
        else:
            month = self.Date.month + 1
            year = self.Date.year        
        try:
            nextdate = datetime.date(year,month,self.Date.day)
        except:
            # if we try to move from 31 of jan to 31 of feb or so
            nextdate = datetime.date(year,month,15)            
        return ('<a href="?date=' 
                + datetime.date.strftime(nextdate,'%Y-%m-%d' )
                + '"> &gt;&gt; </a>' )


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
            data['day'] = result.start_date.date()
            data['url']= ( path + 'obj-' + str(result.sitting_id) )   
            data['did'] = ('dlid_' +  datetime.datetime.strftime(result.start_date,'%Y-%m-%d') +
                           '_stid_' + str( result.sitting_type))                                                
            data_list.append(data)            
        return data_list

    def getTdId(self, Date):
        """
        return an Id for that td element:
        consiting of tdid- + date
        like tdid-2008-01-17
        """
        return 'tdid-' + datetime.date.strftime(Date,'%Y-%m-%d') 

    def getDayClass(self, Date):
        """
        return the class settings for that calendar day
        """
        css_class = ""
        if self.Date.month != Date.month:
            css_class = css_class + "other-month "           
        if Date < datetime.date.today():
            css_class = css_class + "past-date "    
        if Date == datetime.date.today():
            css_class = css_class + "current-date "  
        if Date.weekday() in prefs.getWeekendDays():
            css_class = css_class + "weekend-date "             
        session = Session()    
        query = session.query(domain.HolyDay).filter(schema.holydays.c.holyday_date == Date)
        results = query.all()
        if results:        
            css_class = css_class + "holyday-date "          
        return css_class.strip()
            
    def getWeekNo(self, Date):
        """
        return the weeknumber for a given date
        """
        return Date.isocalendar()[1]


    def getSittings4Day(self, Date):
        """
        return the sittings for that day
        """
        day_data=[]      
        for data in self.Data:
            if data['day'] == Date:
                day_data.append(data)
        return day_data                
        

    def update(self):
        """
        refresh the query
        """                
        self.Date = getDisplayDate(self.request)
        if not self.Date:
            self.Date=datetime.date.today()                            
        self.query, self.Date = current_sitting_query(self.Date)        
        self.request.response.setCookie('display_date', datetime.date.strftime(self.Date,'%Y-%m-%d') )
        self.monthcalendar = calendar.Calendar(prefs.getFirstDayOfWeek()).monthdatescalendar(self.Date.year,self.Date.month)         
        self.monthname = datetime.date.strftime(self.Date,'%B %Y')
        self.Data = self.getData()
    
    render = ViewPageTemplateFile ('templates/plenary_calendar_viewlet.pt')

    
    
class ScheduleCalendarViewlet( PlenarySittingCalendarViewlet ):
    """
    display a calendar with all sittings in a month to schedule items
    """
    
    errors = []
    
    

        


    def getActiveSittingItems(self, sitting_id):
        """
        return all questions assigned to that sitting
        """
        session = Session()
        active_sitting_items_filter = rdb.and_(schema.items_schedule.c.sitting_id == sitting_id, 
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

    def getInactiveSittingItems(self, sitting_id):
        """
        return all questions assigned to that sitting
        """
        session = Session()
        active_sitting_items_filter = rdb.and_(schema.items_schedule.c.sitting_id == sitting_id, 
                                                schema.items_schedule.c.active == False)
        items = session.query(ScheduledItems).filter(active_sitting_items_filter).order_by(schema.items_schedule.c.order)
        data_list=[] 
        results = items.all()
        for result in results:            
            data ={}
            data['schedule_id'] = ( 'isid_' + str(result.schedule_id) ) # isid for ItemSchedule ID 
            if type(result) == ScheduledQuestionItems:                       
                data['subject'] = u'Q ' + str(result.question_number) + u' ' +  result.subject[:10]
                data['title'] = result.subject
                data['type'] = "question"
                data['url'] = '/questions/obj-' + str(result.question_id)                
            elif type(result) == ScheduledMotionItems:    
                data['subject'] = u'M ' + str(result.motion_number) + u' ' +result.title[:10]
                data['title'] = result.title 
                data['type'] = "motion"
                data['url'] = '/motions/obj-' + str(result.motion_id)
            elif type(result) == ScheduledBillItems:    
                data['subject'] = u"B " + result.title[:10]             
                data['title'] = result.title 
                data['type'] = "bill"
                data['url'] = '/bills/obj-' + str(result.bill_id)
            data['status'] = result.status
            data_list.append(data)            
        return data_list


       
       
    def schedule_question(self, question_id, sitting_id, sort_id):        
        session = Session()
        item_schedule = domain.ItemSchedule()
        question = session.query(domain.Question).get(question_id)
        if question:
            # set the question's parent to the application for security checks
            question.__parent__= self.context
            if sitting_id:
                sitting = session.query(domain.GroupSitting).get(sitting_id)
            else:
                sitting = None                
            if sitting:             
                # our question is either admissible, deferred or postponed 
                session.begin()
                try:                     
                    item_schedule.sitting_id = sitting_id
                    item_schedule.item_id = question_id
                    item_schedule.order = sort_id
                    session.save(item_schedule)
                    IWorkflowInfo(question).fireTransitionToward(question_wf_state.scheduled, check_security=True)
                    session.commit()
                except:
                    session.rollback()
                    #rollback leave a inactive session behind, so it has to be closed manually
                    session.close()
                    self.errors.append("Question could not be scheduled")  
                    
                #if IWorkflowInfo(question).state().getState() == question_wf_state.admissible:
                #    IWorkflowInfo(question).fireTransition('schedule', check_security=True)
                #elif IWorkflowInfo(question).state().getState() == question_wf_state.deferred:
                #    IWorkflowInfo(question).fireTransition('schedule-deferred', check_security=True)
                #elif IWorkflowInfo(question).state().getState() == question_wf_state.postponed:
                #    IWorkflowInfo(question).fireTransition('schedule-postponed', check_security=True)
                #else:
                #    print "invalid workflow state:", IWorkflowInfo(question).state().getState()
                        
#                elif question.sitting_id != sitting_id:  
#                    # a question with a sitting id is scheduled
#                    assert IWorkflowInfo(question).state().getState() == question_wf_state.scheduled                  
#                    IWorkflowInfo(question).fireTransition('postpone', check_security=True)
#                    #assert question.sitting_id is None
#                    #question.sitting_id = sitting_id
#                    IWorkflowInfo(question).fireTransition('schedule-postponed', check_security=True)
#                else:
#                    #sitting stays the same - nothing to do
#                    #print question.sitting_id == sitting_id
#                    pass
            else:              
                if IWorkflowInfo(question).state().getState() == question_wf_state.scheduled:
                    IWorkflowInfo(question).fireTransition('postpone', check_security=True)
                else:
                    raise NotImplementedError     
                    
    def schedule_bill(self, bill_id, sitting_id, sort_id):
        session = Session()
        item_schedule = domain.ItemSchedule()
        bill = session.query(domain.Bill).get(bill_id)
        if bill:
            bill.__parent__ = self.context
            if sitting_id:
                sitting = session.query(domain.GroupSitting).get(sitting_id)
            else:
                sitting = None                
            if sitting:   
                if bill.status in [bill_wf_state.submitted , 
                    bill_wf_state.first_reading_postponed ,
                    bill_wf_state.second_pending , 
                    bill_wf_state.second_reading_postponed , 
                    bill_wf_state.whole_house_postponed ,
                    bill_wf_state.house_pending ,
                    bill_wf_state.report_reading_postponed ,                                                                                
                    bill_wf_state.report_reading_pending , 
                    bill_wf_state.third_pending,
                    bill_wf_state.third_reading_postponed ]:
                    item_schedule.sitting_id = sitting_id
                    item_schedule.item_id = bill_id
                    item_schedule.order = sort_id
                    session.save(item_schedule) 
                    if bill.status in [bill_wf_state.submitted , bill_wf_state.first_reading_postponed]:
                        IWorkflowInfo(bill).fireTransitionToward(bill_wf_state.first_reading, check_security=True)
                    elif bill.status in [bill_wf_state.second_pending, bill_wf_state.second_reading_postponed ]:
                        IWorkflowInfo(bill).fireTransitionToward(bill_wf_state.second_reading, check_security=True)
                    elif bill.status in [bill_wf_state.report_reading_postponed ,bill_wf_state.report_reading_pending]:
                        IWorkflowInfo(bill).fireTransitionToward(bill_wf_state.report_reading, check_security=True)
                    elif bill.status in [bill_wf_state.third_pending, bill_wf_state.third_reading_postponed ]:
                        IWorkflowInfo(bill).fireTransitionToward(bill_wf_state.third_reading, check_security=True)
                    elif bill.status in [  bill_wf_state.house_pending, bill_wf_state.whole_house_postponed ]:
                        IWorkflowInfo(bill).fireTransitionToward(bill_wf_state.whole_house, check_security=True)                    
                elif bill.status in [bill_wf_state.first_reading ,
                    bill_wf_state.second_reading , 
                    bill_wf_state.whole_house ,
                    bill_wf_state.report_reading ,                                                                                
                    bill_wf_state.third_reading]:
                    # schedule on multiple days
                    item_schedule.sitting_id = sitting_id
                    item_schedule.item_id = bill_id
                    item_schedule.order = sort_id
                    session.save(item_schedule)  
                else:
                    raise NotImplementedError    
                            
        else:
            raise NotImplementedError 
    
    def schedule_motion(self, motion_id, sitting_id, sort_id):      
        session = Session()
        item_schedule = domain.ItemSchedule()
        motion = session.query(domain.Motion).get(motion_id)
        if motion:
            # set the motion's parent to the application for security checks
            motion.__parent__= self.context    
            if sitting_id:
                sitting = session.query(domain.GroupSitting).get(sitting_id)
            else:
                sitting = None                
            if sitting:    
                # our motion is either admissible, deferred or postponed  
                session.begin()
                try:                    
                    item_schedule.sitting_id = sitting_id
                    item_schedule.item_id = motion_id
                    item_schedule.order = sort_id
                    session.save(item_schedule)  
                    if IWorkflowInfo(motion).state().getState() != motion_wf_state.scheduled:              
                        # scheduling is possible for multipe sittings                    
                        IWorkflowInfo(motion).fireTransitionToward(motion_wf_state.scheduled, check_security=True)   
                    session.commit()
                except:
                    self.errors.append("Motion could not be scheduled")    
                    session.rollback()
                    session.close()
            else:
                if IWorkflowInfo(motion).state().getState() == motion_wf_state.scheduled:
                      IWorkflowInfo(motion).fireTransition('postpone', check_security=True)
                else:
                    raise NotImplementedError     
    
    def schedule_agenda_item(self, agenda_item_id, sitting_id, sort_id):
        session =Session()
        item_schedule = domain.ItemSchedule()
        agenda_item = session.query(domain.AgendaItem).get(agenda_item_id)
        if agenda_item:
            #agenda_item.__parent__ = self.context   
            if sitting_id:
                sitting = session.query(domain.GroupSitting).get(sitting_id)
            else:
                sitting = None
            if sitting:
                session.begin()
                try:
                    item_schedule.sitting_id = sitting_id
                    item_schedule.item_id = agenda_item_id
                    item_schedule.order = sort_id
                    session.save(item_schedule) 
                    session.commit()
                except:
                    self.errors.append("Agenda Item could not be scheduled") 
                    session.rollback()    
                    session.close()
            else:
                pass
        else:
            self.errors.append("Agenda Item could not be scheduled")             
        
    
    def getScheduledItems( self, form ):
        """
        return all items currently scheduled on the calendar
        """
        sitting_ids = []
        for target in form.keys():
            if target[4:] == 'sid_':
                #this is a sitting
                sitting_ids.append(long(target[4:]))
        if len(sitting_ids) > 0:
            # there are sittings on the calendar
            session = Session()
            scheduled_items =  session.query(ScheduledItems).filter(schema.items_schedule.c.sitting_id.in_(sitting_ids))
            return scheduled_items
        else:
            return None
    
    
    def insert_item_into_sitting( self, sitting_id, itemIds=[]):
        """
        an item was dropped on a sitting, or 
        is already scheduled for this sitting
        """      
        session = Session()
        sort_id = 0
        for item_id in itemIds:
            sort_id = sort_id + 1
            if item_id[:2] == 'q_':
                #a question, to be scheduled
                question_id = long(item_id[2:]) 
                self.schedule_question(question_id, sitting_id, sort_id)                 
            elif item_id[:2] == 'm_':
                #a motion, to be scheduled
                motion_id = long(item_id[2:].split('_')[0])
                self.schedule_motion(motion_id, sitting_id, sort_id)
            elif item_id[:2] == 'b_':
                #a bill, to be scheduled
                bill_id = long(item_id[2:].split('_')[0])
                self.schedule_bill(bill_id, sitting_id, sort_id)  
            elif item_id[:2] == 'a_':
                #agenda item
                agenda_item_id = long(item_id[2:].split('_')[0])
                self.schedule_agenda_item(agenda_item_id, sitting_id, sort_id)                  
            elif item_id[:5] == 'isid_':
                # a scheduled item to be rescheduled                    
                scheduled_item_id = long(item_id[5:])
                item = session.query(ScheduledItems).filter(schema.items_schedule.c.schedule_id == scheduled_item_id).one()
                if item.sitting_id == sitting_id:
                    #same sitting no workflow actions just update the sort_id
                    item.order = sort_id
                else:
                    #item was moved from one sitting to another                     
                    raise NotImplementedError( "A scheduled item cannot be rescheduled" )
                    if type(item) == ScheduledQuestionItems:
                        question_id = item.question_id
                        self.schedule_question(question_id, None, 0)
                        self.schedule_question(question_id, sitting_id, sort_id)
                    elif type(item) == ScheduledBillItems:
                        bill_id = item.question_id
                        self.schedule_question(bill_id, None, 0)
                        self.schedule_bill(bill_id, sitting_id, sort_id)
                    elif type(item) == ScheduledMotionItems:
                        motion_id = item.motion_id
                        self.schedule_motion(motion_id, None, 0)
                        self.schedule_motion(motion_id, sitting_id, sort_id)
                    else:
                        raise NotImplementedError      
                          
    def remove_item_from_sitting( self, itemIds=[]):
        """
        an item was dropped into the admissible or postponed questions
        list
        """          
        session = Session()
        for item_id in itemIds:
            if item_id[:5] == 'isid_':
                raise NotImplementedError
                scheduled_item_id = long(item_id[5:])
                item = session.query(ScheduledItems).filter(schema.items_schedule.c.schedule_id == scheduled_item_id).one()
                if type(item) == ScheduledQuestionItems:
                    question_id = item.question_id
                    self.schedule_question(question_id, None, 0)
                elif type(item) == ScheduledBillItems:
                    pass
                elif type(item) == ScheduledMotionItems:
                     motion_id = item.motion_id   
                     self.schedule_motion(motion_id, None, 0)    
                else:
                    raise NotImplementedError                                           
            elif item_id[:2] == 'q_':
                # nothing to do here, either not moved
                # or dropped from admissible to postponed or vice versa
                pass
            elif item_id[:2] == 'b_':
                pass
            elif item_id[:2] == 'm_':
                pass
                 
    def insert_items( self, form ):
        """
        insert items into the calendar
        """
        for target in form.keys():
            # the target is the list in which the item is in
            if target[:4] == 'sid_':
                # the target is a sitting
                itemIds = makeList(form[target])
                sitting_id = long(target[4:])                
                self.insert_item_into_sitting(sitting_id, itemIds)                                                                                     
                   
            elif (target == 'admissible_questions') or (target == 'postponed_questions'):      
                itemIds = makeList(form[target])               
                self.remove_item_from_sitting( itemIds)
                        
                                   
            elif (target == 'admissible_motions') or (target == 'postponed_motions'):
                itemIds = makeList(form[target])
                self.remove_item_from_sitting( itemIds)
                                                              
                    
    def insert_questions(self, form):
        for sitting in form.keys():
            if sitting[:4] == 'sid_':
                qids = makeList(form[sitting])
                sitting_id = long(sitting[4:])     
                sort_id = 0                      
                for qid in qids:                        
                    if qid[:2] == 'q_':
                        sort_id = sort_id + 1
                        question_id = long(qid[2:])
                        self.schedule_question(question_id, sitting_id, sort_id)
                    elif (qid[:5] == 'isid_'):
                        #this is a scheduled item
                        sort_id = sort_id + 1
                        schedule_id = long(qid[5:])
                        question = getScheduledItem(schedule_id)
                        self.schedule_question(question.question_id, sitting_id, sort_id)
 
                                          
            elif (sitting == 'admissible_questions') or (sitting == 'postponed_questions'):                
                qids = makeList(form[sitting])           
                for qid in qids:                            
                    if qid[:2] == 'q_':                            
                        question_id = long(qid[2:])
                        self.schedule_question(question_id, None, 0)
                    elif (qid[:5] == 'isid_'):        
                        schedule_id = long(qid[5:])
                        question = getScheduledItem(schedule_id)
                        self.schedule_question(question.question_id, None, 0)                    
                        
#            elif :
#                qids = form['postponed_questions']
#                if type(qids) == ListType:
#                    for qid in qids:                            
#                        if qid[:2] == 'q_':
#                            sort_id = sort_id + 1
#                            question_id = long(qid[2:])
#                            self.schedule_question(question_id, None, 0)
#                if type(qids) in StringTypes:
#                    if qids[:2] == 'q_':
#                        question_id = long(qids[2:])
#                        self.schedule_question(question_id, None, 0)                        
       
    def update(self):
        """
        refresh the query
        """
        self.errors = []        
        if self.request.form:
            if not self.request.form.has_key('cancel'):
                self.insert_items(self.request.form) 
                
        self.Date = getDisplayDate(self.request)
        if not self.Date:
            self.Date=datetime.date.today()                            
        self.query, self.Date = current_sitting_query(self.Date)        
        self.request.response.setCookie('display_date', datetime.date.strftime(self.Date,'%Y-%m-%d') )
        self.monthcalendar = calendar.Calendar(prefs.getFirstDayOfWeek()).monthdatescalendar(self.Date.year,self.Date.month)         
        self.monthname = datetime.date.strftime(self.Date,'%B %Y')
        self.Data = self.getData()
    
    render = ViewPageTemplateFile ('templates/schedule_calendar_viewlet.pt')
    
class SittingCalendarWeekViewlet(ScheduleCalendarViewlet):
    """
    display only the current week
    """
    render = ViewPageTemplateFile('templates/sitting_week_calendar_viewlet.pt')

    def getWeek(self):
        for week in self.monthcalendar:
            if self.Date in week:
                return week
                

class SittingCalendarAtomWeek(BrowserView):
    """
    just another template for display
    """    
    __call__ = ViewPageTemplateFile("templates/atom-calendar-view.pt")
    def name(self):
        return "Calendar"
        if self.context.__parent__:
            descriptor = queryModelDescriptor( self.context.__parent__.domain_model )
        if descriptor:
            name = getattr( descriptor, 'display_name', None)
        if not name:
            name = getattr( self.context.__parent__.domain_model, '__name__', None)  
        return name 
           
    def feedtitle(self):            
        if self.form_name:
            title = self.form_name
        else:
            title = self.name()
        return title
            
    def feedUid(self):
        return  absoluteURL( self.context, self.request ) + 'atom.xml'
               
    def uid(self):     
        #XXX       
        return "urn:uuid:" + base64.urlsafe_b64encode(self.context.__class__.__name__ + ':' + stringKey(removeSecurityProxy(self.context)))
        
    def url(self):    
        return absoluteURL( self.context, self.request )       
        
    def updated(self):
        return datetime.datetime.now().isoformat()              
    
    
class ScheduleHolyDaysViewlet( viewlet.ViewletBase ):
    """
    a calendar to allow you to schedule the holydays of a year
    """   
    Date=datetime.date.today()
    
    def insert_items( self, form ):
        """
        insert the holydays from the form into
        """
        year = self.Date.year
        year_start = datetime.date(year, 1, 1)
        year_end = datetime.date(year, 12, 31)
        session = Session()
        connection = session.connection(domain.HolyDay)
        del_dates = schema.holydays.delete(schema.holydays.c.holyday_date.between(year_start, year_end))
        connection.execute(del_dates)
        if form.has_key("hdd"):
            datestrings = makeList(form["hdd"])
            for datstr in datestrings:
                holyday = domain.HolyDay()
                dt = time.strptime(datstr,'%Y-%m-%d')
                y = dt[0]
                m = dt[1]
                d = dt[2]
                holyday.holyday_date = datetime.date(y,m,d)
                session.save(holyday)
         
    def getmonthname(self, Date):
        """
        return the name of the month + year
        """
        return  datetime.date.strftime(Date,'%B %Y')
    
    def getWeekNo(self, Date):
        """
        return the weeknumber for a given date
        """
        return Date.isocalendar()[1]
    
    def getTdId(self, Date):
        """
        return an Id for that td element:
        consiting of tdid- + date
        like tdid-2008-01-17
        """
        return 'tdid-' + datetime.date.strftime(Date,'%Y-%m-%d')     
    
    def getDateValue(self, Date):
        return datetime.date.strftime(Date,'%Y-%m-%d')
    
    def getDayClass(self, Date, month):
        """
        return the class settings for that calendar day
        """
        css_class = ""
        if Date.month != month.month:
            css_class = css_class + "other-month "           
        if Date < datetime.date.today():
            css_class = css_class + "past-date "    
        if Date == datetime.date.today():
            css_class = css_class + "current-date "    
        return css_class.strip()
                
    def inThisMonth(self, day, month):
        return day.month == month.month
    
    def isHolyday(self, day):
        session = Session()
        query = session.query(domain.HolyDay).filter(schema.holydays.c.holyday_date == day)
        results = query.all()
        if results:
            return "checked"
        else:
            return
                        
        
    def update(self):
        """
        refresh the query
        """
        self.errors = []
        self.Date = getDisplayDate(self.request)
        if not self.Date:
            self.Date=datetime.date.today() 
        if self.request.form:
            if self.request.form.has_key('save'):
                self.insert_items(self.request.form)                                                          
        #self.query, self.Date = current_sitting_query(self.Date)        
        self.request.response.setCookie('display_date', datetime.date.strftime(self.Date,'%Y-%m-%d') )
        self.yearcalendar = calendar.Calendar(prefs.getFirstDayOfWeek()).yeardatescalendar(self.Date.year,3)         
        #self.monthname = datetime.date.strftime(self.Date,'%B %Y')
        #self.Data = self.getData()
    
    render = ViewPageTemplateFile ('templates/schedule_holyday_calendar.pt')
    
