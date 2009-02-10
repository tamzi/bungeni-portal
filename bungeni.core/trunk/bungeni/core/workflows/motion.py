# encoding: utf-8

import os

from zope import interface
from zope import component
from zope.event import notify
from zope.component.interfaces import ObjectEvent

import zope.securitypolicy.interfaces

from ore.workflow import interfaces as iworkflow
from ore.workflow import workflow

import bungeni.core.workflows.interfaces as interfaces


from bungeni.core.i18n import _

from bungeni.core.workflows.wfstates import motionstates as states
from bungeni.core.workflow import load

path = os.path.split(os.path.abspath( __file__ ))[0] +  os.path.sep      
try:
    wf = load(path + 'motion.xml') 
except:
    wf = load('motion.xml') 


workflow_transition_event_map = {}
for t in wf._id_transitions.values():
    if t.event:
        workflow_transition_event_map[(t.source, t.destination)] = t.event

MotionWorkflowAdapter = workflow.AdaptedWorkflow( wf )

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
    wf = load('motion.xml') 
    print wf.dot()
    
