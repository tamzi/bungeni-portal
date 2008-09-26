
import datetime
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
    #dbutils.setQuestionParliamentId(instance)

def setSubmissionDate(info, context):
    instance = removeSecurityProxy(context)
    instance.clerk_submission_date = datetime.date.today()    
    versions =  bungeni.core.interfaces.IVersioned(instance)
    versions.create('New version created upon submission to clerks office')
    
def setApprovalDate(info, context):
    instance = removeSecurityProxy(context)
    instance.approval_date = datetime.date.today()  
    versions =  bungeni.core.interfaces.IVersioned(instance)            
    versions.create('New Version, Question approved by speakers office')

def setQuestionScheduleHistory(info, context):
    question_id = context.question_id
    sitting_id = context.sitting_id
    dbutils.insertQuestionScheduleHistory(question_id, sitting_id) 
    instance = removeSecurityProxy(context)
    instance.sitting_id = None       


def submitResponse( info, context ):
    """
    A Response to a question is submitted to the clerks office,
    the questions status is set to responded
    """

    instance = removeSecurityProxy(context)
    question = dbutils.getQuestion(instance.response_id)
    IWorkflowInfo(question).fireTransition('respond-writing')

def publishResponse( info, context ):
    """
    The Response was reviewed by the clerks office, the questions
    status is set to answered
    """
    instance = removeSecurityProxy(context)
    question = dbutils.getQuestion(instance.response_id)
    IWorkflowInfo(question).fireTransition('answer')
    
