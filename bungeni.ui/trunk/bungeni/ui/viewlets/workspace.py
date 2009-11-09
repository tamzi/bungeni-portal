# encoding: utf-8
import datetime

import sqlalchemy.sql.expression as sql

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.viewlet import viewlet

from ore.alchemist import Session
from ore.workflow import interfaces

from bungeni.core.workflows.question import states as question_wf_state #[u"questionstates
from bungeni.core.workflows.motion import states as motion_wf_state #[u"motionstates
from bungeni.core.workflows.bill import states as bill_wf_state #[u"billstates
from bungeni.core.workflows.tableddocument import states as tableddocument_wf_state
from bungeni.core.workflows.agendaitem import states as agendaitem_wf_state

from bungeni.models import utils
import bungeni.models.schema as schema
import bungeni.models.domain as domain
import bungeni.core.globalsettings as prefs

#from bungeni.ui.i18n import MessageFactory as _

def get_wf_state(item):
    # return human readable workflow title
    wf = interfaces.IWorkflow(item) 
    wf_state = interfaces.IWorkflowState(
        item).getState()
    return wf.workflow.states[wf_state].title    



class ViewletBase(viewlet.ViewletBase):
    render = ViewPageTemplateFile ('templates/workspace_item_viewlet.pt')

class UserIdViewlet(viewlet.ViewletBase):
    """ display the users
    principal id """
    principal_id = None
    
    def __init__( self,  context, request, view, manager ):        

        self.context = context
        self.request = request
        self.__parent__= context
        self.manager = manager
        
    def update(self):
        self.principal_id = utils.getUserId()
        
    render = ViewPageTemplateFile ('../forms/templates/user_id.pt')        
    
class QuestionInStateViewlet( ViewletBase ):
    name = state = None

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
                data['subject'] = u'Q ' + str(result.question_number) + u' ' + result.short_name
            else:
                data['subject'] = result.short_name
            data['title'] = result.short_name
            data['result_item_class'] = 'workflow-state-' + result.status
            data['url'] = '/business/questions/obj-' + str(result.question_id)
            data['status'] = get_wf_state(result)
            data['owner'] = "%s %s" %(result.owner.first_name, result.owner.last_name)
            data['type'] =  result.type.capitalize()
            data_list.append(data)            
        return data_list
    
    
    def update(self):
        """
        refresh the query
        """
        session = Session()
        qfilter = ( domain.Question.status == self.state )
        
        questions = session.query(domain.Question).filter(qfilter)
        self.query = questions        

class MyQuestionsViewlet( ViewletBase ):
    name = u"My Questions"
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
                data['subject'] = u'Q ' + str(result.question_number) + u' ' + result.short_name 
            else:
                data['subject'] = result.short_name 
            data['title'] = result.short_name + ' (' + result.status + ')'
            data['result_item_class'] = 'workflow-state-' + result.status 
            data['url'] = '/business/questions/obj-' + str(result.question_id)
            data['status'] = get_wf_state(result)
            data['owner'] = "%s %s" %(result.owner.first_name, result.owner.last_name)
            data['type'] =  result.type.capitalize()            
            data_list.append(data)            
        return data_list
    
    
    def update(self):
        """
        refresh the query
        """
        session = Session()
        try:
            user_id = self._parent.user_id    
        except:
            user_id = None     
        qfilter = ( domain.Question.owner_id == user_id )
        
        questions = session.query(domain.Question).filter(qfilter).order_by(domain.Question.question_id.desc())
        self.query = questions        
            
class MyMotionsViewlet( ViewletBase ):
    name = "My Motions"
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
                data['subject'] = u'M ' + str(result.motion_number) + u' ' +  result.short_name 
            else:
                data['subject'] =  result.short_name 
            data['title'] = result.short_name  + ' (' + result.status + ')'
            data['result_item_class'] = 'workflow-state-' + result.status             
            data['url'] = '/business/motions/obj-' + str(result.motion_id)
            data['status'] = get_wf_state(result)
            data['owner'] = "%s %s" %(result.owner.first_name, result.owner.last_name)
            data['type'] =  result.type.capitalize()            
            data_list.append(data)            
        return data_list
    
    
    def update(self):
        """
        refresh the query
        """
        session = Session()
        try:
            user_id = self._parent.user_id    
        except:
            user_id = None     
        qfilter = ( domain.Motion.owner_id == user_id )        
        motions = session.query(domain.Motion).filter(qfilter)
        self.query = motions        

class MyGroupsViewlet( ViewletBase ):
    name = "My Groups"
    list_id = "my_groups"    
    def getData(self):
        """
        return the data of the query
        """      
        data_list = []
        results = self.query.all()
        parliament_id = self._parent.context.parliament_id
        government_id = self._parent.government_id
        for result in results:            
            data ={}
            data['qid']= ( 'g_' + str(result.group_id) )              
            data['subject'] = result.short_name
            data['title'] = result.short_name  + ' (' + result.type + ')'
            data['result_item_class'] = 'workflow-state-' + result.status   
            url = "/archive/browse/parliaments/obj-" + str(parliament_id) 
            if type(result) == domain.Parliament:
                data['url'] = url
            elif type(result) == domain.Committee:   
                #data['url'] = url + '/committees/obj-' + str(result.group_id) 
                data['url'] = ('/groups/' + 
                    result.parent_group.group_principal_id + 
                    '/' + result.group_principal_id)
            elif type(result) == domain.PoliticalParty:   
                data['url'] = url + '/politicalparties/obj-' + str(result.group_id)                                                  
            elif type(result) == domain.Ministry:   
                data['url'] = url + ('/governments/obj-%s/ministries/obj-%s' % (
                        str(government_id), str(result.group_id) ))                                      
            else:               
                data['url'] = '#' 
            data['status'] = get_wf_state(result)
            data['owner'] = ""
            data['type'] =  result.type.capitalize()            
            data_list.append(data)            
        return data_list
    
    
    def update(self):
        """
        refresh the query
        """
        session = Session()
        user_id = self._parent.user_id    
        parliament_id = self._parent.context.parliament_id
        group_ids = self._parent.user_group_ids
        gfilter = sql.and_(domain.Group.group_id.in_(group_ids),
                            domain.Group.status == 'active')
        groups = session.query(domain.Group).filter(gfilter)
        self.query = groups            



class DraftQuestionViewlet( QuestionInStateViewlet ):
    """
    display the draft questions
    """    
    name = question_wf_state[u"draft"].title
    state = question_wf_state[u"draft"].id
    list_id = "draft_questions"

    def update(self):
        """
        refresh the query
        """
        super(DraftQuestionViewlet, self).update()
        session = Session()
        try:
            user_id = self._parent.user_id    
        except:
            user_id = None     
        qfilter = ( domain.Question.owner_id == user_id )        
        self.query = self.query.filter(qfilter).order_by(domain.Question.question_id.desc())  

class SubmittedQuestionViewlet( QuestionInStateViewlet ):
    """
    display the submitted questions
    """    
    name = question_wf_state[u"submitted"].title
    state =  question_wf_state[u"submitted"].id   
    list_id = "submitted_questions"  
    
class ReceivedQuestionViewlet( QuestionInStateViewlet ):
    """
    display the recieved questions
    """    
    name = question_wf_state[u"received"].title
    state = question_wf_state[u"received"].id   
    list_id = "recieved_questions"     
    
class ScheduledQuestionViewlet( QuestionInStateViewlet ): 
    name = question_wf_state[u"scheduled"].title
    state = question_wf_state[u"scheduled"].id
    list_id = "scheduled_questions"     
        
class PostponedQuestionViewlet( QuestionInStateViewlet ):
    """
    display the postponed questions
    """    
    name = question_wf_state[u"postponed"].title
    state = question_wf_state[u"postponed"].id   
    list_id = "postponed_questions"    
    
    
class AdmissibleQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"admissible"].title
    state = question_wf_state[u"admissible"].id
    list_id = "admissible_questions"
   
class InadmissibleQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"inadmissible"].title
    state = question_wf_state[u"inadmissible"].id
    list_id = "inadmissible_questions"
  
class ClarifyMPQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"clarify_mp"].title
    state = question_wf_state[u"clarify_mp"].id
    list_id = "clarify_mp_questions"  
    
    def update(self):
        super(ClarifyMPQuestionViewlet, self).update()
        session = Session()
        try:
            user_id = self._parent.user_id    
        except:
            user_id = None     
        qfilter = ( domain.Question.owner_id == user_id )        
        self.query = self.query.filter(qfilter).order_by(domain.Question.question_id.desc())
 

class ClarifyClerkQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"clarify_clerk"].title
    state = question_wf_state[u"clarify_clerk"].id
    list_id = "clarify_clerk_questions"  

class ResponsePendingQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"response_pending"].title
    state = question_wf_state[u"response_pending"].id
    list_id = "response_pending_questions" 

class CompleteQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"complete"].title
    state = question_wf_state[u"complete"].id
    list_id = "complete_questions" 

class DeferredQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"deferred"].title
    state = question_wf_state[u"deferred"].id
    list_id = "deferred_questions" 

class ElapsedQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"elapsed"].title
    state = question_wf_state[u"elapsed"].id
    list_id = "elapsed_questions" 


class RespondedQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"responded"].title
    state = question_wf_state[u"responded"].id
    list_id = "responded_questions" 

class AnsweredQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"answered"].title
    state = question_wf_state[u"answered"].id
    list_id = "answered_questions" 

class WithdrawnQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = question_wf_state[u"withdrawn"].title
    state = question_wf_state[u"withdrawn"].id
    list_id = "withdrawn_questions" 

#"Question pending response"


 
class MotionInStateViewlet( ViewletBase ):  
    name = state = None
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
            data['subject'] = u'M ' + str(result.motion_number) + u' ' +  result.short_name
            data['title'] = result.short_name
            if result.approval_date:
                data['result_item_class'] = ('workflow-state-' + 
                    result.status  + 'sc-after-' + 
                    datetime.date.strftime(result.approval_date, '%Y-%m-%d'))
            else:         
                data['result_item_class'] = 'workflow-state-' + result.status       
            data['url'] = '/business/motions/obj-' + str(result.motion_id)
            data['status'] = get_wf_state(result)
            data['owner'] = "%s %s" %(result.owner.first_name, result.owner.last_name)
            data['type'] =  result.type.capitalize()            
            data_list.append(data)            
        return data_list
    
    
    def update(self):
        """
        refresh the query
        """
        session = Session()
        motions = session.query(domain.Motion).filter(domain.Motion.status == self.state)
        self.query = motions        


class SubmittedMotionViewlet( MotionInStateViewlet ):   
    """
    display the submitted Motions
    """
    name = motion_wf_state[u"submitted"].title
    state = motion_wf_state[u"submitted"].id
    list_id = "submitted_motions"


class ReceivedMotionViewlet( MotionInStateViewlet ):   
    """
    display the submitted Motions
    """
    name = motion_wf_state[u"received"].title
    state = motion_wf_state[u"received"].id
    list_id = "received_motions"

class CompleteMotionViewlet( MotionInStateViewlet ):   
    """
    display the submitted Motions
    """
    name = motion_wf_state[u"complete"].title
    state = motion_wf_state[u"complete"].id
    list_id = "complete_motions"
    
   

class ClarifyMpMotionViewlet( MotionInStateViewlet ):   
    """
    display the submitted Motions
    """
    name = motion_wf_state[u"clarify_mp"].title
    state = motion_wf_state[u"clarify_mp"].id
    list_id = "clarify_mp_motions"
    
class ClarifyClerkMotionViewlet( MotionInStateViewlet ):   
    """
    display the submitted Motions
    """
    name = motion_wf_state[u"clarify_clerk"].title
    state = motion_wf_state[u"clarify_clerk"].id
    list_id = "clarify_clerk_motions"    

class DeferredMotionViewlet( MotionInStateViewlet ):   
    """
    display the submitted Motions
    """
    name =  motion_wf_state[u"deferred"].title
    state = motion_wf_state[u"deferred"].id
    list_id = "deferred_motions"    
    
    
    
class AdmissibleMotionViewlet( MotionInStateViewlet ):   
    """
    display the admissible Motions
    """
    name = motion_wf_state[u"admissible"].title
    state = motion_wf_state[u"admissible"].id
    list_id = "admissible_motions"
    

class PostponedMotionViewlet( MotionInStateViewlet ):   
    """
    display the admissible Motions
    """
    name = motion_wf_state[u"postponed"].title
    state = motion_wf_state[u"postponed"].id
    list_id = "postponed_motions"

class BillItemsViewlet( ViewletBase ): 
    """
    Display all bills that can be scheduled for a parliamentary sitting
    """  
    name  = u"Bills"
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
            data['subject'] = result.short_name
            data['title'] = result.short_name
            data['result_item_class'] = ('workflow-state-' + 
                result.status )
            data['url'] = '/business/%ss/obj-%i' %(result.type, 
                            result.parliamentary_item_id)   
            data['status'] = get_wf_state(result)
            data['owner'] = "%s %s" %(result.owner.first_name, result.owner.last_name)
            data['type'] =  result.type.capitalize()                                         
            data_list.append(data)            
        return data_list
    
    
    def update(self):
        """
        refresh the query
        """
        session = Session()
        bills = session.query(domain.Bill).filter(domain.Bill.status.in_( [bill_wf_state[u"submitted"].id , 
                                                                                bill_wf_state[u"first_reading_postponed"].id ,
                                                                                bill_wf_state[u"second_reading_pending"].id , 
                                                                                bill_wf_state[u"second_reading_postponed"].id , 
                                                                                bill_wf_state[u"whole_house_postponed"].id ,
                                                                                bill_wf_state[u"house_pending"].id ,
                                                                                bill_wf_state[u"report_reading_postponed"].id ,                                                                                
                                                                                bill_wf_state[u"report_reading_pending"].id , 
                                                                                bill_wf_state[u"third_reading_pending"].id,
                                                                                bill_wf_state[u"third_reading_postponed"].id ]
                                                                                ))
        self.query = bills            

class DraftBillViewlet(BillItemsViewlet):
    name  = u"Draft Bills"
    list_id = "draft_bills"

    def update(self):
        """
        refresh the query
        """
        session = Session()
        bills = session.query(domain.Bill).filter(domain.Bill.status.in_( [bill_wf_state[u"draft"].id]
                                                                                ))
        self.query = bills            



class ItemInStageViewlet( ViewletBase ):
    """
    Group parliamentary items per stage:
    e.g. action required, in progress, answered/debated,
    'dead' (withdrawn, elapsed, inadmissible)
    
    """
    name = "Items in Stage"
    states = []
    list_id = "items-in-stage"    
    types = ['motion',
            'question',
            'agendaitem',
            'tableddocument',
            'bill']



    def getData(self):
        """
        return the data of the query
        """      
        data_list = []
        results = self.query.all()
       
        for result in results:            
            data ={}
            data['qid']= ( 'i-' + str(result.parliamentary_item_id) )
            if type(result) == domain.AgendaItem:
                g = u' ' + result.group.type + u' ' + result.group.short_name
            else:
                g = u''                                         
            data['subject'] = result.short_name
            data['title'] = result.short_name      
            data['result_item_class'] = 'workflow-state-' + result.status       
            data['url'] = '/business/%ss/obj-%i' %(result.type, 
                            result.parliamentary_item_id)
            data['status'] = get_wf_state(result)
            data['owner'] = "%s %s" %(result.owner.first_name, result.owner.last_name)
            data['type'] =  result.type.capitalize()
            data_list.append(data)            
        return data_list

    def update(self):
        """
        refresh the query
        """
        session = Session()
        try:
            user_id = self._parent.user_id    
        except:
            user_id = None     
        qfilter = sql.and_( domain.ParliamentaryItem.owner_id == user_id,
                domain.ParliamentaryItem.status.in_(self.states),
                domain.ParliamentaryItem.type.in_(self.types )
                            )        
        self.query = session.query(domain.ParliamentaryItem).filter(
                qfilter).order_by(
            domain.ParliamentaryItem.parliamentary_item_id.desc())  

class AllItemsInStageViewlet( ItemInStageViewlet ): 

    def update(self):
        """
        refresh the query
        """
        session = Session()    
        qfilter = sql.and_(
                domain.ParliamentaryItem.status.in_(self.states),
                domain.ParliamentaryItem.type.in_(self.types )
                    )        
        self.query = session.query(domain.ParliamentaryItem).filter(qfilter).order_by(
            domain.ParliamentaryItem.parliamentary_item_id.desc()) 
            


class MPItemDraftViewlet( ItemInStageViewlet ): 
    name = "Draft Items"
    states = [motion_wf_state[u"draft"].id,
        question_wf_state[u"draft"].id,
        agendaitem_wf_state[u"draft"].id,
        tableddocument_wf_state[u"draft"].id,
        bill_wf_state[u"draft"].id,
        ]
    list_id = "items-draft"    


class MPItemActionRequiredViewlet( ItemInStageViewlet ): 
    """
    Display all questions and motions that require action
    (e.g. draft, clarification required)
    """  
    name = "Action Required"
    states = [motion_wf_state[u"clarify_mp"].id,
        question_wf_state[u"clarify_mp"].id,
        agendaitem_wf_state[u"clarify_mp"].id,
        tableddocument_wf_state[u"clarify_mp"].id,
        ]
    list_id = "items-action-required"     


    

class MPItemInProgressViewlet(ItemInStageViewlet):
    """
    going through the workflow in clerks/speakers office
    """
    name = "Items in Progress"
    states = [
        question_wf_state[u"submitted"].id,
        question_wf_state[u"received"].id,
        question_wf_state[u"admissible"].id,
        question_wf_state[u"clarify_clerk"].id,     
        question_wf_state[u"complete"].id,  
        motion_wf_state[u"submitted"].id,
        motion_wf_state[u"received"].id,
        motion_wf_state[u"complete"].id,
        motion_wf_state[u"clarify_clerk"].id,
        motion_wf_state[u"admissible"].id,
        question_wf_state[u"scheduled"].id,
        question_wf_state[u"postponed"].id,
        question_wf_state[u"response_pending"].id,        
        question_wf_state[u"deferred"].id,
        question_wf_state[u"responded"].id,
        motion_wf_state[u"deferred"].id,
        motion_wf_state[u"postponed"].id,
        motion_wf_state[u"scheduled"].id,
        agendaitem_wf_state[u"submitted"].id,
        agendaitem_wf_state[u"received"].id,
        agendaitem_wf_state[u"complete"].id,
        agendaitem_wf_state[u"clarify_clerk"].id,
        agendaitem_wf_state[u"admissible"].id,
        agendaitem_wf_state[u"deferred"].id,
        agendaitem_wf_state[u"postponed"].id,
        agendaitem_wf_state[u"scheduled"].id,    
        tableddocument_wf_state[u"submitted"].id,
        tableddocument_wf_state[u"received"].id,
        tableddocument_wf_state[u"complete"].id,
        tableddocument_wf_state[u"clarify_clerk"].id,
        tableddocument_wf_state[u"admissible"].id,
        tableddocument_wf_state[u"deferred"].id,
        tableddocument_wf_state[u"postponed"].id,
        tableddocument_wf_state[u"scheduled"].id,    
        bill_wf_state[u"submitted"].id , 
        bill_wf_state[u"first_reading_postponed"].id ,
        bill_wf_state[u"second_reading"].id , 
        bill_wf_state[u"second_reading_postponed"].id , 
        bill_wf_state[u"whole_house_postponed"].id ,
        bill_wf_state[u"whole_house"].id ,
        bill_wf_state[u"report_reading_postponed"].id ,                                                                                
        bill_wf_state[u"report_reading"].id , 
        bill_wf_state[u"third_reading"].id,
        bill_wf_state[u"third_reading_postponed"].id                                
        ]
    list_id = "items-in-progress"     


class MPItemArchiveViewlet(ItemInStageViewlet):
    name = "Archived Items"
    states = [
        question_wf_state[u"answered"].id,
        question_wf_state[u"debated"].id,
        motion_wf_state[u"debated"].id,
        agendaitem_wf_state[u"debated"].id,
        tableddocument_wf_state[u"debated"].id,  
        question_wf_state[u"elapsed"].id,
        question_wf_state[u"withdrawn"].id,
        question_wf_state[u"inadmissible"].id, 
        motion_wf_state[u"withdrawn"].id,
        motion_wf_state[u"elapsed"].id,
        motion_wf_state[u"inadmissible"].id,          
        agendaitem_wf_state[u"withdrawn"].id,
        agendaitem_wf_state[u"elapsed"].id,
        agendaitem_wf_state[u"inadmissible"].id,  
        tableddocument_wf_state[u"withdrawn"].id,
        tableddocument_wf_state[u"elapsed"].id,
        tableddocument_wf_state[u"inadmissible"].id,          
        bill_wf_state[u"approved"].id , 
        bill_wf_state[u"rejected"].id ,          
        ]
    list_id = "items-archived"     

class MPItemSuccessEndViewlet(ItemInStageViewlet):
    """ items in end status that were discussed/answered ..."""
    name = "Items succesfully Tabled"
    states = [
        question_wf_state[u"answered"].id,
        question_wf_state[u"debated"].id,
        motion_wf_state[u"debated"].id,
        question_wf_state[u"elapsed"].id,
        question_wf_state[u"withdrawn"].id,
        question_wf_state[u"inadmissible"].id,        
        motion_wf_state[u"withdrawn"].id,
        motion_wf_state[u"elapsed"].id,
        motion_wf_state[u"inadmissible"].id        
        ]
    list_id = "items-sucess"     

class MPItemFailedEndViewlet(ItemInStageViewlet):
    """ Items in end status that did not recieve an answer """
    name = "Items that failed to be tabled"
    states = [
        question_wf_state[u"elapsed"].id,
        question_wf_state[u"withdrawn"].id,
        question_wf_state[u"inadmissible"].id,        
        motion_wf_state[u"withdrawn"].id,
        motion_wf_state[u"elapsed"].id,
        motion_wf_state[u"inadmissible"].id
        ]
    list_id = "items-failed"     


class ClerkItemActionRequiredViewlet( AllItemsInStageViewlet ): 
    types = ['motion',
            'question',
            'agendaitem',
            'tableddocument']

    name = "Action Required"
    states = [
        question_wf_state[u"submitted"].id,
        question_wf_state[u"received"].id,
        question_wf_state[u"clarify_clerk"].id,  
        question_wf_state[u"responded"].id,        
        motion_wf_state[u"submitted"].id,
        motion_wf_state[u"received"].id,
        motion_wf_state[u"clarify_clerk"].id,    
        agendaitem_wf_state[u"submitted"].id,
        agendaitem_wf_state[u"received"].id,
        agendaitem_wf_state[u"clarify_clerk"].id,    
        tableddocument_wf_state[u"submitted"].id,
        tableddocument_wf_state[u"received"].id,
        tableddocument_wf_state[u"clarify_clerk"].id,        
    ]
    list_id = "items-action-required"

class ClerkReviewedItemViewlet( AllItemsInStageViewlet ): 
    name = "Reviewed Items"
    states = [
        question_wf_state[u"complete"].id,  
        motion_wf_state[u"complete"].id,
        agendaitem_wf_state[u"complete"].id,
        tableddocument_wf_state[u"complete"].id, 
        question_wf_state[u"admissible"].id,  
        motion_wf_state[u"admissible"].id,
        agendaitem_wf_state[u"admissible"].id,
        tableddocument_wf_state[u"admissible"].id,  
        
        question_wf_state[u"scheduled"].id,
        question_wf_state[u"postponed"].id,
        question_wf_state[u"response_pending"].id,        
        question_wf_state[u"deferred"].id,
        question_wf_state[u"responded"].id,
        motion_wf_state[u"deferred"].id,
        motion_wf_state[u"postponed"].id,
        motion_wf_state[u"scheduled"].id,
        agendaitem_wf_state[u"deferred"].id,
        agendaitem_wf_state[u"postponed"].id,
        agendaitem_wf_state[u"scheduled"].id,    
        tableddocument_wf_state[u"deferred"].id,
        tableddocument_wf_state[u"postponed"].id,
        tableddocument_wf_state[u"scheduled"].id,
            
        bill_wf_state[u"submitted"].id , 
        bill_wf_state[u"first_reading_postponed"].id ,
        bill_wf_state[u"second_reading"].id , 
        bill_wf_state[u"second_reading_postponed"].id , 
        bill_wf_state[u"whole_house_postponed"].id ,
        bill_wf_state[u"whole_house"].id ,
        bill_wf_state[u"report_reading_postponed"].id ,                                                                                
        bill_wf_state[u"report_reading"].id , 
        bill_wf_state[u"third_reading"].id,
        bill_wf_state[u"third_reading_postponed"].id                            
    ]
    
class ItemsCompleteViewlet( AllItemsInStageViewlet ): 
    name = "Action Required"
    states = [
        question_wf_state[u"complete"].id,  
        motion_wf_state[u"complete"].id,
        agendaitem_wf_state[u"complete"].id,
        tableddocument_wf_state[u"complete"].id,                                     
    ]
    list_id = "items-action-required"

class ItemsApprovedViewlet( AllItemsInStageViewlet ): 
    name = "Approved Items"
    states = [   
        question_wf_state[u"admissible"].id,  
        motion_wf_state[u"admissible"].id,
        agendaitem_wf_state[u"admissible"].id,
        tableddocument_wf_state[u"admissible"].id,                                   
        
    ]
    list_id = "items-approved"

class MinistryItemsViewlet(viewlet.ViewletBase):
    render = ViewPageTemplateFile ('templates/ministry_ws_viewlet.pt')

    states = [
        question_wf_state[u"admissible"].id,  
        question_wf_state[u"scheduled"].id,                                          
        question_wf_state[u"response_pending"].id,          
    ]

    def _getItems(self, ministry):
        data_list = []   
        session = Session()
        query = session.query(domain.Question).filter(
            sql.and_(
                domain.Question.ministry_id == ministry.group_id,
                domain.Question.status.in_(self.states)))                    
        results = query.all()
        
        for result in results:            
            data ={}
            data['qid']= ( 'q_' + str(result.question_id) )  
            if result.question_number:                       
                data['subject'] = u'Q ' + str(result.question_number) + u' ' + result.short_name + ' (' + result.status + ')'
            else:
                data['subject'] = result.short_name + ' (' + result.status + ')'
            data['title'] = result.short_name + ' (' + result.status + ')'
            data['result_item_class'] = 'workflow-state-' + result.status 
            #http://localhost:8081/archive/browse/parliaments/obj-9/governments/obj-4/ministries/obj-121/questions/obj-4004            
            data['url'] = '/archive/browse/parliaments/obj-%i/governments/obj-%i/ministries/obj-%i/questions/obj-%i' %(
                self._parent.context.parliament_id, self._parent.government_id, 
                ministry.group_id, result.question_id)                
            
            data_list.append(data)            
        return data_list        
    
    def getData(self):
        """
        return the data of the query
        """    
        data_list = []       
        results = self.query.all()
        
        for result in results:            
            data ={}
            data['subject'] = result.short_name 
            data['url'] = '/archive/browse/parliaments/obj-%i/governments/obj-%i/ministries/obj-%i/' %(
                self._parent.context.parliament_id, self._parent.government_id, result.group_id)
            data['items'] = self._getItems(result)                
            data_list.append(data)         
            data['status'] = get_wf_state(result)
            data['owner'] = "%s %s" %(result.owner.first_name, result.owner.last_name)
            data['type'] =  result.type.capitalize()
            data_list.append(data)                 
        return data_list
    
    
    def update(self):
        """
        refresh the query
        """
        session = Session()   
        try:
            ministry_ids = self._parent.ministry_ids
        except:
            ministry_ids = []                        
        qfilter = domain.Ministry.group_id.in_(ministry_ids)        
        ministries = session.query(domain.Ministry).filter(qfilter).order_by(
            domain.Ministry.start_date.desc())            
        self.query = ministries    
        
        
        
