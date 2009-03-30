
import datetime
from zope.security.proxy import removeSecurityProxy
from zope import component

from zope.security.management import getInteraction
from zope.publisher.interfaces import IRequest

from ore.workflow.interfaces import IWorkflowInfo, InvalidTransitionError
import ore.workflow.workflow

import bungeni.core.interfaces
import bungeni.models.interfaces
import bungeni.models.domain as domain
import bungeni.core.globalsettings as prefs

import dbutils

def getUserId( ):
    interaction = getInteraction()
    for participation in interaction.participations:
        if IRequest.providedBy(participation):
            return participation.principal.id


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
    dbutils.setQuestionMinistryId(instance)    

def setSubmissionDate(info, context):
    instance = removeSecurityProxy(context)
    instance.submission_date = datetime.date.today()    
    versions =  bungeni.core.interfaces.IVersioned(instance)
    versions.create('New version created upon submission to clerks office')
    
def setApprovalDate(info, context):
    instance = removeSecurityProxy(context)
    instance.approval_date = datetime.date.today()  
    versions =  bungeni.core.interfaces.IVersioned(instance)            
    versions.create('New Version created upon approval by speakers office')
    if type(instance) == domain.Question:
        dbutils.setQuestionSerialNumber(instance)
    elif type(instance) == domain.Motion:
        dbutils.setMotionSerialNumber(instance)                

def setMinistrySubmissionDate(info, context):
    instance = removeSecurityProxy(context)
    instance.ministry_submit_date = datetime.date.today()  

def setQuestionScheduleHistory(info, context):
    question_id = context.question_id
    dbutils.removeQuestionFromItemSchedule(question_id)
  

def getQuestionMinistry(info, context):
    ministry_id = context.ministry_id
    return ministry_id != None

def getQuestionSchedule(info, context):
    question_id = context.question_id
    return dbutils.isItemScheduled(question_id)

def getMotionSchedule(info, context):
    motion_id = context.motion_id
    return dbutils.isItemScheduled(motion_id)

def getQuestionSubmissionAllowed(info, context):    
    return prefs.getQuestionSubmissionAllowed()


def setBillSubmissionDate( info, context ):
    instance = removeSecurityProxy(context)
    instance.submission_date = datetime.date.today()

def setBillPublicationDate( info, context ):
    instance = removeSecurityProxy(context)
    instance.publication_date = datetime.date.today()

def submitResponse( info, context ):
    """A Response to a question is submitted to the clerks office,
    the questions status is set to responded
    """

    instance = removeSecurityProxy(context)
    question = dbutils.getQuestion(instance.response_id)
    if (question.status != u"responded"):
        IWorkflowInfo(question).fireTransitionToward(u"responded")
     

def publishResponse( info, context ):
    """The Response was reviewed by the clerks office, the questions
    status is set to answered
    """
    instance = removeSecurityProxy(context)
    question = dbutils.getQuestion(instance.response_id)
    IWorkflowInfo(question).fireTransition('answer')
    
def setMotionHistory( info, context ):
    motion_id = context.motion_id
    dbutils.removeMotionFromItemSchedule(motion_id)

def setParliamentId( info, context):
    instance = removeSecurityProxy(context)
    if not instance.parliament_id:
        parliamentId = prefs.getCurrentParliamentId()
        instance.parliament_id = parliamentId
    
def resonse_allow_submit(info, context):
    instance = removeSecurityProxy(context)
    question = dbutils.getQuestion(instance.response_id)
    if ((question.status == u"response_pending")
        or (question.status ==  u"scheduled")
        or (question.status == u"responded")):
        return True
    else:
        return False        

def response_allow_complete(info, context):
    instance = removeSecurityProxy(context)
    question = dbutils.getQuestion(instance.response_id)
    if (question.status == u"responded"):
        return True
    else:
        return False        
            
             
          
    
