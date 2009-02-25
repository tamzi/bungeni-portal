# encoding: utf-8
# Calendar for scheduling questions
# at the top the questions available for scheduling are displayed,
# below you have a calendar that displays the sittings
# to schedule drag the question to be scheduled to the sitting

import calendar, base64
import datetime, time
from types import ListType, StringTypes

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.publisher.browser import BrowserView
from zope.viewlet.manager import WeightOrderedViewletManager
from zope.viewlet import viewlet
import zope.interface
from zope.traversing.browser.absoluteurl import absoluteURL

from zc.resourcelibrary import need
from ore.alchemist import Session
from ore.workflow.interfaces import IWorkflowInfo

from interfaces import IScheduleCalendar, IScheduleItems, IScheduleHolydayCalendar, IPlenaryCalendar, IScheduleGroupCalendar
from bungeni.ui.utils import getDisplayDate
import bungeni.models.schema as schema
import bungeni.models.domain as domain

from bungeni.core.workflows.question import states as question_wf_state #[u"questionstates
from bungeni.core.workflows.motion import states as motion_wf_state #[u"motionstates
from bungeni.core.workflows.bill import states as bill_wf_state #[u"billstates
import bungeni.core.globalsettings as prefs

import sqlalchemy.sql.expression as sql
import sqlalchemy as rdb

from z3c.pt.texttemplate import ViewTextTemplateFile

import simplejson

### debug


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



def makeList( itemIds ):

    if type(itemIds) == ListType:
        return itemIds            
    elif type(itemIds) in StringTypes:
        # only one item in this list
        return [itemIds,]
    else:
         raise TypeError ("Form values must be of type string or list")

def getParliamentaryItem(item_id):
    """
    rweturn the item for a item_id
    """
    session = Session()
    scheduled_item = session.query(domain.Question).get(item_id)
    if scheduled_item:
        return scheduled_item
    scheduled_item = session.query(domain.Motion).get(item_id)
    if scheduled_item:
        return scheduled_item
    scheduled_item = session.query(domain.Bill).get(item_id)
    if scheduled_item:
        return scheduled_item
    scheduled_item = session.query(domain.AgendaItem).get(item_id)
    if scheduled_item:
        return scheduled_item


def getScheduledItem( schedule_id ):
    """
    return the item for a given schedule_id
    """
    session = Session()
    item_schedule_item = session.query(domain.ItemSchedule).get(schedule_id)   
    #scheduled_item = session.query(scheduled_items).filter(schema.items_schedule.c.schedule_id == schedule_id)[0]
    return getParliamentaryItem(item_schedule_item.item_id)

def getSitting( schedule_id ):
    session = Session()
    item_schedule_item = session.query(domain.ItemSchedule).get(schedule_id)
    return item_schedule_item

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
    
    def billSittingTooEarly( self, sitting, bill):
        """
        Elapsed days from date of publication for placement of bill	
        Configurable numeric value describing number of days after date of publication 
        of bill after which bill can be placed before the house
        """
        if sitting is None:
            return
        noOfDaysBeforeBillSchedule = prefs.getNoOfDaysBeforeBillSchedule()
        minScheduleDate = bill.publication_date + datetime.timedelta(noOfDaysBeforeBillSchedule)
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
        if (type(question) == domain.Question):
            return "Questions cannot be postponed in the calendar, use the workflow of the question instead" 
        #if type(question) == ScheduledQuestionItems:
        #    return "Questions cannot be postponed in the calendar, use the workflow of the question instead"     
        #if type(question) == ScheduledQuestionItems or (type(question) == domain.Question):
        #    if question.status == question_wf_state[u"questionstates.postponed:                
        #        return
        #    elif question.status == question_wf_state[u"questionstates.scheduled:
        #        return
        #    else:
        #        return "You cannot postpone this question"    
        elif (type(question) == domain.Motion):
            return "To postpone a motion drag it to the 'postponed motions' area"
        else:
            return "Unknown Item Type - you cannot drag this thing here"
            
    def admitQuestion(self, question):
        if (type(question) == domain.Question):
            return "Questions cannot be postponed in the calendar, use the workflow of the question instead"
        #if type(question) == ScheduledQuestionItems:
        #    return "Questions cannot be postponed in the calendar, use the workflow of the question instead" 
        #if type(question) == ScheduledQuestionItems or (type(question) == domain.Question):
        #    if question.status == question_wf_state[u"questionstates.postponed:                
        #        return "This question is postponed, you can schedule it by dropping it on a sitting"
        #    elif question.status == question_wf_state[u"questionstates.scheduled:
        #        return "To postpone a question drag it to the 'postponed questions' area"
        #    elif question.status == question_wf_state[u"questionstates.admissible:    
        #        return
        #    else:
        #        return "You cannot make this question admissible"    
        elif (type(question) == domain.Motion):
            return "To postpone a motion drag it to the 'postponed motions' area"
        else:
            return "Unknown Item Type - you cannot drag this thing here"
            
    def admitMotion(self, motion):
        if (type(motion) == domain.Motion):
            return "Motions cannot be postponed in the calendar, use the workflow of the motion instead"
        #if type(motion) == ScheduledMotionItems:
        #    return "Motions cannot be postponed in the calendar, use the workflow of the motion instead" 
        #if type(motion) == ScheduledMotionItems or (type(motion) == domain.Motion):
        #    if motion.status == motion_wf_state[u"motionstates.postponed:                
        #        return "This motion is postponed, you can schedule it by dropping it on a sitting"
        #    elif motion.status == motion_wf_state[u"motionstates.scheduled:
        #        return "To postpone a motion drag it to the 'postponed motions' area"
        #    elif motion.status == motion_wf_state[u"motionstates.admissible:  
        #        return  
        #    else:
        #        return "You cannot make this motion admissible"    
        elif (type(motion) == domain.Question):
            return "To postpone a question drag it to the 'postponed questions' area"
        else:
            return "Unknown Item Type - you cannot drag this thing here"            
        
    def postponeMotion(self, motion):  
        if (type(motion) == domain.Motion):
            return "Motions cannot be postponed in the calendar, use the workflow of the motion instead"          
        #if type(motion) == ScheduledMotionItems:
        #    return "Motions cannot be postponed in the calendar, use the workflow of the motion instead"  
        #if type(motion) == ScheduledMotionItems or (type(motion) == domain.Motion):
        #    if motion.status == motion_wf_state[u"motionstates.postponed:                
        #        return 
        #    elif motion.status == motion_wf_state[u"motionstates.scheduled:
        #        return
        #    else:
        #        return "You cannot postpone this motion"    
        elif (type(motion) == domain.Question):
            return "To postpone a Motion drag it to the 'postponed motions' area"
        else:
            return "Unknown Item Type - you cannot drag this thing here"
            
    def postponeAgendaItem(self, agendaitem):
        #if type(agendaitem) ==ScheduledAgendaItems:
        #    return "AgendaItems cannot be postponed in the calendar"
        if type(agendaitem) == domain.AgendaItem:
            return
        else:
            return "Unknown Item Type - you cannot drag this thing here"                        
             
    def postponeBill(self, bill):  
        #if type(bill) == ScheduledBillItems:
        #    return "Bills cannot be postponed in the calendar, use the workflow of the bill instead"  
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
                    sitting = getSitting(schedule_id)
                    schedule_sitting_id = sitting.sitting_id
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
                        if type(s_item) == domain.Question:
                            sitting_questions.append(s_item.question_id)
                        elif type(s_item) == domain.Motion:
                            sitting_motions.append(s_item.motion_id)
                        elif type(s_item) == domain.Bill:                            
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
        if (type(item) == domain.Question):
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
        elif (type(item) == domain.Motion):
            result = self.MotionScheduledInPast(sitting)
            if result:
                errors.append(result)  
            result = self.getDuplicateSchedule(item.motion_id, sitting_motions)
            if result:
                errors.append(result)
    
            #data = {'errors':['to many motions','motion scheduled to early'], 'warnings': ['more than 1 motion by mp...',]}
            data = {'errors': errors, 'warnings': warnings}
            return simplejson.dumps( data )
        elif (type(item) == domain.Bill):
            result = self.BillScheduledInPast(sitting)
            if result:
                errors.append(result)  
            result = self.getDuplicateSchedule(item.bill_id, sitting_bills)
            if result:
                errors.append(result)    
            result=self.billSittingTooEarly(sitting, item)    
            if result:
                warnings.append(result)
            #data = {'errors':['to many motions','motion scheduled to early'], 'warnings': ['more than 1 motion by mp...',]}
            data = {'errors': errors, 'warnings': warnings}
            return simplejson.dumps( data )   
        elif (type(item) == domain.AgendaItem):
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


def getCurrentSittingsQuery(start_date, end_date, session_id = None, group_id = None):
    """
    get all sittings for a specific session or group between start and end date
    """ 
    session=Session()
    start_datetime = datetime.datetime(start_date.year, start_date.month, start_date.day, 0,0,0)
    end_datetime = datetime.datetime(end_date.year, end_date.month, end_date.day, 23, 59 ,59)              
    end_datetime
    gsfilter = None
    if session_id:
        # a plenary session
        if not(group_id is  None):
            # you may either schedule for a group or a session not both!
            raise NotImplementedError
        gsfilter = sql.and_(
                schema.sittings.c.start_date.between(start_datetime, end_datetime),
                schema.sittings.c.session_id == session_id)        
    if group_id:
        # sittings for a group - committee, political group, ...        
        if not(session_id is  None):
            # you may either schedule for a group or a session not both!            
            raise NotImplementedError
        gsfilter = sql.and_(
                schema.sittings.c.start_date.between(start_datetime, end_datetime),
                schema.sittings.c.group_id == group_id)
    if not gsfilter:            
        # You must either schedule for a group or a session
        raise NotImplementedError 
    else:
        return session.query(domain.GroupSitting).filter(gsfilter).order_by(schema.sittings.c.start_date)
            
            
class Calendar( BrowserView ):
    __call__ = ViewPageTemplateFile("templates/schedule.pt")


class ScheduleGroupCalendar( BrowserView ):
    __call__ = ViewPageTemplateFile("templates/group_schedule.pt")

class ScheduleCalendarViewletManager( WeightOrderedViewletManager ):
    """
    manage the viewlets that make up the calendar view
    """
    zope.interface.implements(IScheduleCalendar) 

class ScheduleGroupCalendarViewletManager( WeightOrderedViewletManager ):
    """
    manage the viewlets that make up the calendar view
    """
    zope.interface.implements(IScheduleGroupCalendar) 



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
    name = question_wf_state[u"questionstates.postponed"].title
    state = question_wf_state[u"questionstates.postponed"].id   
    list_id = "postponed_questions"    
    
    
class AdmissibleQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"questionstates.admissible"].title
    state = question_wf_state[u"questionstates.admissible"].id
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
    name = motion_wf_state[u"motionstates.admissible"].title
    state = motion_wf_state[u"motionstates.admissible"].id
    list_id = "admissible_motions"
    

class PostponedMotionViewlet( MotionInStateViewlet ):   
    """
    display the admissible Motions
    """
    name = motion_wf_state[u"motionstates.postponed"].title
    state = motion_wf_state[u"motionstates.postponed"].id
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
        offset = datetime.timedelta(prefs.getNoOfDaysBeforeBillSchedule())
        for result in results:            
            data ={}
            data['qid']= ( 'b_' + str(result.bill_id) )                         
            data['subject'] = u'B ' + result.title
            data['title'] = result.title
            data['schedule_date_class'] = 'sc-after-'  + datetime.date.strftime(result.publication_date + offset, '%Y-%m-%d')
            data_list.append(data)            
        return data_list
    
    
    def update(self):
        """
        refresh the query
        """
        session = Session()
        bills = session.query(domain.Bill).filter(schema.bills.c.status.in_( [bill_wf_state[u"billstates.submitted"].id , 
                                                                                bill_wf_state[u"billstates.first_reading_postponed"].id ,
                                                                                bill_wf_state[u"billstates.second_reading_pending"].id , 
                                                                                bill_wf_state[u"billstates.second_reading_postponed"].id , 
                                                                                bill_wf_state[u"billstates.whole_house_postponed"].id ,
                                                                                bill_wf_state[u"billstates.house_pending"].id ,
                                                                                bill_wf_state[u"billstates.report_reading_postponed"].id ,                                                                                
                                                                                bill_wf_state[u"billstates.report_reading_pending"].id , 
                                                                                bill_wf_state[u"billstates.third_reading_pending"].id,
                                                                                bill_wf_state[u"billstates.third_reading_postponed"].id ]
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

class PlenaryAtomCalendar( BrowserView ):
    __call__ = ViewPageTemplateFile("templates/plenary-atom.pt")

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
                                    + ' - ' + datetime.datetime.strftime(result.end_date,'%H:%M')
                                    + ' (' + sit_types[result.sitting_type] + ')')
            data['start_date'] = result.start_date
            data['end_date'] = result.end_date
            data['start_time'] = result.start_date.time()
            data['end_time'] = result.end_date.time()            
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
        items = session.query(domain.ItemSchedule).filter(active_sitting_items_filter).order_by(schema.items_schedule.c.order)
        data_list=[] 
        #pdb.set_trace() 
        results = items.all()        
        q_offset = datetime.timedelta(prefs.getNoOfDaysBeforeQuestionSchedule())
        for iresult in results:            
            data ={}
            result = getParliamentaryItem(iresult.item_id)
            #data['qid']= ( 'q_' + str(result.question_id) ) 
            data['schedule_id'] = ( 'isid_' + str(iresult.schedule_id) ) # isid for ItemSchedule ID             
            if type(result) == domain.Question:                       
                data['subject'] = u'Q ' + str(result.question_number) + u' ' +  result.subject[:10] + u'... '
                data['title'] = result.subject
                data['type'] = "question"
                data['schedule_date_class'] = 'sc-after-' + datetime.date.strftime(result.approval_date + q_offset, '%Y-%m-%d')
                data['url'] = '/questions/obj-' + str(result.question_id)
            elif type(result) == domain.Motion:    
                data['subject'] = u'M ' + str(result.motion_number) + u' ' +result.title[:10] + u'... '
                data['title'] = result.title
                data['type'] = "motion"                
                data['schedule_date_class'] = 'sc-after-' + datetime.date.strftime(result.approval_date, '%Y-%m-%d')
                data['url'] = '/motions/obj-' + str(result.motion_id)
            elif type(result) == domain.Bill:    
                data['subject'] = u"B " + result.title[:10]  + u'... '
                data['title'] = result.title             
                data['type'] = "bill"
                data['schedule_date_class'] = 'sc-after-' + datetime.date.strftime(result.publication_date + q_offset, '%Y-%m-%d')
                data['url'] = '/bills/obj-' + str(result.bill_id)
            elif type(result) == domain.AgendaItem:    
                data['subject'] = u"" + result.title[:10]  + u'... '
                data['title'] = result.title             
                data['type'] = "agenda_item"
                data['schedule_date_class'] = 'sc-after-' + datetime.date.strftime(datetime.date.today(), '%Y-%m-%d')
                data['url'] = '/agendaitems/obj-' + str(result.agenda_item_id)                
                
            data['status'] = iresult.status
            data_list.append(data)            
        return data_list

    def getInactiveSittingItems(self, sitting_id):
        """
        return all questions assigned to that sitting
        """
        session = Session()
        active_sitting_items_filter = rdb.and_(schema.items_schedule.c.sitting_id == sitting_id, 
                                                schema.items_schedule.c.active == False)
        items = session.query(domain.ItemSchedule).filter(active_sitting_items_filter).order_by(schema.items_schedule.c.order)
        data_list=[] 
        results = items.all()
        for iresult in results:            
            data ={}
            result = getParliamentaryItem(iresult.item_id)
            data['schedule_id'] = ( 'isid_' + str(iresult.schedule_id) ) # isid for ItemSchedule ID 
            if type(result) == domain.Question:                       
                data['subject'] = u'Q ' + str(result.question_number) + u' ' +  result.subject[:10]
                data['title'] = result.subject
                data['type'] = "question"
                data['url'] = '/questions/obj-' + str(result.question_id)                
            elif type(result) == domain.Motion:    
                data['subject'] = u'M ' + str(result.motion_number) + u' ' +result.title[:10]
                data['title'] = result.title 
                data['type'] = "motion"
                data['url'] = '/motions/obj-' + str(result.motion_id)
            elif type(result) == domain.Bill:    
                data['subject'] = u"B " + result.title[:10]             
                data['title'] = result.title 
                data['type'] = "bill"
                data['url'] = '/bills/obj-' + str(result.bill_id)
            data['status'] = result.status
            data_list.append(data)            
        return data_list


       
       
                  
       
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
    
    render = ViewPageTemplateFile ('templates/schedule_calendar_viewlet.pt')


class WeeklyScheduleCalendarViewlet( ScheduleCalendarViewlet ):
    """
    a weekly calendar to schedule itmes for plenary or group sittings
    """
    
    def _getSittingTypes(self):
        session = Session()
        sitting_types = session.query( domain.SittingType ).all()
        data = {}
        for sitting_type in sitting_types:
            data[sitting_type.sitting_type_id] = {'start': sitting_type.start_time,
                                                  'end': sitting_type.end_time,
                                                  'type': sitting_type.sitting_type }
        return data                               
    
    
    def getDayHours(self):
        return range(7,21)
        
    def getHourStyle(self, hour):
        """
        <div class="hour even" style="top: 4em; height: 4em;">    
        """
        top = 'top: ' + str((hour - 7) * 4) + 'em; '
        height = 'height: 4em; position: absolute;'
        return top + height
            
    def getEventStyle(self, start, end):
        """
        get start and duration for event to position it
        style="top: 4em; height: 4em;
        """    
        top = 'top: ' + str( ((start.hour - 7) * 4) + ( start.minute / 15 ) ) + 'em; '
        td = end - start
        height = 'height: ' + str((float(td.seconds) / 900.0)) +  'em; position: absolute; background:blue;'
        return top + height
                
    def getDay(self, day):
        return datetime.date.strftime(day, '%A %d')
    
    def getWeek(self):
        for week in self.monthcalendar:
            if self.Date in week:
                return week

    def update(self):
        """
        refresh the query
        """      
        need("yui-core")    
        need("yui-container")
        need("yui-button") 
        need("yui-dragdrop")        
        session_id = None
        group_id = None            
        self.Date = getDisplayDate(self.request)
        if not self.Date:
            self.Date=datetime.date.today()                            
        self.request.response.setCookie('display_date', datetime.date.strftime(self.Date,'%Y-%m-%d') )
        self.monthcalendar = calendar.Calendar(prefs.getFirstDayOfWeek()).monthdatescalendar(self.Date.year,self.Date.month)         
        self.monthname = datetime.date.strftime(self.Date,'%B %Y')  
        self.weekcalendar =  self.getWeek()
        start_date = self.weekcalendar[0]      
        end_date = self.weekcalendar[-1]
        try:
            if self.context.__parent__.session_id:
                session_id = self.context.__parent__.session_id
        except:                
            if self.context.__parent__.group_id:
                group_id = self.context.__parent__.group_id    
        self.query = getCurrentSittingsQuery(start_date, end_date, session_id, group_id)
        self.Data = self.getData()
        self.sitting_types = self._getSittingTypes()

    render = ViewPageTemplateFile ('templates/schedule_week_calendar_viewlet.pt')

class ScheduleSittingWeekSubmit( BrowserView ):
    """
    get the values of the Ajax sitting schedule
    and schedule the sitting
    """
    
    def editSitting(self, formdata):
        session = Session()
        sitting_id = long(formdata['form_sitting_id'])
        sitting_type = long(formdata['form_sitting_type'])        
        sitting = session.query(domain.GroupSitting).get(sitting_id)        
        dt = time.strptime(formdata['form_sitting_date'],'%Y-%m-%d')
        ds = time.strptime(formdata['form_sitting_start'],'%H:%M:%S')
        de = time.strptime(formdata['form_sitting_end'],'%H:%M:%S')
        sitting.start_date = datetime.datetime( dt[0], dt[1], dt[2], ds[3], ds[4] )
        sitting.end_date = datetime.datetime( dt[0], dt[1], dt[2], de[3], de[4] )
        
    
    
    def addSitting(self, formdata):
        session = Session()
        sitting = domain.GroupSitting()
        #sitting_type = long(formdata['form_sitting_type'])                
        dt = time.strptime(formdata['form_sitting_date'],'%Y-%m-%d')
        ds = time.strptime(formdata['form_sitting_start'],'%H:%M:%S')
        de = time.strptime(formdata['form_sitting_end'],'%H:%M:%S')
        sitting.start_date = datetime.datetime( dt[0], dt[1], dt[2], ds[3], ds[4] )
        sitting.end_date = datetime.datetime( dt[0], dt[1], dt[2], de[3], de[4] )
        sitting.sitting_type = 1L #sitting_type
        sitting.group_id = self.context.__parent__.group_id
        session.save(sitting)        
        
    def __call__( self ):
        errors = []
        warnings = []        
        data = {'errors': errors, 'warnings': warnings}
        form_data = self.request.form
        print form_data
        if form_data:
            if form_data.has_key('form_sitting_id'):
                if form_data['form_sitting_id']:
                    self.editSitting(form_data) 
                else:
                    self.addSitting(form_data)    
            else:
                self.addSitting(form_data)   
        


class ScheduleSittingSubmitViewlet ( viewlet.ViewletBase ):
    """
    this only gets the posted values and inserts them into the db           
    and reports any errors the might occur
    """
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
                    IWorkflowInfo(question).fireTransitionToward(question_wf_state[u"questionstates.scheduled"].id, check_security=True)
                    item_schedule.status = IWorkflowInfo(question).state().getState()
                    session.commit()
                except:
                    session.rollback()
                    #rollback leave a inactive session behind, so it has to be closed manually
                    session.close()
                    self.errors.append("Question could not be scheduled")  
                    
                #if IWorkflowInfo(question).state().getState() == question_wf_state[u"questionstates.admissible:
                #    IWorkflowInfo(question).fireTransition('schedule', check_security=True)
                #elif IWorkflowInfo(question).state().getState() == question_wf_state[u"questionstates.deferred:
                #    IWorkflowInfo(question).fireTransition('schedule-deferred', check_security=True)
                #elif IWorkflowInfo(question).state().getState() == question_wf_state[u"questionstates.postponed:
                #    IWorkflowInfo(question).fireTransition('schedule-postponed', check_security=True)
                #else:
                #    print "invalid workflow state:", IWorkflowInfo(question).state().getState()
                        
#                elif question.sitting_id != sitting_id:  
#                    # a question with a sitting id is scheduled
#                    assert IWorkflowInfo(question).state().getState() == question_wf_state[u"questionstates.scheduled                  
#                    IWorkflowInfo(question).fireTransition('postpone', check_security=True)
#                    #assert question.sitting_id is None
#                    #question.sitting_id = sitting_id
#                    IWorkflowInfo(question).fireTransition('schedule-postponed', check_security=True)
#                else:
#                    #sitting stays the same - nothing to do
#                    #print question.sitting_id == sitting_id
#                    pass
            else:              
                if IWorkflowInfo(question).state().getState() == question_wf_state[u"questionstates.scheduled"].id:
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
                if bill.status in [bill_wf_state[u"billstates.submitted"].id , 
                    bill_wf_state[u"billstates.first_reading_postponed"].id ,
                    bill_wf_state[u"billstates.second_reading_pending"].id , 
                    bill_wf_state[u"billstates.second_reading_postponed"].id , 
                    bill_wf_state[u"billstates.whole_house_postponed"].id ,
                    bill_wf_state[u"billstates.house_pending"].id ,
                    bill_wf_state[u"billstates.report_reading_postponed"].id ,                                                                                
                    bill_wf_state[u"billstates.report_reading_pending"].id , 
                    bill_wf_state[u"billstates.third_reading_pending"].id,
                    bill_wf_state[u"billstates.third_reading_postponed"].id ]:
                    item_schedule.sitting_id = sitting_id
                    item_schedule.item_id = bill_id
                    item_schedule.order = sort_id
                    session.save(item_schedule) 
                    if bill.status in [bill_wf_state[u"billstates.submitted"].id , bill_wf_state[u"billstates.first_reading_postponed"].id]:
                        IWorkflowInfo(bill).fireTransitionToward(bill_wf_state[u"billstates.first_reading"].id, check_security=True)
                    elif bill.status in [bill_wf_state[u"billstates.second_reading_pending"].id, bill_wf_state[u"billstates.second_reading_postponed"].id ]:
                        IWorkflowInfo(bill).fireTransitionToward(bill_wf_state[u"billstates.second_reading"].id, check_security=True)
                    elif bill.status in [bill_wf_state[u"billstates.report_reading_postponed"].id ,bill_wf_state[u"billstates.report_reading_pending"].id]:
                        IWorkflowInfo(bill).fireTransitionToward(bill_wf_state[u"billstates.report_reading"].id, check_security=True)
                    elif bill.status in [bill_wf_state[u"billstates.third_reading_pending"].id, bill_wf_state[u"billstates.third_reading_postponed"].id ]:
                        IWorkflowInfo(bill).fireTransitionToward(bill_wf_state[u"billstates.third_reading"].id, check_security=True)
                    elif bill.status in [  bill_wf_state[u"billstates.house_pending"].id, bill_wf_state[u"billstates.whole_house_postponed"].id ]:
                        IWorkflowInfo(bill).fireTransitionToward(bill_wf_state[u"billstates.whole_house"].id, check_security=True)   
                    item_schedule.status = bill.status                     
                elif bill.status in [bill_wf_state[u"billstates.first_reading"].id ,
                    bill_wf_state[u"billstates.second_reading"].id , 
                    bill_wf_state[u"billstates.whole_house"].id ,
                    bill_wf_state[u"billstates.report_reading"].id ,                                                                                
                    bill_wf_state[u"billstates.third_reading"].id]:
                    # schedule on multiple days
                    item_schedule.sitting_id = sitting_id
                    item_schedule.item_id = bill_id
                    item_schedule.order = sort_id
                    item_schedule.status = bill.status 
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
                    if IWorkflowInfo(motion).state().getState() != motion_wf_state[u"motionstates.scheduled"].id:              
                        # scheduling is possible for multipe sittings                    
                        IWorkflowInfo(motion).fireTransitionToward(motion_wf_state[u"motionstates.scheduled"].id, check_security=True)   
                    item_schedule.status = IWorkflowInfo(motion).state().getState()
                    session.commit()
                except:
                    self.errors.append("Motion could not be scheduled")    
                    session.rollback()
                    session.close()
            else:
                if IWorkflowInfo(motion).state().getState() == motion_wf_state[u"motionstates.scheduled"].id:
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
                item = getScheduledItem(scheduled_item_id) # session.query(domainItems).filter(schema.items_schedule.c.schedule_id == scheduled_item_id).one()
                sitting = getSitting(scheduled_item_id)
                if sitting.sitting_id == sitting_id:
                    #same sitting no workflow actions just update the sort_id
                    item.order = sort_id
                else:
                    #item was moved from one sitting to another                     
                    raise NotImplementedError( "A scheduled item cannot be rescheduled" )
                    if type(item) == domain.Question:
                        question_id = item.question_id
                        self.schedule_question(question_id, None, 0)
                        self.schedule_question(question_id, sitting_id, sort_id)
                    elif type(item) == domain.Bill:
                        bill_id = item.question_id
                        self.schedule_question(bill_id, None, 0)
                        self.schedule_bill(bill_id, sitting_id, sort_id)
                    elif type(item) == domain.Motion:
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
                item = getScheduledItem(scheduled_item_id) 
                #item = session.query(ScheduledItems).filter(schema.items_schedule.c.schedule_id == scheduled_item_id).one()
                if type(item) == domain.Question:
                    question_id = item.question_id
                    self.schedule_question(question_id, None, 0)
                elif type(item) == domain.Bill:
                    pass
                elif type(item) == domain.Motion:
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
                
    render =  ViewPageTemplateFile ('templates/schedule_sitting_submit_viewlet.pt')
    
class SittingCalendarWeekViewlet(ScheduleCalendarViewlet):
    """
    display only the current week
    """
    render = ViewPageTemplateFile('templates/sitting_week_calendar_viewlet.pt')

    def getWeek(self):
        for week in self.monthcalendar:
            if self.Date in week:
                return week
                         
    
    
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
    

class ScheduleSittingDragDropViewlet(viewlet.ViewletBase):
    """Get the markup and javascript for the YUI Drag and Drop."""

    template = ViewTextTemplateFile("templates/dragdrop.pt")
    
    def update(self):
        need('yui-dragdrop')
        need('yui-animation')
        need('yui-json')

        # for debugging
        need('yui-logger')

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
        approved_questions = session.query(domain.Question).filter(schema.questions.c.status == question_wf_state[u"questionstates.admissible"].id ).distinct()
        results = approved_questions.all()
        for result in results:
            self.approved_question_ids.append(result.question_id)
        agenda_items = session.query(domain.AgendaItem)
        results = agenda_items.all()
        for result in results:
            self.agenda_item_ids.append(result.agenda_item_id)                
        postponed_questions = session.query(domain.Question).filter(schema.questions.c.status == question_wf_state[u"questionstates.postponed"].id).distinct()
        results = postponed_questions.all()
        for result in results:
            self.postponed_question_ids.append(result.question_id)  
        approved_motions = session.query(domain.Motion).filter(schema.motions.c.status == motion_wf_state[u"motionstates.admissible"].id).distinct()
        results = approved_motions.all()
        for result in results:
            self.approved_motion_ids.append(result.motion_id) 
        postponed_motions = session.query(domain.Motion).filter(schema.motions.c.status == motion_wf_state[u"motionstates.postponed"].id).distinct()
        results = postponed_motions.all()              
        for result in results:
            self.postponed_motion_ids.append(result.motion_id) 
        bills = session.query(domain.Bill).filter(schema.bills.c.status.in_( [bill_wf_state[u"billstates.submitted"].id , 
                                                                                bill_wf_state[u"billstates.first_reading_postponed"].id ,
                                                                                bill_wf_state[u"billstates.second_reading_pending"].id , 
                                                                                bill_wf_state[u"billstates.second_reading_postponed"].id , 
                                                                                bill_wf_state[u"billstates.whole_house_postponed"].id ,
                                                                                bill_wf_state[u"billstates.house_pending"].id ,
                                                                                bill_wf_state[u"billstates.report_reading_postponed"].id ,                                                                                
                                                                                bill_wf_state[u"billstates.report_reading_pending"].id , 
                                                                                bill_wf_state[u"billstates.third_reading_pending"].id,
                                                                                bill_wf_state[u"billstates.third_reading_postponed"].id ]
                                                                                ))  
        results = bills.all()
        for result in results:
            self.bill_ids.append(result.bill_id)                                                                                            
        sittings, self.Date = current_sitting_query(self.Date)    
        results = sittings.all()     
        for result in results:
            self.sitting_ids.append(result.sitting_id)     
       
        dd_scheduled_items =  session.query(domain.ItemSchedule).filter( rdb.and_(schema.items_schedule.c.sitting_id.in_(self.sitting_ids), 
                                                                    schema.items_schedule.c.active == True))
        
        
        
        results = dd_scheduled_items.all()
        for result in results:
            self.scheduled_item_ids.append(result.schedule_id)    
        cal = calendar.Calendar(prefs.getFirstDayOfWeek())    
        for t_date in cal.itermonthdates(self.Date.year, self.Date.month):
            self.table_date_ids.append('"tdid-' + datetime.date.strftime(t_date,'%Y-%m-%d"'))                 

    def render(self):
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
            'currentDateId': currentDateId
            }

        return self.template(**js_inserts)

    
