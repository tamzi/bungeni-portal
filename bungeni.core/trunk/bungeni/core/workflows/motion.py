import os

from ore.workflow import workflow
from bungeni.core.workflows import events
from bungeni.core.workflows.xmlimport import load

path = os.path.split(os.path.abspath( __file__ ))[0]
wf = load("%s/motion.xml" % path)

events.register_workflow_transitions(wf)
WorkflowAdapter = workflow.AdaptedWorkflow(wf)
states = wf.states
