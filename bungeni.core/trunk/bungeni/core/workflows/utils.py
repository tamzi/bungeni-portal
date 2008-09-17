from zope.security.proxy import removeSecurityProxy
from zope import component


from ore.workflow.interfaces import IWorkflowInfo
import ore.workflow.workflow
import bungeni.core.workflows.question
import bungeni.core.interfaces
import bungeni.core.domain as domain

import dbutils

def createVersion(info, context):
    """Create a new version of an object and return it."""

    instance = removeSecurityProxy(context)
    versions =  bungeni.core.interfaces.IVersioned(instance)
    versions.create('New version created upon workflow transition.')
    
def setQuestionDefaults(info, context):
    """get the default values for a question.
    current parliament, ... """ 
    instance = removeSecurityProxy(context)
    dbutils.setQuestionParliamentId(instance)
           

def submitResponse( info, context ):
    """
    A Response to a question is submitted to the clerks office,
    the questions status is set to responded
    """
    ## this stuff is only to make the tests work
    component.provideAdapter( bungeni.core.workflows.WorkflowState,
                             (bungeni.core.interfaces.IBungeniContent,))

    component.provideAdapter( bungeni.core.workflows.question.QuestionWorkflowAdapter,
                            (domain.Question,))
    component.provideAdapter(ore.workflow.workflow.WorkflowInfo,(domain.Question,))
    ### end of test setup
    instance = removeSecurityProxy(context)
    question = dbutils.getQuestion(instance.question_id)
    IWorkflowInfo(question).fireTransition('respond-writing')

def publishResponse( info, context ):
    """
    The Response was reviewed by the clerks office, the questions
    status is set to answered
    """
    # make the tests work
    component.provideAdapter( bungeni.core.workflows.WorkflowState,
                             (bungeni.core.interfaces.IBungeniContent,))

    component.provideAdapter( bungeni.core.workflows.question.QuestionWorkflowAdapter,
                            (domain.Question,))
    component.provideAdapter(ore.workflow.workflow.WorkflowInfo,(domain.Question,))
    # end test setup
    instance = removeSecurityProxy(context)
    question = dbutils.getQuestion(instance.question_id)
    IWorkflowInfo(question).fireTransition('answer')
    
