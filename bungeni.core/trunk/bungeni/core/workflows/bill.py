"""
need workflow viewlet for current transition, and current state?
"""

from zope import interface, component, event

from ore.workflow import interfaces as iworkflow
from ore.workflow import workflow

#import interfaces
#import utils

from bungeni.core.i18n import _

class states:

    ministry_draft = "ministry_draft"
    member_draft = "member_draft"
    
    submitted = "submitted"
    first_reading = "first_reading"
    first_committee = "first_committee"
    
    second_pending = "second_pending"
    second_reading = "second_reading"
    second_committee = "second_committee"

    house_pending = "house_pending"
    whole_house ="whole_house"

    # is there a third pending state for a bill
    third_pending = "third_pending"
    third_reading = "third_reading"

    approved = "approved"
    rejected = "rejected"
    

def create_bill_workflow( ):

    transitions = []

    add = transitions.append

    add( workflow.Transition(
        transition_id = 'member-submit',
        title=_(u"Submit"),
        source = states.member_draft,
        destination = states.submitted,
        permission = "bungeni.bill.MemberSubmit"
        ) )

    add( workflow.Transition(
        transition_id = 'minister-submit',
        title=_(u"Submit"),
        source = states.ministry_draft,
        destination = states.submitted,
        permission = "bungeni.bill.MinisterSubmit",
        ) )

    add( workflow.Transition(
        transition_id = 'schedule-first',
        title=_(u"Schedule First Reading"),
        source = states.submitted,
        destination = states.first_reading,
        permission = "bungeni.bill.Schedule",
        ) )

    add( workflow.Transition(
        transition_id = 'select-first-committee',
        title=_(u"Send to Committee"),
        source = states.first_reading,
        destination = states.first_committee,
        permission = "bungeni.bill.SelectCommittee",
        ) )

    add( workflow.Transition(
        transition_id = 'schedule-second',
        title=_(u"Schedule Second Reading"),
        source = states.first_reading,
        destination = states.second_reading,
        permission = "bungeni.bill.Schedule",
        ) )

    add( workflow.Transition(
        transition_id = 'select-second-committee',
        title=_(u"Send to Committee"),
        source = states.second_reading,
        destination = states.second_committee,
        permission = "bungeni.bill.SelectCommittee",
        ) )

    add( workflow.Transition(
        transition_id = 'schedule-whole-house',
        title=_(u"Schedule Whole House Committee"),
        source = states.second_reading,
        destination = states.whole_house,
        permission = "bungeni.bill.Schedule",
        ) )

    add( workflow.Transition(
        transition_id = 'recommitted',
        title=_(u"Recommit Bill"),
        source = states.second_reading,
        destination = states.whole_house,
        permission = "bungeni.bill.Recommit",
        ) )

    add( workflow.Transition(
        transition_id = 'schedule-third-reading',
        title=_(u"Schedule Third Reading"),
        source = states.whole_house,
        destination = states.third_reading,
        permission = "bungeni.bill.Schedule",
        ) )

    add( workflow.Transition(
        transition_id = 'reject',
        title=_(u"Rejected"),
        source = states.third_reading,
        destination = states.rejected,
        permission = "bungeni.bill.ChangeStatus",
        ) )

    add( workflow.Transition(
        transition_id = 'approve',
        title=_(u"Approved"),
        source = states.third_reading,
        destination = states.approved,
        permission = "bungeni.bill.ChangeStatus",
        ) )    
    
    return transitions

workflow_transition_event_map = {
#    (states.submitted, states.received): interfaces.IQuestionReceivedEvent,
#    (states.draft, states.submitted): interfaces.IQuestionSubmittedEvent,
    }

@component.adapter(iworkflow.IWorkflowTransitionEvent)
def workflowTransitionEventDispatcher( event ):
    source = event.source
    destination = event.destination

    iface = workflow_transition_event_map.get((source, destination))
    if iface is None:
        return
    
    transition_event = ObjectEvent(event.object)
    interface.alsoProvides(transition_event, iface)
    event.notify(transition_event)
 
class BillWorkflow( workflow.Workflow ):

    def __init__( self ):
        super( BillWorkflow, self ).__init__( create_bill_workflow() )

BillWorkflowAdapter = workflow.AdaptedWorkflow( BillWorkflow() )

if __name__ == '__main__':
    wf = BillWorkflow()
    print wf.toDot()
    
         
        
