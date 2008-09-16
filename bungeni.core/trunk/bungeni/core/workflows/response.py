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
    draft = _(u"draft response") # a draft response of a Ministry
    submitted = _(u"response submitted") # response submitted to clerks office for review
    complete = _(u"response complete") # response reviewed by clerks office
    
def create_response_workflow( ):
    transitions = []
    add = transitions.append
    
    add( workflow.Transition(
        transition_id = 'create',
        title='Create',
        trigger = iworkflow.AUTOMATIC,
        source = None,
 #       action = utils.setResponseDefaults,        
        destination = states.draft,
        #permission = "bungeni.response.Create",
        ) )

    add( workflow.Transition(
        transition_id = 'submit',
        title=_(u'Submit Response'),
        source = states.draft,
        trigger = iworkflow.MANUAL,        
        destination = states.submitted,
        permission = 'bungeni.response.Submit',
        ) )    
        
    add( workflow.Transition(
        transition_id = 'complete',
        title=_(u'Complete Response'),
        source = states.submitted,
        trigger = iworkflow.MANUAL,        
        destination = states.complete,
        permission = 'bungeni.response.Complete',
        ) )            
    
    return transitions
    
workflow_transition_event_map = {    
    (states.draft, states.submitted): interfaces.IResponseSubmittedEvent,
    (states.submitted, states.complete): interfaces.IResponseCompletedEvent,
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

class ResponseWorkflow( workflow.Workflow ):

    def __init__( self ):
        super( ResponseWorkflow, self).__init__( create_response_workflow() )

ResponseWorkflowAdapter = workflow.AdaptedWorkflow( ResponseWorkflow() )

if __name__ == '__main__':
    wf = ResponseWorkflow()
    print wf.dot()

                
