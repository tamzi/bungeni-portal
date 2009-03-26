import os
import events
import xmlimport

import bill
import question
import motion
import response
import version

from bungeni.models import domain
from bungeni.models.interfaces import IVersion

from ore.workflow import workflow

path = os.path.split(os.path.abspath(__file__))[0]

def load_workflow(module, kls):
    name = module.__name__.rsplit('.')[-1]
    wf = xmlimport.load("%s/%s.xml" % (path, name))
    events.register_workflow_transitions(wf, kls)
    module.wf = wf
    module.states = wf.states
    return wf

QuestionWorkflowAdapter = workflow.AdaptedWorkflow(
    load_workflow(question, domain.Question))
MotionWorkflowAdapter = workflow.AdaptedWorkflow(
    load_workflow(motion, domain.Motion))
BillWorkflowAdapter = workflow.AdaptedWorkflow(
    load_workflow(bill, domain.Bill))
ResponseWorkflowAdapter = workflow.AdaptedWorkflow(
    load_workflow(response, domain.Response))
VersionWorkflowAdapter = workflow.AdaptedWorkflow(
    load_workflow(version, IVersion))

