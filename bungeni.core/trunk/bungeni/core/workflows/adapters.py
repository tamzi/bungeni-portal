import os
import bill
import question
import motion
import response
import events
import xmlimport


from ore.workflow import workflow

path = os.path.split(os.path.abspath(__file__))[0]

def load_workflow(module):
    name = module.__name__.rsplit('.')[-1]
    wf = xmlimport.load("%s/%s.xml" % (path, name))
    events.register_workflow_transitions(wf)
    module.wf = wf
    module.states = wf.states
    return wf

QuestionWorkflowAdapter = workflow.AdaptedWorkflow(load_workflow(question))
MotionWorkflowAdapter = workflow.AdaptedWorkflow(load_workflow(motion))
BillWorkflowAdapter = workflow.AdaptedWorkflow(load_workflow(bill))
ResponseWorkflowAdapter = workflow.AdaptedWorkflow(load_workflow(response))

