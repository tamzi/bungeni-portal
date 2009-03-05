# encoding: utf-8

from zope import interface
from zope import component
from zope.event import notify
from zope.component.interfaces import ObjectEvent
from ore.workflow import interfaces

# global workflow transition event map
workflow_transition_event_map = {}

def get_workflow_transitions(wf):
    return wf._id_transitions.values()
    
def register_workflow_transitions(wf):
    """Use this method to register workflow transitions, such that
    events will be fired after a transition."""
    
    for t in get_workflow_transitions(wf):
        if t.event:
            workflow_transition_event_map[
                (t.source, t.destination)] = t.event

@component.adapter(interfaces.IWorkflowTransitionEvent)
def workflowTransitionEventDispatcher(event):
    source = event.source
    destination = event.destination

    iface = workflow_transition_event_map.get((source, destination))
    if iface is not None:
        transition_event = ObjectEvent(event.object)
        interface.alsoProvides(transition_event, iface)
        notify(transition_event)

