# encoding: utf-8
import datetime

from zope.app.pagetemplate import ViewPageTemplateFile

from zope.viewlet import viewlet
from zope.viewlet.manager import WeightOrderedViewletManager

from ore.alchemist import Session

from bungeni.core.workflows.question import states as question_wf_state #[u"questionstates
from bungeni.core.workflows.motion import states as motion_wf_state #[u"motionstates
from bungeni.core.workflows.bill import states as bill_wf_state #[u"billstates
import bungeni.models.schema as schema
import bungeni.models.domain as domain
import bungeni.core.globalsettings as prefs

#from bungeni.ui.i18n import MessageFactory as _


class Manager(WeightOrderedViewletManager):
    """Workspace viewlet manager."""


class QuestionInStateViewlet( viewlet.ViewletBase ):
    name = state = None
    render = ViewPageTemplateFile ('templates/workspace_item_viewlet.pt')    
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
            if result.question_number:                       
                data['subject'] = u'Q ' + str(result.question_number) + u' ' + result.subject
            else:
                data['subject'] = result.subject
            data['title'] = result.subject
            data['schedule_date_class'] = 'sc-after-' #+ datetime.date.strftime(result.approval_date + offset, '%Y-%m-%d')
            data['url'] = '/questions/obj-' + str(result.question_id)
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

class MyQuestionsViewlet( viewlet.ViewletBase ):
    name = u"My Questions"
    render = ViewPageTemplateFile ('templates/workspace_item_viewlet.pt')    
    list_id = "my_questions"    
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
            if result.question_number:                       
                data['subject'] = u'Q ' + str(result.question_number) + u' ' + result.subject + ' (' + result.status + ')'
            else:
                data['subject'] = result.subject + ' (' + result.status + ')'
            data['title'] = result.subject + ' (' + result.status + ')'
            data['schedule_date_class'] = 'sc-after-' #+ datetime.date.strftime(result.approval_date + offset, '%Y-%m-%d')
            data['url'] = '/questions/obj-' + str(result.question_id)
            data_list.append(data)            
        return data_list
    
    
    def update(self):
        """
        refresh the query
        """
        session = Session()
        try:
            user_id = self.request.principal.user_id    
        except:
            user_id = None     
        qfilter = ( schema.questions.c.owner_id == user_id )
        
        questions = session.query(domain.Question).filter(qfilter).order_by(schema.questions.c.question_id.desc())
        self.query = questions        
            
class MyMotionsViewlet( viewlet.ViewletBase ):
    name = "My Motions"
    render = ViewPageTemplateFile ('templates/workspace_item_viewlet.pt')    
    list_id = "my_motions"    
    def getData(self):
        """
        return the data of the query
        """      
        data_list = []
        results = self.query.all()
       
        for result in results:            
            data ={}
            data['qid']= ( 'm_' + str(result.motion_id) )  
            if result.motion_number:                       
                data['subject'] = u'M ' + str(result.motion_number) + u' ' +  result.title  + ' (' + result.status + ')'
            else:
                data['subject'] =  result.title  + ' (' + result.status + ')'
            data['title'] = result.title  + ' (' + result.status + ')'
            data['schedule_date_class'] = 'sc-after-'  #+ datetime.date.strftime(result.approval_date, '%Y-%m-%d')
            data['url'] = '/motions/obj-' + str(result.motion_id)
            data_list.append(data)            
        return data_list
    
    
    def update(self):
        """
        refresh the query
        """
        session = Session()
        try:
            user_id = self.request.principal.user_id    
        except:
            user_id = None     
        qfilter = ( schema.motions.c.owner_id == user_id )        
        motions = session.query(domain.Motion).filter(qfilter)
        self.query = motions        



class DraftQuestionViewlet( QuestionInStateViewlet ):
    """
    display the draft questions
    """    
    name = question_wf_state[u"questionstates.draft"].title
    state = question_wf_state[u"questionstates.draft"].id
    list_id = "draft_questions"

class SubmittedQuestionViewlet( QuestionInStateViewlet ):
    """
    display the submitted questions
    """    
    name = question_wf_state[u"questionstates.submitted"].title
    state =  question_wf_state[u"questionstates.submitted"].id   
    list_id = "submitted_questions"  
    
class ReceivedQuestionViewlet( QuestionInStateViewlet ):
    """
    display the recieved questions
    """    
    name = question_wf_state[u"questionstates.received"].title
    state = question_wf_state[u"questionstates.received"].id   
    list_id = "recieved_questions"     
    
class ScheduledQuestionViewlet( QuestionInStateViewlet ): 
    name = question_wf_state[u"questionstates.scheduled"].title
    state = question_wf_state[u"questionstates.scheduled"].id
    list_id = "scheduled_questions"     
        
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
    list_id = "admissible_questions"
   
class InadmissibleQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"questionstates.inadmissible"].title
    state = question_wf_state[u"questionstates.inadmissible"].id
    list_id = "inadmissible_questions"
  
class ClarifyMPQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"questionstates.clarify_mp"].title
    state = question_wf_state[u"questionstates.clarify_mp"].id
    list_id = "clarify_mp_questions"  
 

class ClarifyClerkQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"questionstates.clarify_clerk"].title
    state = question_wf_state[u"questionstates.clarify_clerk"].id
    list_id = "clarify_clerk_questions"  

class ResponsePendingQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"questionstates.response_pending"].title
    state = question_wf_state[u"questionstates.response_pending"].id
    list_id = "response_pending_questions" 

class CompleteQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"questionstates.complete"].title
    state = question_wf_state[u"questionstates.complete"].id
    list_id = "complete_questions" 

class DeferredQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"questionstates.deferred"].title
    state = question_wf_state[u"questionstates.deferred"].id
    list_id = "deferred_questions" 

class ElapsedQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"questionstates.elapsed"].title
    state = question_wf_state[u"questionstates.elapsed"].id
    list_id = "elapsed_questions" 


class RespondedQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"questionstates.responded"].title
    state = question_wf_state[u"questionstates.responded"].id
    list_id = "responded_questions" 

class AnsweredQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"questionstates.answered"].title
    state = question_wf_state[u"questionstates.answered"].id
    list_id = "answered_questions" 

class WithdrawnQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"questionstates.withdrawn"].title
    state = question_wf_state[u"questionstates.withdrawn"].id
    list_id = "withdrawn_questions" 

#"Question pending response"


 
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
            data['url'] = '/motions/obj-' + str(result.motion_id)
            data_list.append(data)            
        return data_list
    
    
    def update(self):
        """
        refresh the query
        """
        session = Session()
        motions = session.query(domain.Motion).filter(schema.motions.c.status == self.state)
        self.query = motions        


class SubmittedMotionViewlet( MotionInStateViewlet ):   
    """
    display the submitted Motions
    """
    name = motion_wf_state[u"motionstates.submitted"].title
    state = motion_wf_state[u"motionstates.submitted"].id
    list_id = "submitted_motions"


class ReceivedMotionViewlet( MotionInStateViewlet ):   
    """
    display the submitted Motions
    """
    name = motion_wf_state[u"motionstates.received"].title
    state = motion_wf_state[u"motionstates.received"].id
    list_id = "received_motions"

class CompleteMotionViewlet( MotionInStateViewlet ):   
    """
    display the submitted Motions
    """
    name = motion_wf_state[u"motionstates.complete"].title
    state = motion_wf_state[u"motionstates.complete"].id
    list_id = "complete_motions"
    
   

class ClarifyMpMotionViewlet( MotionInStateViewlet ):   
    """
    display the submitted Motions
    """
    name = motion_wf_state[u"motionstates.clarify_mp"].title
    state = motion_wf_state[u"motionstates.clarify_mp"].id
    list_id = "clarify_mp_motions"
    
class ClarifyClerkMotionViewlet( MotionInStateViewlet ):   
    """
    display the submitted Motions
    """
    name = motion_wf_state[u"motionstates.clarify_clerk"].title
    state = motion_wf_state[u"motionstates.clarify_clerk"].id
    list_id = "clarify_clerk_motions"    

class DeferredMotionViewlet( MotionInStateViewlet ):   
    """
    display the submitted Motions
    """
    name =  motion_wf_state[u"motionstates.deferred"].title
    state = motion_wf_state[u"motionstates.deferred"].id
    list_id = "deferred_motions"    
    
    
    
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

