# encoding: utf-8
from zope import interface
from zope import component
from zope.event import notify
from zope.component.interfaces import ObjectEvent

from ore.workflow import interfaces as iworkflow
from ore.workflow import workflow

import interfaces
import utils

from bungeni.core.i18n import _

class states:
    draft = _(u"draft")
    submitted = _(u"submitted")
    received = _(u"received")
    complete = _(u"complete")
    admissible = _(u"admissible")
    inadmissible = _(u"inadmissible")
    requires_amend =_(u"requires_amend")
    scheduled =_(u"scheduled")
    deferred = _(u"deferred")
    postponed =_(u"postponed")
    responded = _(u"responded")
    answered =_(u"answered")
    withdrawn =_(u"withdrawn")
    

def create_question_workflow( ):
    transitions = []
    add = transitions.append
    
    add( workflow.Transition(
        transition_id = 'create',
        title='Create',
        trigger = iworkflow.AUTOMATIC,
        source = None,
        destination = states.draft,
        permission = "bungeni.question.Create",
        ) )

    add( workflow.Transition(
        transition_id = 'submit-to-clerk',
        title=_(u'Submit to Clerk'),
        source = states.draft,
        trigger = iworkflow.MANUAL,        
        action = utils.createVersion,
        destination = states.submitted,
        permission = 'bungeni.question.Submit',
        ) )    

    add( workflow.Transition(
        transition_id = 'received-by-clerk',
        title=_(u'Receive'),
        source = states.submitted,
        trigger = iworkflow.MANUAL,                
        destination = states.received,
        permission = 'bungeni.question.Recieve',        
        ) )    

    #If a question is flagged by the Clerk /' Speakers office as 
    #"requiring editing by the MP" (e.g. missing data etc.) the system sends 
    #a notification to the MP to access the question and review it according 
    #to Speaker/Clerk's  office remarks. 
    #A new version of the question will be created, once the question is modified and saved.

    add( workflow.Transition(
        transition_id = 'require-edit-by-mp',
        title=_(u'Needs Clarification by MP'),
        source = states.received,
        trigger = iworkflow.MANUAL,                
        destination = states.draft,
        permission = 'bungeni.question.clerk.Review',        
        ) )   
    # the clerks office can reject a question directly

    add( workflow.Transition(
        transition_id = 'clerk-reject',
        title=_(u'Reject'),
        source = states.received,
        trigger = iworkflow.MANUAL,                
        destination = states.inadmissible,
        permission = 'bungeni.question.clerk.Review',        
        ) ) 


    
    #After the Clerk's Office is through with the Notices reviews and there are satisfied 
    #that the Questions have all the formal requirements – the question is marked as “complete” 
    #and is made available / forwarded to the Speaker's Office for reviewing and to make it 
    #“admissible”. At the same time the question is also forwarded to the ministry. 
    #While the ministry can preview the question the ministry cannot respond until 
    #the state of the question has been set to “admissible” by the Speaker's office 
    #(for details about questions being set to “admissible” see Approval of Questions )

    add( workflow.Transition(
        transition_id = 'complete',
        title=_(u'Complete'),
        source = states.received,
        trigger = iworkflow.MANUAL,                
        destination = states.complete,
        permission = 'bungeni.question.clerk.Review',        
        ) ) 

    #the Speaker's office may decide that a proposed Question is “admissible”, “inadmissible” 
    #or “requires amendment”.
    
    #An inadmissible Question is rejected and the Member who proposed the Question 
    #will be notified accordingly via their workspace and optionally by email.
    #Question that require amendments may be modified and re-submitted
    #Questions marked as “admissible” are then made available for Scheduling     
    
    add( workflow.Transition(
        transition_id = 'approve',
        title=_(u'Approve'),
        source = states.complete,
        trigger = iworkflow.MANUAL,                
        destination = states.admissible,
        permission = 'bungeni.question.speaker.Review',        
        ) )     
        
    add( workflow.Transition(
        transition_id = 'reject',
        title=_(u'Reject'),
        source = states.complete,
        trigger = iworkflow.MANUAL,                
        destination = states.inadmissible,
        permission = 'bungeni.question.speaker.Review',        
        ) )    
        
    add( workflow.Transition(
        transition_id = 'require-amendment',
        title=_(u'Requires Amendment'),
        source = states.complete,
        trigger = iworkflow.MANUAL,                
        action = utils.createVersion,        
        destination = states.requires_amend,
        permission = 'bungeni.question.speaker.Review',        
        ) )                    
    
    # after a question is amended it can be resubmitted to the clerks office
    
    add( workflow.Transition(
        transition_id = 'resubmit-clerk',
        title=_(u'Resubmit to clerk'),
        source = states.requires_amend,
        trigger = iworkflow.MANUAL,                
        action = utils.createVersion,
        destination = states.submitted,
        permission = 'bungeni.question.Submit',       
        ) )          
    
    #Among the “admissible” questions the Speaker or the Clerk's office will 
    #select questions for scheduling for a specific sitting
    #Questions when “admissible” are made available for “scheduling”
    #Questions with the “require a Written response” flag do not appear as questions available for scheduling.




    add( workflow.Transition(
        transition_id = 'schedule',
        title=_(u'Schedule'),
        #trigger = iworkflow. , #triggered by scheduling ?        
        source = states.admissible,
        trigger = iworkflow.MANUAL,                
        destination = states.scheduled,
        permission = 'bungeni.question.Schedule',        
        ) )         
    
    # questions which are flagged as “requiring written response” are never scheduled,
    # but are answered directly by the ministry 

    add( workflow.Transition(
        transition_id = 'respond-writing',
        title=_(u'Respond'),
        source = states.admissible,
        trigger = iworkflow.MANUAL,                
        destination = states.responded,
        permission = 'bungeni.question.Schedule',        
        ) )         
    
    
    
    #all admissible questions awaiting an oral response etc. and flag them for “scheduling” for a later day 
    #or otherwise drop them from the pending ones. Dropping a question sets its status to “Deferred” 

    add( workflow.Transition(
        transition_id = 'defer',
        title=_(u'Defer'),
        source = states.admissible,
        trigger = iworkflow.MANUAL,                
        destination = states.deferred,
        permission = 'bungeni.question.Schedule',        
        ) )  

    # A defered question can be rescheduled later

    add( workflow.Transition(
        transition_id = 'schedule-deferred',
        title=_(u'Schedule'),
        source = states.deferred,
        #trigger = iworkflow. , #triggered by scheduling ?                
        trigger = iworkflow.MANUAL,                
        destination = states.scheduled,
        permission = 'bungeni.question.Schedule',        
        ) )  



    # in a sitting the question is either answered or it gets postopned
    
    add( workflow.Transition(
        transition_id = 'postpone',
        title=_(u'Postpone'),
        source = states.scheduled,
        trigger = iworkflow.MANUAL,                
        destination = states.postponed,
        permission = 'bungeni.question.Schedule',        
        ) )      
        
    add( workflow.Transition(
        transition_id = 'respond-sitting',
        title=_(u'Respond'),
        source = states.scheduled,
        trigger = iworkflow.MANUAL,                
        destination = states.responded,
        permission = 'bungeni.question.Respond',        
        ) )      
        
    # postponed questions are rescheduled
    
    add( workflow.Transition(
        transition_id = 'schedule-postponed',
        title=_(u'Postpone'),
        source = states.postponed,
        trigger = iworkflow.MANUAL,                
        destination = states.scheduled,        
        permission = 'bungeni.question.Schedule',        
        ) )      

    #The response is sent to the Clerk's office, before being sent to the MP.
    #XXX come up with something better than answered
    add( workflow.Transition(
        transition_id = 'answer',
        title=_(u'Answer'),
        source = states.responded,
        trigger = iworkflow.MANUAL,                
        destination = states.answered,
        permission = 'bungeni.question.Answer',        
        ) )       

    #the MP can withdraw his question at (almost) any stage
    #i.e the stages where it can still be presented to the 
    # ministry/house

    add( workflow.Transition(
        transition_id = 'withdraw-draft',
        title=_(u'Withdraw'),
        source = states.draft,
        trigger = iworkflow.MANUAL,                
        destination = states.withdrawn,
        permission = 'bungeni.question.Withdraw',        
        ) )  

    add( workflow.Transition(
        transition_id = 'withdraw-submitted',
        title=_(u'Withdraw'),
        source = states.submitted,
        trigger = iworkflow.MANUAL,                
        destination = states.withdrawn,
        permission = 'bungeni.question.Withdraw',        
        ) )   

    add( workflow.Transition(
        transition_id = 'withdraw-received',
        title=_(u'Withdraw'),
        source = states.received,
        trigger = iworkflow.MANUAL,                
        destination = states.withdrawn,
        permission = 'bungeni.question.Withdraw',        
        ) )   
    add( workflow.Transition(
        transition_id = 'withdraw-complete',
        title=_(u'Withdraw'),
        source = states.complete,
        trigger = iworkflow.MANUAL,                
        destination = states.withdrawn,
        permission = 'bungeni.question.Withdraw',        
        ) )   
    add( workflow.Transition(
        transition_id = 'withdraw-admissible',
        title=_(u'Withdraw'),
        source = states.admissible,
        trigger = iworkflow.MANUAL,                
        destination = states.withdrawn,
        permission = 'bungeni.question.Withdraw',        
        ) )   
    add( workflow.Transition(
        transition_id = 'withdraw-amend',
        title=_(u'Withdraw'),
        source = states.requires_amend,
        trigger = iworkflow.MANUAL,                
        destination = states.withdrawn,
        permission = 'bungeni.question.Withdraw',        
        ) )                           
    add( workflow.Transition(
        transition_id = 'withdraw-scheduled',
        title=_(u'Withdraw'),
        source = states.scheduled,
        trigger = iworkflow.MANUAL,                
        destination = states.withdrawn,
        permission = 'bungeni.question.Withdraw',        
        ) )   
    add( workflow.Transition(
        transition_id = 'withdraw-deferred',
        title=_(u'Withdraw'),
        source = states.deferred,
        trigger = iworkflow.MANUAL,                
        destination = states.withdrawn,
        permission = 'bungeni.question.Withdraw',        
        ) )   
    add( workflow.Transition(
        transition_id = 'withdraw-postponed',
        title=_(u'Withdraw'),
        source = states.postponed,
        trigger = iworkflow.MANUAL,                
        destination = states.withdrawn,
        permission = 'bungeni.question.Withdraw',        
        ) )   
                
    return transitions

workflow_transition_event_map = {
    (states.submitted, states.received): interfaces.IQuestionReceivedEvent,
    (states.draft, states.submitted): interfaces.IQuestionSubmittedEvent,
    }

@component.adapter(iworkflow.IWorkflowTransitionEvent)
def workflowTransitionEventDispatcher(event):
    source = event.source
    destination = event.destination

    iface = workflow_transition_event_map.get((source, destination))
    if iface is not None:
        transition_event = ObjectEvent(event.object)
        interface.alsoProvides(transition_event, iface)
        notify(transition_event)

class QuestionWorkflow( workflow.Workflow ):

    def __init__( self ):
        super( QuestionWorkflow, self).__init__( create_question_workflow() )

QuestionWorkflowAdapter = workflow.AdaptedWorkflow( QuestionWorkflow() )

if __name__ == '__main__':
    wf = QuestionWorkflow()
    print wf.toDot()


    
