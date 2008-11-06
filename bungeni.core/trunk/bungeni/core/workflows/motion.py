# encoding: utf-8
from zope import interface
from zope import component
from zope.event import notify
from zope.component.interfaces import ObjectEvent

from ore.workflow import interfaces as iworkflow
from ore.workflow import workflow

import bungeni.core.workflows.interfaces as interfaces
import bungeni.core.workflows.utils as utils

from bungeni.core.i18n import _

class states:
    draft = _(u"draft motion") # a draft motion of a MP
    private = _("private motion") # private draft of a MP
    submitted = _(u"Motion submitted") # submitted from MP to clerks office
    received = _(u"Motion received by clerks office") # recieved by clerks office
    complete = _(u"Motion complete") # reviewed by clers office sent to speakers office
    admissible = _(u"Motion admissible") # reviewed by speakers office available for scheduling
    inadmissible = _(u"Motion inadmissible") # rejected by speakers office
    clarify_mp = _(u"Motion needs clarification by MP") # clerks office needs clarification by MP
    clarify_clerk = _("Motion needs clarification by Clerks Office") # speakers office needs clarification by clerks office
    scheduled =_(u"Motion scheduled") # is scheduled for debate at a sitting
    deferred = _(u"Motion deferred") # admissable motion that cannot be debated 
    postponed = _(u"Motion postponed") # motion was scheduled for but not debated at the sitting
    elapsed = _(u"Motion elapsed") # defered or postponed motion that were not debated
    debated = _(u"Motion debated") # a motion was debated 
    withdrawn = _(u"Motion withdrawn") # the owner of the motion can withdraw the motion

def postpone(info,context):
    utils.setMotionHistory(info,context)



def create_motion_workflow( ):
    transitions = []
    add = transitions.append
    
    add( workflow.Transition(
        transition_id = 'create',
        title='Create',
        trigger = iworkflow.AUTOMATIC,
        source = None,       
        destination = states.draft,
        #permission = "bungeni.motion.Create",
        ) )

    add( workflow.Transition(
        transition_id = 'make-private',
        title=_(u'Make private'),
        source = states.draft,
        trigger = iworkflow.MANUAL,        
        destination = states.private,
        permission = 'bungeni.motion.Submit',
        ) )    

    add( workflow.Transition(
        transition_id = 're-draft',
        title=_(u'Re draft'),
        source = states.private,
        trigger = iworkflow.MANUAL,        
        destination = states.draft,
        permission = 'bungeni.motion.Submit',
        ) )    


    add( workflow.Transition(
        transition_id = 'submit-to-clerk',
        title=_(u'Submit to Clerk'),
        source = states.draft,
        trigger = iworkflow.MANUAL,        
        action = utils.createVersion,
        destination = states.submitted,
        permission = 'bungeni.motion.Submit',
        ) )    

    add( workflow.Transition(
        transition_id = 'received-by-clerk',
        title=_(u'Receive'),
        source = states.submitted,
        trigger = iworkflow.MANUAL,                
        destination = states.received,
        permission = 'bungeni.motion.Recieve',        
        ) )    

    #If a motion is flagged by the Clerk /' Speakers office as 
    #"requiring editing by the MP" (e.g. missing data etc.) the system sends 
    #a notification to the MP to access the motion and review it according 
    #to Speaker/Clerk's  office remarks. 
    #A new version of the motion will be created, once the motion is modified and saved.

    add( workflow.Transition(
        transition_id = 'require-edit-by-mp',
        title=_(u'Needs Clarification by MP'),
        source = states.received,
        trigger = iworkflow.MANUAL,                
        destination = states.clarify_mp,
        permission = 'bungeni.motion.clerk.Review',        
        ) )   
    # the clerks office can reject a motion directly

    #add( workflow.Transition(
    #    transition_id = 'clerk-reject',
    #    title=_(u'Reject'),
    #    source = states.received,
    #    trigger = iworkflow.MANUAL,                
    #    destination = states.inadmissible,
    #    permission = 'bungeni.motion.clerk.Review',        
    #    ) ) 


    
    #After the Clerk's Office is through with the Notices reviews and there are satisfied 
    #that the motions have all the formal requirements – the motion is marked as “complete” 
    #and is made available / forwarded to the Speaker's Office for reviewing and to make it 
    #“admissible”. At the same time the motion is also forwarded to the ministry. 
    #While the ministry can preview the motion the ministry cannot respond until 
    #the state of the motion has been set to “admissible” by the Speaker's office 
    #(for details about motions being set to “admissible” see Approval of motions )

    add( workflow.Transition(
        transition_id = 'complete',
        title=_(u'Complete'),
        source = states.received,
        trigger = iworkflow.MANUAL,                
        destination = states.complete,
        permission = 'bungeni.motion.clerk.Review',        
        ) ) 

    #the Speaker's office may decide that a proposed motion is “admissible”, “inadmissible” 
    #or “requires amendment”.
    
    #An inadmissible motion is rejected and the Member who proposed the motion 
    #will be notified accordingly via their workspace and optionally by email.
    #motion that require amendments may be modified and re-submitted
    #motions marked as “admissible” are then made available for Scheduling     
    
    add( workflow.Transition(
        transition_id = 'approve',
        title=_(u'Approve'),
        source = states.complete,
        trigger = iworkflow.MANUAL,                
        destination = states.admissible,
        permission = 'bungeni.motion.speaker.Review',        
        ) )     
        
    add( workflow.Transition(
        transition_id = 'reject',
        title=_(u'Reject'),
        source = states.complete,
        trigger = iworkflow.MANUAL,                
        destination = states.inadmissible,
        permission = 'bungeni.motion.speaker.Review',        
        ) )    
        
    add( workflow.Transition(
        transition_id = 'require-amendment',
        title=_(u'Needs Clarification'),
        source = states.complete,
        trigger = iworkflow.MANUAL,                
        action = utils.createVersion,        
        destination = states.clarify_clerk,
        permission = 'bungeni.motion.speaker.Review',        
        ) )                    
    
    # a motion that requires clarification/amendmends
    # can be resubmitted by the clerks office
    
    add( workflow.Transition(
        transition_id = 'complete-clarify',
        title=_(u'Complete'),
        source = states.clarify_clerk,
        trigger = iworkflow.MANUAL,                
        destination = states.complete,
        permission = 'bungeni.motion.clerk.Review',        
        ) )     
    
    # or send to the mp for clarification     
    add( workflow.Transition(
        transition_id = 'mp-clarify',
        title=_(u'Needs Clarification by MP'),
        source = states.clarify_clerk,
        trigger = iworkflow.MANUAL,                
        destination = states.clarify_mp,
        permission = 'bungeni.motion.clerk.Review',        
        ) )         
    
    
    # after a motion is amended it can be resubmitted to the clerks office
    
    add( workflow.Transition(
        transition_id = 'resubmit-clerk',
        title=_(u'Resubmit to clerk'),
        source = states.clarify_mp,
        trigger = iworkflow.MANUAL,                
        action = utils.createVersion,
        destination = states.submitted,
        permission = 'bungeni.motion.Submit',       
        ) )          
    
    #Among the “admissible” motions the Speaker or the Clerk's office will 
    #select motions for scheduling for a specific sitting
    #motions when “admissible” are made available for “scheduling”



    add( workflow.Transition(
        transition_id = 'schedule',
        title=_(u'Schedule'),
        #trigger = iworkflow. , #triggered by scheduling ?        
        source = states.admissible,
        trigger = iworkflow.MANUAL,                
        destination = states.scheduled,
        permission = 'bungeni.motion.Schedule',        
        ) )         
    
              
    
    
    #all admissible motions awaiting an oral response etc. and flag them for “scheduling” for a later day 
    #or otherwise drop them from the pending ones. Dropping a motion sets its status to “Deferred” 

    add( workflow.Transition(
        transition_id = 'defer',
        title=_(u'Defer'),
        source = states.admissible,
        trigger = iworkflow.MANUAL,                
        destination = states.deferred,
        permission = 'bungeni.motion.Schedule',        
        ) )  

    add( workflow.Transition(
        transition_id = 'elapse-defered',
        title=_(u'Elapse'),
        source = states.deferred,
        trigger = iworkflow.MANUAL,                
        destination = states.elapsed,
        permission = 'bungeni.motion.Schedule',        
        ) )  


    # A defered motion can be rescheduled later

    add( workflow.Transition(
        transition_id = 'schedule-deferred',
        title=_(u'Schedule'),
        source = states.deferred,
        #trigger = iworkflow. , #triggered by scheduling ?                
        trigger = iworkflow.MANUAL,                
        destination = states.scheduled,
        permission = 'bungeni.motion.Schedule',        
        ) )  



    # in a sitting the motion is either answered or it gets postopned
    
    add( workflow.Transition(
        transition_id = 'postpone',
        title=_(u'Postpone'),
        source = states.scheduled,
        trigger = iworkflow.MANUAL, 
        action = postpone,               
        destination = states.postponed,
        permission = 'bungeni.motion.Schedule',        
        ) )      
        
    add( workflow.Transition(
        transition_id = 'debate',
        title=_(u'Debate'),
        source = states.scheduled,
        trigger = iworkflow.MANUAL,                
        destination = states.debated,
        permission = 'bungeni.motion.Debate',        
        ) )      
        
    # postponed motions are rescheduled
    
    add( workflow.Transition(
        transition_id = 'schedule-postponed',
        title=_(u'Schedule'),
        source = states.postponed,
        trigger = iworkflow.MANUAL,                
        destination = states.scheduled,        
        permission = 'bungeni.motion.Schedule',        
        ) )      

    # postponed motion can elapse

    add( workflow.Transition(
        transition_id = 'elapse-postponed',
        title=_(u'Elapse'),
        source = states.postponed,
        trigger = iworkflow.MANUAL,                
        destination = states.elapsed,        
        permission = 'bungeni.motion.Schedule',        
        ) )    
        
        

    #the MP can withdraw his motion at (almost) any stage
    #i.e the stages where it can still be presented to the 
    #house

#    add( workflow.Transition(
#        transition_id = 'withdraw-draft',
#        title=_(u'Withdraw'),
#        source = states.draft,
#        trigger = iworkflow.MANUAL,                
#        destination = states.withdrawn,
#        permission = 'bungeni.motion.Withdraw',        
#        ) )  

    add( workflow.Transition(
        transition_id = 'withdraw-submitted',
        title=_(u'Withdraw'),
        source = states.submitted,
        trigger = iworkflow.MANUAL,                
        destination = states.withdrawn,
        permission = 'bungeni.motion.Withdraw',        
        ) )   

    add( workflow.Transition(
        transition_id = 'withdraw-received',
        title=_(u'Withdraw'),
        source = states.received,
        trigger = iworkflow.MANUAL,                
        destination = states.withdrawn,
        permission = 'bungeni.motion.Withdraw',        
        ) )   
    add( workflow.Transition(
        transition_id = 'withdraw-complete',
        title=_(u'Withdraw'),
        source = states.complete,
        trigger = iworkflow.MANUAL,                
        destination = states.withdrawn,
        permission = 'bungeni.motion.Withdraw',        
        ) )   
    add( workflow.Transition(
        transition_id = 'withdraw-admissible',
        title=_(u'Withdraw'),
        source = states.admissible,
        trigger = iworkflow.MANUAL,                
        destination = states.withdrawn,
        permission = 'bungeni.motion.Withdraw',        
        ) )   
    add( workflow.Transition(
        transition_id = 'withdraw-amend',
        title=_(u'Withdraw'),
        source = states.clarify_mp,
        trigger = iworkflow.MANUAL,                
        destination = states.withdrawn,
        permission = 'bungeni.motion.Withdraw',        
        ) )                           
    add( workflow.Transition(
        transition_id = 'withdraw-scheduled',
        title=_(u'Withdraw'),
        source = states.scheduled,
        trigger = iworkflow.MANUAL,                
        destination = states.withdrawn,
        permission = 'bungeni.motion.Withdraw',        
        ) )   
    add( workflow.Transition(
        transition_id = 'withdraw-deferred',
        title=_(u'Withdraw'),
        source = states.deferred,
        trigger = iworkflow.MANUAL,                
        destination = states.withdrawn,
        permission = 'bungeni.motion.Withdraw',        
        ) )   
    add( workflow.Transition(
        transition_id = 'withdraw-postponed',
        title=_(u'Withdraw'),
        source = states.postponed,
        trigger = iworkflow.MANUAL,                
        destination = states.withdrawn,
        permission = 'bungeni.motion.Withdraw',        
        ) )   



    return transitions

workflow_transition_event_map = {
    (states.submitted, states.received): interfaces.IMotionReceivedEvent,
    (states.draft, states.submitted): interfaces.IMotionSubmittedEvent,
    (states.complete, states.inadmissible): interfaces.IMotionRejectedEvent,
    (states.received, states.clarify_mp): interfaces.IMotionClarifyEvent,
    (states.clarify_clerk, states.clarify_mp): interfaces.IMotionClarifyEvent,
    (states.admissible, states.deferred): interfaces.IMotionDeferredEvent,
    (states.admissible, states.scheduled): interfaces.IMotionScheduledEvent,
    (states.postponed, states.scheduled): interfaces.IMotionScheduledEvent,    
    (states.scheduled, states.postponed): interfaces.IMotionPostponedEvent,
    (states.scheduled, states.debated): interfaces.IMotionDebatedEvent,
    }


class MotionWorkflow( workflow.Workflow ):

    def __init__( self ):
        super( MotionWorkflow, self).__init__( create_motion_workflow() )

MotionWorkflowAdapter = workflow.AdaptedWorkflow( MotionWorkflow() )

@component.adapter(iworkflow.IWorkflowTransitionEvent)
def workflowTransitionEventDispatcher(event):
    source = event.source
    destination = event.destination

    iface = workflow_transition_event_map.get((source, destination))
    if iface is not None:
        transition_event = ObjectEvent(event.object)
        interface.alsoProvides(transition_event, iface)
        notify(transition_event)


if __name__ == '__main__':
    wf = MotionWorkflow()
    print wf.dot()
    
