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
    requires_amendment =_(u"requires_amendment")
    scheduled =_(u"scheduled")
    deferred = _(u"deferred")
    postponed =_(u"postponed")
    responded = _(u"responded")
    answered =_(u"answered")
    

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
        action = utils.createVersion,
        destination = states.submitted,
        permission = 'bungeni.question.Submit',
        ) )    

    add( workflow.Transition(
        transition_id = 'received-by-clerk',
        title=_(u'Receive'),
        source = states.submitted,
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
        title=_(u'Requires editing by MP'),
        source = states.received,
        destination = states.draft,
        permission = 'bungeni.question.clerk.review',        
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
        destination = states.complete,
        permission = 'bungeni.question.clerk.review',        
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
        destination = states.admissible,
        permission = 'bungeni.question.speaker.review',        
        ) )     
        
    add( workflow.Transition(
        transition_id = 'reject',
        title=_(u'Reject'),
        source = states.complete,
        destination = states.inadmissible,
        permission = 'bungeni.question.speaker.review',        
        ) )    
        
    add( workflow.Transition(
        transition_id = 'require-amendment',
        title=_(u'Requires Amendment'),
        source = states.complete,
        action = utils.createVersion,        
        destination = states.requires_amendment,
        permission = 'bungeni.question.speaker.review',        
        ) )                    
    
    # after a question is amended it can be resubmitted to the clerks office
    
    add( workflow.Transition(
        transition_id = 'resubmit-clerk',
        title=_(u'Resubmit to Clerk'),
        source = states.requires_amendment,
#        action = utils.createVersion,
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
        destination = states.scheduled,
        permission = 'bungeni.question.schedule',        
        ) )         
    
    # questions which are flagged as “requiring written response” are never scheduled,
    # but are answered directly by the ministry 

    add( workflow.Transition(
        transition_id = 'respond-writing',
        title=_(u'Respond'),
        source = states.admissible,
        destination = states.responded,
        permission = 'bungeni.question.schedule',        
        ) )         
    
    
    
    #all admissible questions awaiting an oral response etc. and flag them for “scheduling” for a later day 
    #or otherwise drop them from the pending ones. Dropping a question sets its status to “Deferred” 

    add( workflow.Transition(
        transition_id = 'defer',
        title=_(u'Defer'),
        source = states.admissible,
        destination = states.deferred,
        permission = 'bungeni.question.schedule',        
        ) )  

    # A defered question can be rescheduled later

    add( workflow.Transition(
        transition_id = 'schedule-deferred',
        title=_(u'Schedule'),
        source = states.deferred,
        #trigger = iworkflow. , #triggered by scheduling ?                
        destination = states.scheduled,
        permission = 'bungeni.question.schedule',        
        ) )  



    # in a sitting the question is either answered or it gets postopned
    
    add( workflow.Transition(
        transition_id = 'postpone',
        title=_(u'Postpone'),
        source = states.scheduled,
        destination = states.postponed,
        permission = 'bungeni.question.schedule',        
        ) )      
        
    add( workflow.Transition(
        transition_id = 'respond-sitting',
        title=_(u'Respond'),
        source = states.scheduled,
        destination = states.responded,
        permission = 'bungeni.question.respond',        
        ) )      
        
    # postponed questions are rescheduled
    
    add( workflow.Transition(
        transition_id = 'schedule-postponed',
        title=_(u'Postpone'),
        source = states.postponed,
        destination = states.scheduled,        
        permission = 'bungeni.question.schedule',        
        ) )      

    #The response is sent to the Clerk's office, before being sent to the MP.
    #XXX come up with something better than answered
    add( workflow.Transition(
        transition_id = 'answer',
        title=_(u'Answer'),
        source = states.responded,
        destination = states.answered,
        permission = 'bungeni.question.answer',        
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


    
