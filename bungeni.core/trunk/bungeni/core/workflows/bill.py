"""
need workflow viewlet for current transition, and current state?
"""
import os

from zope import component
from zope.security.proxy import removeSecurityProxy
import zope.securitypolicy.interfaces

from ore.workflow import workflow
from ore.workflow import interfaces as iworkflow

from bungeni.core.i18n import _
import bungeni.core.workflows.utils as utils
#from bungeni.core.workflows.wfstates import billstates as states
from bungeni.core.workflow import load
    
path = os.path.split(os.path.abspath( __file__ ))[0] +  os.path.sep      
try:
    wf = load(path + 'bill.xml') 
except:
    wf = load('bill.xml') 
    
    
workflow_transition_event_map = {}
for t in wf._id_transitions.values():
    if t.event:
        workflow_transition_event_map[(t.source, t.destination)] = t.event
        
@component.adapter(iworkflow.IWorkflowTransitionEvent)
def workflowTransitionEventDispatcher(event):
    source = event.source
    destination = event.destination

    iface = workflow_transition_event_map.get((source, destination))
    if iface is not None:
        transition_event = ObjectEvent(event.object)
        interface.alsoProvides(transition_event, iface)
        notify(transition_event)

BillWorkflowAdapter = workflow.AdaptedWorkflow( wf )
states = wf.states

if __name__ == '__main__':
    #wf = BillWorkflow()
    #transitions = create_bill_workflow()
    wf = load('bill.xml')    
    print wf.dot()
    
         
        
