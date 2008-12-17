# encoding: utf-8
import datetime, time
from zope import component

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.viewlet import viewlet
from zope.viewlet.manager import WeightOrderedViewletManager

from ore.alchemist import Session

from bungeni.core.workflows.question import states as question_wf_state
from bungeni.core.workflows.motion import states as motion_wf_state
from bungeni.core.workflows.bill import states as bill_wf_state
import bungeni.core.schema as schema
import bungeni.core.domain as domain
import bungeni.core.globalsettings as prefs

from bungeni.ui.i18n import MessageFactory as _

#from bungeni.core.workflows.question import states

class Manager(WeightOrderedViewletManager):
    """Workspace viewlet manager."""


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
            data['schedule_date_class'] = 'sc-after-' #+ datetime.date.strftime(result.approval_date + offset, '%Y-%m-%d')
            data_list.append(data)            
        return data_list
    
    
    def update(self):
        """
        refresh the query
        """
        session = Session()
        qfilter = ( schema.questions.c.status == self.state )
        
        questions = session.query(domain.Question).filter(qfilter)
        self.query = questions        




class DraftQuestionViewlet( QuestionInStateViewlet ):
    """
    display the postponed questions
    """    
    name = state = question_wf_state.draft
    list_id = "draft_questions"

class SubmittedQuestionViewlet( QuestionInStateViewlet ):
    """
    display the postponed questions
    """    
    name = state = question_wf_state.submitted   
    list_id = "submitted_questions"  
    
class ReceivedQuestionViewlet( QuestionInStateViewlet ):
    """
    display the postponed questions
    """    
    name = state = question_wf_state.received   
    list_id = "recieved_questions"     
        
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
    list_id = "admissible_questions"
   
class InadmissibleQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = state = question_wf_state.inadmissible
    list_id = "inadmissible_questions"
  
class ClarifyMPQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = state = question_wf_state.clarify_mp
    list_id = "clarify_mp_questions"  
 

class ClarifyClerkQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = state = question_wf_state.clarify_clerk
    list_id = "clarify_clerk_questions"  

class ResponsePendingQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = state = question_wf_state.response_pending
    list_id = "response_pending_questions" 



class DeferredQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = state = question_wf_state.deferred
    list_id = "deferred_questions" 

class ElapsedQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = state = question_wf_state.elapsed
    list_id = "elapsed_questions" 


class RespondedQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = state = question_wf_state.responded
    list_id = "responded_questions" 

class AnsweredQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = state = question_wf_state.answered
    list_id = "answered_questions" 

class WithdrawnQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = state = question_wf_state.withdrawn
    list_id = "withdrawn_questions" 


 
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

