from ore.workflow import interfaces as iworkflow
from ore.workflow import workflow

from bungeni.core.i18n import _

class states:
    draft = _(u"draft")
    submitted = _(u"submitted")
    received = _(u"received")

def create_question_workflow( ):
    transitions = []
    add = transitions.append
    
    add( workflow.Transition(
        transition_id = 'create',
        title='Create',
        trigger = iworkflow.AUTOMATIC,
        source = None,
        destination = states.draft
        ) )

    add( workflow.Transition(
        transition_id = 'submit-to-clerk',
        title=_(u'Submit to Clerk'),
        source = states.draft,
        destination = states.submitted
        ) )    

    add( workflow.Transition(
        transition_id = 'received-by-clerk',
        title=_(u'Receive'),
        source = states.submitted,
        destination = states.received
        ) )    

    return transitions

class QuestionWorkflow( workflow.Workflow ):

    def __init__( self ):
        super( QuestionWorkflow, self).__init__( create_question_workflow() )

QuestionWorkflowAdapter = workflow.AdaptedWorkflow( QuestionWorkflow() )

if __name__ == '__main__':
    wf = QuestionWorkflow()
    print wf.toDot()


    
