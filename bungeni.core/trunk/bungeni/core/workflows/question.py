# encoding: utf-8
from zope import interface
from zope import component
from zope.event import notify
from zope.component.interfaces import ObjectEvent
import zope.securitypolicy.interfaces
from zope.security.proxy import removeSecurityProxy


#from sqlalchemy.orm import mapper
#import bungeni.core.schema as schema
import bungeni.core
#import bungeni.core.domain as domain



from ore.workflow import interfaces as iworkflow
from ore.workflow import workflow



import bungeni.core.workflows.interfaces as interfaces
import bungeni.core.workflows.utils as utils

from bungeni.core.i18n import _

class states:
    draft = _(u"draft question") # a draft question of a MP
    private = _("private question") # private draft of a MP
    submitted = _(u"Question submitted to clerk") # submitted from MP to clerks office
    received = _(u"Question received by clerk") # recieved by clerks office
    complete = _(u"Question complete") # reviewed by clers office sent to speakers office
    admissible = _(u"admissible Question") # reviewed by speakers office available for scheduling or to
                                  # to be send to ministry for written response
    inadmissible = _(u"inadmissible Question") # rejected by speakers office
    clarify_mp = _(u"Question needs MP clarification") # clerks office needs clarification by MP
    clarify_clerk = _("Question needs Clerks clarification") # speakers office needs clarification by clerks office
    scheduled =_(u"Question scheduled") # is scheduled for debate at a sitting
    response_pending = _(u"Question pending response") # ministry has to write a response
    deferred = _(u"Question deferred") # admissable question that cannot be debated 
    postponed = _(u"Question postponed") # question was scheduled for but not debated at the sitting
    elapsed = _(u"Question elapsed") # defered or postponed question that were not answered
                            # or questions that required a written answer by a ministry which were not answered
    responded = _(u"Question responded") # a question was debated or a written answer was given by a ministry
    answered = _(u"Question answered") # the written answer was reviewed by the clerks office
                              # or debate reference input by clerks office
    withdrawn = _(u"Question withdrawn") # the owner of the question can withdraw the question
    
#############
# the actions that set the correct
# roles and permissions to the workflowed object
#

# you may get all transition_ids by calling
# wf =  bungeni.core.workflows.question.QuestionWorkflow()
# wf.__dict__['_id_transitions'].keys()      
#
#'defer', 'withdraw-admissible', 'send-ministry', 'respond-writing', 'postponed-ministry', 
#'withdraw-submitted', 'withdraw-complete', 'require-edit-by-mp', 'withdraw-scheduled', 
#'withdraw-postponed', 'defer-ministry', 'elapse-pending', 'create', 'require-amendment', 
#'reject', 'make-private', 'received-by-clerk', 'postpone', 'withdraw-amend', 'complete', 
#'schedule', 'complete-clarify', 'respond-sitting', 'answer', 'elapse-postponed', 
#'submit-to-clerk', 'elapse-defered', 'withdraw-deferred', 'schedule-postponed', 
#'schedule-deferred', 're-draft', 'mp-clarify', 'withdraw-received', 'approve', 'resubmit-clerk'


def denyAllWrites(question):
    """
    remove all rights to change the question from all involved roles
    """
    rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )
    rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.Owner' )
    rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.Clerk' )
    rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.Speaker' )
    rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.MP' )
    rpm.denyPermissionToRole( 'bungeni.question.delete', u'bungeni.Owner' )
    rpm.denyPermissionToRole( 'bungeni.question.delete', u'bungeni.Clerk' )
    rpm.denyPermissionToRole( 'bungeni.question.delete', u'bungeni.Speaker' )
    rpm.denyPermissionToRole( 'bungeni.question.delete', u'bungeni.MP' )    

def create(info,context):
    """
    create a question -> state.draft, grant all rights to owner
    """
    utils.setQuestionDefaults(info, context)
    user_id = utils.getUserId()
    if not user_id:
        user_id ='-'
    zope.securitypolicy.interfaces.IPrincipalRoleMap( context ).assignRoleToPrincipal( u'bungeni.Owner', user_id) 
        
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
    question = removeSecurityProxy(context)
    rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )
    rpm.grantPermissionToRole( 'bungeni.question.view', u'bungeni.Clerk' )
    rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.Owner' )
    rpm.denyPermissionToRole( 'bungeni.question.delete', u'bungeni.Owner' )
     
    
def recievedByClerk( info, context ):
    """
    the question is recieved by the clerks office, 
    the clerk can edit the question
    """
    utils.createVersion(info, context)   
    question = removeSecurityProxy(context)     
    zope.securitypolicy.interfaces.IRolePermissionMap( question ).grantPermissionToRole( 'bungeni.question.edit', u'bungeni.Clerk' )

def withdraw( info, context ):
    """
    a question can be withdrawn by the owner, it is than visible to
    and cannot be edited by anyone
    """
    question = removeSecurityProxy(context)
    denyAllWrites(question)

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
    question = removeSecurityProxy(context)
    denyAllWrites(question)
    
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
    question = removeSecurityProxy(context)
    denyAllWrites(question)
    rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )
    rpm.grantPermissionToRole( 'bungeni.response.add', u'bungeni.Minister' )
    
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
    question = removeSecurityProxy(context)
    rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )
    rpm.grantPermissionToRole( 'bungeni.question.edit', u'bungeni.Owner' )
    rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.Clerk' )   
    

    
def requireAmendment(info,context):
    """
    A question is send back from the speakers office 
    the clerks office for clarification
    """
    utils.createVersion(info,context)
    question = removeSecurityProxy(context)
    rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )
    rpm.grantPermissionToRole( 'bungeni.question.edit', u'bungeni.Clerk' )
    rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.Speaker' )   
    
def reject(info,context):
    """
    A question that is not admissible, 
    Nobody is allowed to edit it
    """
    question = removeSecurityProxy(context)
    denyAllWrites(question)
    
def postpone(info,context):
    """
    A question that was scheduled but could not be debated,
    it is available for rescheduling.
    """
    utils.setQuestionScheduleHistory(info,context)
    pass

def complete(info,context):
    """
    A question is marked as complete by the clerks office, 
    it is available to the speakers office for review
    """
    utils.createVersion(info,context)
    question = removeSecurityProxy(context)
    rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )
    rpm.grantPermissionToRole( 'bungeni.question.view', u'bungeni.Speaker' )
    rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.Clerk' )     
    
    
    
def schedule(info,context):
    """
    the question gets scheduled no one can edit the question
    """
    question = removeSecurityProxy(context)
    rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )
    rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.Speaker' )
    

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
    question = removeSecurityProxy(context)
    rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )
    rpm.grantPermissionToRole( 'bungeni.question.view', u'bungeni.Speaker' )
    rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.Clerk' ) 
    
def respondSitting(info,context):
    """
    A question was debated, the question cannot be edited, 
    the clerks office can add a response
    """
    question = removeSecurityProxy(context)
    rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )    
    rpm.grantPermissionToRole( 'bungeni.response.add', u'bungeni.Clerk' )
    
def answer(info,context):
    """
    the response was reviewed by the clerks office, 
    the question is visible 
    """
    pass

def mpClarify(info,context):
    """
    send from the clerks office to the mp for clarification 
    the MP can edit it the clerk cannot
    """
    utils.createVersion(info,context)
    question = removeSecurityProxy(context)
    rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )
    rpm.grantPermissionToRole( 'bungeni.question.edit', u'bungeni.Owner' )
    rpm.denyPermissionToRole( 'bungeni.question.edit', u'bungeni.Clerk' ) 
        
    
def approve(info,context):
    """
    the question is admissible and can be send to ministry,
    or is available for scheduling in a sitting
    """
    question = removeSecurityProxy(context)
    rpm = zope.securitypolicy.interfaces.IRolePermissionMap( question )    
    rpm.grantPermissionToRole( 'bungeni.question.edit', u'bungeni.Speaker' )
    utils.setApprovalDate(info,context)
   







def create_question_workflow( ):
    transitions = []
    add = transitions.append
    
    add( workflow.Transition(
        transition_id = 'create',
        title='Create',
        trigger = iworkflow.AUTOMATIC,
        source = None,        
        action = create,               
        destination = states.draft,
        #permission = "bungeni.question.Create",
        ) )

    add( workflow.Transition(
        transition_id = 'make-private',
        title=_(u'Make private'),
        source = states.draft,
        trigger = iworkflow.MANUAL,  
        action = makePrivate,      
        destination = states.private,
        permission = 'bungeni.question.Submit',
        ) )    

    add( workflow.Transition(
        transition_id = 're-draft',
        title=_(u'Re draft'),
        source = states.private,
        trigger = iworkflow.MANUAL,        
        action=reDraft,
        destination = states.draft,
        permission = 'bungeni.question.Submit',
        ) )    


    add( workflow.Transition(
        transition_id = 'submit-to-clerk',
        title=_(u'Submit to Clerk'),
        source = states.draft,
        trigger = iworkflow.MANUAL,        
        action = submitToClerk,
        destination = states.submitted,
        permission = 'bungeni.question.Submit',
        ) )    

    add( workflow.Transition(
        transition_id = 'received-by-clerk',
        title=_(u'Receive'),
        source = states.submitted,
        trigger = iworkflow.MANUAL, 
        action = recievedByClerk,                       
        destination = states.received,
        permission = 'bungeni.question.Recieve',        
        ) )    

    #If a question is flagged by the Clerk /' Speakers office as 
    #"requiring editing by the MP" (e.g. missing data etc.) the system sends 
    #a notification to the MP to access the question and review it according 
    #to Speaker/Clerk's  office remarks. 
    #A new version of the question will be created, once the question is modified and saved.

    add( workflow.Transition(
        transition_id = 'require-edit-by-mp',
        title=_(u'Needs Clarification by MP'),
        source = states.received,
        trigger = iworkflow.MANUAL,   
        action = requireEditByMp,             
        destination = states.clarify_mp,
        permission = 'bungeni.question.clerk.Review',        
        ) )   
    # the clerks office can reject a question directly

    #add( workflow.Transition(
    #    transition_id = 'clerk-reject',
    #    title=_(u'Reject'),
    #    source = states.received,
    #    trigger = iworkflow.MANUAL,                
    #    destination = states.inadmissible,
    #    permission = 'bungeni.question.clerk.Review',        
    #    ) ) 


    
    #After the Clerk's Office is through with the Notices reviews and there are satisfied 
    #that the Questions have all the formal requirements – the question is marked as “complete” 
    #and is made available / forwarded to the Speaker's Office for reviewing and to make it 
    #“admissible”. At the same time the question is also forwarded to the ministry. 
    #While the ministry can preview the question the ministry cannot respond until 
    #the state of the question has been set to “admissible” by the Speaker's office 
    #(for details about questions being set to “admissible” see Approval of Questions )

    add( workflow.Transition(
        transition_id = 'complete',
        title=_(u'Complete'),
        source = states.received,
        trigger = iworkflow.MANUAL,
        action = complete, 
        destination = states.complete,
        permission = 'bungeni.question.clerk.Review',        
        ) ) 

    #the Speaker's office may decide that a proposed Question is “admissible”, “inadmissible” 
    #or “requires amendment”.
    
    #An inadmissible Question is rejected and the Member who proposed the Question 
    #will be notified accordingly via their workspace and optionally by email.
    #Question that require amendments may be modified and re-submitted
    #Questions marked as “admissible” are then made available for Scheduling     
    
    add( workflow.Transition(
        transition_id = 'approve',
        title=_(u'Approve'),
        source = states.complete,
        trigger = iworkflow.MANUAL, 
        action = approve,                                     
        destination = states.admissible,
        permission = 'bungeni.question.speaker.Review',        
        ) )     
        
    add( workflow.Transition(
        transition_id = 'reject',
        title=_(u'Reject'),
        source = states.complete,
        trigger = iworkflow.MANUAL,     
        action=reject,           
        destination = states.inadmissible,
        permission = 'bungeni.question.speaker.Review',        
        ) )    
        
    add( workflow.Transition(
        transition_id = 'require-amendment',
        title=_(u'Needs Clarification'),
        source = states.complete,
        trigger = iworkflow.MANUAL,                
        action = requireAmendment,        
        destination = states.clarify_clerk,
        permission = 'bungeni.question.speaker.Review',        
        ) )                    
    
    # a question that requires clarification/amendmends
    # can be resubmitted by the clerks office
    
    add( workflow.Transition(
        transition_id = 'complete-clarify',
        title=_(u'Complete'),
        source = states.clarify_clerk,
        trigger = iworkflow.MANUAL,   
        action = completeClarify,             
        destination = states.complete,
        permission = 'bungeni.question.clerk.Review',        
        ) )     
    
    # or send to the mp for clarification     
    add( workflow.Transition(
        transition_id = 'mp-clarify',
        title=_(u'Needs Clarification by MP'),
        source = states.clarify_clerk,
        trigger = iworkflow.MANUAL,
        action = mpClarify,                
        destination = states.clarify_mp,
        permission = 'bungeni.question.clerk.Review',        
        ) )         
    
    
    # after a question is amended it can be resubmitted to the clerks office
    
    add( workflow.Transition(
        transition_id = 'resubmit-clerk',
        title=_(u'Resubmit to clerk'),
        source = states.clarify_mp,
        trigger = iworkflow.MANUAL,                
        action = submitToClerk,
        destination = states.submitted,
        permission = 'bungeni.question.Submit',       
        ) )          
    
    #Among the “admissible” questions the Speaker or the Clerk's office will 
    #select questions for scheduling for a specific sitting
    #Questions when “admissible” are made available for “scheduling”
    #Questions with the “require a Written response” flag do not appear as questions available for scheduling.




    add( workflow.Transition(
        transition_id = 'schedule',
        title=_(u'Schedule'),
        #trigger = iworkflow. , #triggered by scheduling ?        
        source = states.admissible,
        trigger = iworkflow.MANUAL,                
        action = schedule,
        destination = states.scheduled,
        permission = 'bungeni.question.Schedule',        
        ) )         
    
    # questions which are flagged as “requiring written response” are never scheduled,
    # but are answered directly by the ministry 

    add( workflow.Transition(
        transition_id = 'send-ministry',
        title=_(u'Send to ministry'),
        source = states.admissible,
        trigger = iworkflow.MANUAL,   
        condition = utils.getQuestionMinistry,    
        action = sendToMinistry,               
        destination = states.response_pending,
        permission = 'bungeni.question.Schedule',        
        ) )  


    add( workflow.Transition(
        transition_id = 'respond-writing',
        title=_(u'Respond'),
        source = states.response_pending,
        trigger = iworkflow.SYSTEM,   
        action = respondWriting,             
        destination = states.responded,
        permission = 'bungeni.question.write_answer',        
        ) )         
    
    add( workflow.Transition(
        transition_id = 'elapse-pending',
        title=_(u'Elapse'),
        source = states.response_pending,
        trigger = iworkflow.MANUAL,                
        action = elapse,
        destination = states.elapsed,
        permission = 'bungeni.question.write_answer',        
        ) )            
    
    
    #all admissible questions awaiting an oral response etc. and flag them for “scheduling” for a later day 
    #or otherwise drop them from the pending ones. Dropping a question sets its status to “Deferred” 

    add( workflow.Transition(
        transition_id = 'defer',
        title=_(u'Defer'),
        source = states.admissible,
        trigger = iworkflow.MANUAL,                
        action = defer,
        destination = states.deferred,
        permission = 'bungeni.question.Schedule',        
        ) )  

    add( workflow.Transition(
        transition_id = 'elapse-defered',
        title=_(u'Elapse'),
        source = states.deferred,
        trigger = iworkflow.MANUAL,                
        action = elapse,
        destination = states.elapsed,
        permission = 'bungeni.question.Schedule',        
        ) )  



    # a deferred question may be send to a ministry for a written response
    
    add( workflow.Transition(
        transition_id = 'defer-ministry',
        title=_(u'Send to ministry'),
        source = states.deferred,
        trigger = iworkflow.MANUAL,        
        action = sendToMinistry,         
        condition = utils.getQuestionMinistry,                   
        destination = states.response_pending,
        permission = 'bungeni.question.Schedule',        
        ) )  

    # A defered question can be rescheduled later

    add( workflow.Transition(
        transition_id = 'schedule-deferred',
        title=_(u'Schedule'),
        source = states.deferred,
        #trigger = iworkflow. , #triggered by scheduling ?                
        trigger = iworkflow.MANUAL,                
        action = schedule,
        destination = states.scheduled,
        permission = 'bungeni.question.Schedule',        
        ) )  



    # in a sitting the question is either answered or it gets postopned
    
    add( workflow.Transition(
        transition_id = 'postpone',
        title=_(u'Postpone'),
        source = states.scheduled,
        trigger = iworkflow.MANUAL, 
        action = postpone,
        destination = states.postponed,
        permission = 'bungeni.question.Schedule',        
        ) )      
        
    add( workflow.Transition(
        transition_id = 'respond-sitting',
        title=_(u'Respond'),
        source = states.scheduled,
        trigger = iworkflow.MANUAL,                
        action = respondSitting,
        destination = states.responded,
        permission = 'bungeni.question.Respond',        
        ) )      
        
    # postponed questions are rescheduled
    
    add( workflow.Transition(
        transition_id = 'schedule-postponed',
        title=_(u'Schedule'),
        source = states.postponed,
        trigger = iworkflow.MANUAL,            
        action = schedule,    
        destination = states.scheduled,        
        permission = 'bungeni.question.Schedule',        
        ) )      

    # postponed question can elapse

    add( workflow.Transition(
        transition_id = 'elapse-postponed',
        title=_(u'Elapse'),
        source = states.postponed,
        trigger = iworkflow.MANUAL,  
        action = elapse,              
        destination = states.elapsed,        
        permission = 'bungeni.question.Schedule',        
        ) )    
        
    # postponed question can be send to a ministry for a written response

    add( workflow.Transition(
        transition_id = 'postponed-ministry',
        title=_(u'Send to Ministry'),
        source = states.postponed,
        action = sendToMinistry,
        condition = utils.getQuestionMinistry ,                           
        trigger = iworkflow.MANUAL,                
        destination = states.response_pending,        
        permission = 'bungeni.question.Schedule',        
        ) )    
        

    #The response is sent to the Clerk's office, before being sent to the MP.
    #XXX come up with something better than answered
    add( workflow.Transition(
        transition_id = 'answer',
        title=_(u'Answer'),
        source = states.responded,
        trigger = iworkflow.SYSTEM,                
        action=answer,
        destination = states.answered,
        permission = 'bungeni.question.Answer',        
        ) )       

    #the MP can withdraw his question at (almost) any stage
    #i.e the stages where it can still be presented to the 
    # ministry/house

#    add( workflow.Transition(
#        transition_id = 'withdraw-draft',
#        title=_(u'Withdraw'),
#        source = states.draft,
#        trigger = iworkflow.MANUAL,                
#        destination = states.withdrawn,
#        permission = 'bungeni.question.Withdraw',        
#        ) )  

    add( workflow.Transition(
        transition_id = 'withdraw-submitted',
        title=_(u'Withdraw'),
        source = states.submitted,
        trigger = iworkflow.MANUAL,         
        action = withdraw,       
        destination = states.withdrawn,
        permission = 'bungeni.question.Withdraw',        
        ) )   

    add( workflow.Transition(
        transition_id = 'withdraw-received',
        title=_(u'Withdraw'),
        source = states.received,
        trigger = iworkflow.MANUAL,                
        action = withdraw,
        destination = states.withdrawn,
        permission = 'bungeni.question.Withdraw',        
        ) )   
    add( workflow.Transition(
        transition_id = 'withdraw-complete',
        title=_(u'Withdraw'),
        source = states.complete,
        trigger = iworkflow.MANUAL,                
        action = withdraw,
        destination = states.withdrawn,
        permission = 'bungeni.question.Withdraw',        
        ) )   
    add( workflow.Transition(
        transition_id = 'withdraw-admissible',
        title=_(u'Withdraw'),
        source = states.admissible,
        trigger = iworkflow.MANUAL,                
        action = withdraw,
        destination = states.withdrawn,
        permission = 'bungeni.question.Withdraw',        
        ) )   
    add( workflow.Transition(
        transition_id = 'withdraw-amend',
        title=_(u'Withdraw'),
        source = states.clarify_mp,
        trigger = iworkflow.MANUAL,                
        action = withdraw,
        destination = states.withdrawn,
        permission = 'bungeni.question.Withdraw',        
        ) )                           
    add( workflow.Transition(
        transition_id = 'withdraw-scheduled',
        title=_(u'Withdraw'),
        source = states.scheduled,
        trigger = iworkflow.MANUAL,                
        action = withdraw,
        destination = states.withdrawn,
        permission = 'bungeni.question.Withdraw',        
        ) )   
    add( workflow.Transition(
        transition_id = 'withdraw-deferred',
        title=_(u'Withdraw'),
        source = states.deferred,
        trigger = iworkflow.MANUAL,                
        destination = states.withdrawn,
        action = withdraw,
        permission = 'bungeni.question.Withdraw',        
        ) )   
    add( workflow.Transition(
        transition_id = 'withdraw-postponed',
        title=_(u'Withdraw'),
        source = states.postponed,
        trigger = iworkflow.MANUAL,                
        action = withdraw,
        destination = states.withdrawn,
        permission = 'bungeni.question.Withdraw',        
        ) )   
                
    return transitions

workflow_transition_event_map = {
    (states.submitted, states.received): interfaces.IQuestionReceivedEvent,
    (states.draft, states.submitted): interfaces.IQuestionSubmittedEvent,
    (states.complete, states.inadmissible): interfaces.IQuestionRejectedEvent,
    (states.received, states.clarify_mp): interfaces.IQuestionClarifyEvent,
    (states.admissible, states.deferred): interfaces.IQuestionDeferredEvent,
    (states.admissible, states.scheduled): interfaces.IQuestionScheduledEvent,
    (states.scheduled, states.postponed): interfaces.IQuestionPostponedEvent,
    (states.deferred, states.response_pending): interfaces.IQuestionSentToMinistryEvent,
    (states.admissible, states.response_pending): interfaces.IQuestionSentToMinistryEvent,    
    (states.postponed, states.response_pending): interfaces.IQuestionSentToMinistryEvent, 
    (states.postponed, states.scheduled): interfaces.IQuestionScheduledEvent,       
    (states.responded, states.answered): interfaces.IQuestionAnsweredEvent,
    }

@component.adapter(iworkflow.IWorkflowTransitionEvent)
def workflowTransitionEventDispatcher(event):
    source = event.source
    destination = event.destination

    iface = workflow_transition_event_map.get((source, destination))
    if iface is not None:
        transition_event = ObjectEvent(event.object)
        interface.alsoProvides(transition_event, iface)
        notify(transition_event)

class QuestionWorkflow( workflow.Workflow ):

    def __init__( self ):
        super( QuestionWorkflow, self).__init__( create_question_workflow() )

QuestionWorkflowAdapter = workflow.AdaptedWorkflow( QuestionWorkflow() )

if __name__ == '__main__':
    wf = QuestionWorkflow()
    print wf.dot()


    
