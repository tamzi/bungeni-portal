# encoding: utf-8

import bungeni.core.workflows.utils as utils
import zope.securitypolicy.interfaces

def denyAllWrites(question):
    """
    remove all rights to change the question from all involved roles
    """
    pass
    #rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )
    #rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.Owner' )
    #rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.Clerk' )
    #rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.Speaker' )
    #rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.MP' )
    #rpm.denyPermissionToRole( 'bungeni.question.delete', u'bungeni.Owner' )
    #rpm.denyPermissionToRole( 'bungeni.question.delete', u'bungeni.Clerk' )
    #rpm.denyPermissionToRole( 'bungeni.question.delete', u'bungeni.Speaker' )
    #rpm.denyPermissionToRole( 'bungeni.question.delete', u'bungeni.MP' )    

def create(info,context):
    """
    create a question -> state.draft, grant all rights to owner
    deny right to add supplementary questions.
    """
    utils.setQuestionDefaults(info, context)
    user_id = utils.getUserId()
    if not user_id:
        user_id ='-'
    zope.securitypolicy.interfaces.IPrincipalRoleMap( context ).assignRoleToPrincipal( u'bungeni.Owner', user_id)     
    #rpm = zope.securitypolicy.interfaces.IRolePermissionMap( context )    
    #rpm.denyPermissionToRole( 'bungeni.question.add', u'bungeni.MP' )
        
def makePrivate(info,context):
    """
    a question that is not being asked
    """
    pass

def reDraft(info, context):
    """
    
    """
    pass


#def resubmitClerk(info,context):
#    submitToClerk(info,context)

def submitToClerk(info,context):      
    """
    a question submitted to the clerks office, the owner cannot edit it anymore
    the clerk has no edit rights until it is recieved
    """
    utils.setSubmissionDate(info, context)
    #question = removeSecurityProxy(context)
    #rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )
    #rpm.grantPermissionToRole( 'bungeni.question.view', u'bungeni.Clerk' )
    #rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.Owner' )
    #rpm.denyPermissionToRole( 'bungeni.question.delete', u'bungeni.Owner' )
     
    
def recievedByClerk( info, context ):
    """
    the question is recieved by the clerks office, 
    the clerk can edit the question
    """
    utils.createVersion(info, context)   
    #question = removeSecurityProxy(context)     
    #zope.securitypolicy.interfaces.IRolePermissionMap( question ).grantPermissionToRole( 'bungeni.question.edit', u'bungeni.Clerk' )

def withdraw( info, context ):
    """
    a question can be withdrawn by the owner, it is  visible to ...
    and cannot be edited by anyone
    """
    #if context.status == states.scheduled:        
    utils.setQuestionScheduleHistory(info,context)    
    #question = removeSecurityProxy(context)
    #denyAllWrites(question)

#def withdrawAdmissible(info,context):
#   withdraw( info, context )
#def withdrawSubmitted(info,context):
#    withdraw
#def withdrawComplete(info,context):
#   withdraw( info, context )
#def withdrawAmend(info,context):
#   withdraw( info, context )
#def withdrawDeferred(info,context):
#   withdraw( info, context )
#def withdrawReceived(info,context):
#    pass
#def withdrawScheduled(info,context):
#   withdraw( info, context )
#def withdrawPostponed(info,context):
#   withdraw( info, context )


def elapse(info,context):
    """
    A question that could not be answered or debated, 
    it is visible to ... and cannot be edited
    """
    #question = removeSecurityProxy(context)
    #denyAllWrites(question)
    pass
    
#def elapsePending(info,context):
#    elapse
#def elapsePostponed(info,context):
#    pass
#def elapseDefered(info,context):
#    elapse

def defer(info,context):
    """
    A question that cannot be debated it is available for scheduling
    but cannot be edited
    """
    pass
#def deferMinistry(info,context):
#    utils.setMinistrySubmissionDate(info, context)


def sendToMinistry(info,context):
    """
    A question sent to a ministry for a written answer, 
    it cannot be edited, the ministry can add a written response
    """
    utils.setMinistrySubmissionDate(info,context)
    #question = removeSecurityProxy(context)
    #denyAllWrites(question)
    #rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )
    #XXX this should be assigned to a specific ministry group
    #rpm.grantPermissionToRole( 'bungeni.response.add', u'bungeni.Minister' )
    #rpm.grantPermissionToRole( 'bungeni.response.view', u'bungeni.Minister' )
    
#def postponedMinistry(info,context):
#    pass    
    
def respondWriting(info,context):
    """
    A written response from a ministry
    """
    pass


def requireEditByMp(info,context):
    """
    A question is unclear and requires edits/amendments by the MP
    Only the MP is able to edit it, the clerks office looses edit rights
    """
    utils.createVersion(info,context)
    #question = removeSecurityProxy(context)
    #rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )
    #rpm.grantPermissionToRole( 'bungeni.question.edit', u'bungeni.Owner' )
    #rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.Clerk' )   
    

    
def requireAmendment(info,context):
    """
    A question is send back from the speakers office 
    the clerks office for clarification
    """
    utils.createVersion(info,context)
    #question = removeSecurityProxy(context)
    #rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )
    #rpm.grantPermissionToRole( 'bungeni.question.edit', u'bungeni.Clerk' )
    #rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.Speaker' )   
    
def reject(info,context):
    """
    A question that is not admissible, 
    Nobody is allowed to edit it
    """
    #question = removeSecurityProxy(context)
    #denyAllWrites(question)
    pass
    
def postpone(info,context):
    """
    A question that was scheduled but could not be debated,
    it is available for rescheduling.
    """
    utils.setQuestionScheduleHistory(info,context)
    #question = removeSecurityProxy(context)
    #rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )  
    #rpm.denyPermissionToRole( 'bungeni.response.add', u'bungeni.Clerk' )
    #rpm.denyPermissionToRole( 'bungeni.response.view', u'bungeni.Clerk' )        
    #pass

def complete(info,context):
    """
    A question is marked as complete by the clerks office, 
    it is available to the speakers office for review
    """
    utils.createVersion(info,context)
    #question = removeSecurityProxy(context)
    #rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )
    #rpm.grantPermissionToRole( 'bungeni.question.view', u'bungeni.Speaker' )
    #rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.Clerk' )     
    
    
    
def schedule(info,context):
    """
    the question gets scheduled no one can edit the question,
    a response may be added
    """
    pass
    #question = removeSecurityProxy(context)
    #rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )
    #rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.Speaker' )
    #rpm.grantPermissionToRole( 'bungeni.response.add', u'bungeni.Clerk' )
    #rpm.grantPermissionToRole( 'bungeni.response.view', u'bungeni.Clerk' )    

#def schedulePostponed(info,context):
#    schedule
#def scheduleDeferred(info,context):
#    schedule

def completeClarify(info,context):
    """
    a question that requires clarification/amendmends
    is  resubmitted by the clerks office to the speakers office
    """
    utils.createVersion(info,context)
    #question = removeSecurityProxy(context)
    #rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )
    #rpm.grantPermissionToRole( 'bungeni.question.view', u'bungeni.Speaker' )
    #rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.Clerk' ) 
    
def respondSitting(info,context):
    """
    A question was debated, the question cannot be edited, 
    the clerks office can add a response
    """
    pass
    #question = removeSecurityProxy(context)
    #rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )    
    #rpm.grantPermissionToRole( 'bungeni.response.add', u'bungeni.Clerk' )
    #rpm.grantPermissionToRole( 'bungeni.response.view', u'bungeni.Clerk' )
    
def answer(info,context):
    """
    the response was reviewed by the clerks office, 
    the question is visible, if the question was a written question
    supplementary question now can be asked. 
    """
    pass
    #question = removeSecurityProxy(context)
    #rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question ) 
    #rpm.grantPermissionToRole( 'bungeni.question.add', u'bungeni.MP' )
    #rpm.grantPermissionToRole( 'bungeni.question.view', u'bungeni.Everybody' )
    #rpm.grantPermissionToRole( 'bungeni.response.view',  u'bungeni.Everybody' )
    
def mpClarify(info,context):
    """
    send from the clerks office to the mp for clarification 
    the MP can edit it the clerk cannot
    """
    utils.createVersion(info,context)
    #question = removeSecurityProxy(context)
    #rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )
    #rpm.grantPermissionToRole( 'bungeni.question.edit', u'bungeni.Owner' )
    #rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.Clerk' ) 
        
    
def approve(info,context):
    """
    the question is admissible and can be send to ministry,
    or is available for scheduling in a sitting
    """
    #question = removeSecurityProxy(context)
    #rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )    
    #rpm.grantPermissionToRole( 'bungeni.question.edit', u'bungeni.Speaker' )
    #rpm.grantPermissionToRole( 'bungeni.question.view', u'zope.Everybody')
    utils.setApprovalDate(info,context)
   
