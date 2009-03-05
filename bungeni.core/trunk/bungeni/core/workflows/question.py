# encoding: utf-8

from zope import component
from bungeni.core.workflows.notification import Notification
from bungeni.core.workflows import interfaces
from bungeni.core import globalsettings as prefs
from bungeni.core.workflows import dbutils
from bungeni.core.i18n import _
from bungeni.models import domain
from ore.alchemist import Session

import bungeni.core.workflows.utils as utils
import zope.securitypolicy.interfaces

class actions:
    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def makePrivate(info,context):
        """
        a question that is not being asked
        """
        pass

    @staticmethod
    def reDraft(info, context):
        """

        """
        pass


    #def resubmitClerk(info,context):
    #    submitToClerk(info,context)

    @staticmethod
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

    @staticmethod
    def recievedByClerk( info, context ):
        """
        the question is recieved by the clerks office, 
        the clerk can edit the question
        """
        utils.createVersion(info, context)   
        #question = removeSecurityProxy(context)     
        #zope.securitypolicy.interfaces.IRolePermissionMap( question ).grantPermissionToRole( 'bungeni.question.edit', u'bungeni.Clerk' )

    @staticmethod
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


    @staticmethod
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

    @staticmethod
    def defer(info,context):
        """
        A question that cannot be debated it is available for scheduling
        but cannot be edited
        """
        pass
    #def deferMinistry(info,context):
    #    utils.setMinistrySubmissionDate(info, context)


    @staticmethod
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

    @staticmethod
    def respondWriting(info,context):
        """
        A written response from a ministry
        """
        pass


    @staticmethod
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



    @staticmethod
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

    @staticmethod
    def reject(info,context):
        """
        A question that is not admissible, 
        Nobody is allowed to edit it
        """
        #question = removeSecurityProxy(context)
        #denyAllWrites(question)
        pass

    @staticmethod
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

    @staticmethod
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


    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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


    @staticmethod
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
   
class SendNotificationToMemberUponReceipt(Notification):
    component.adapts(interfaces.IQuestionReceivedEvent)

    body = _('notification_email_to_member_upon_receipt_of_question',
             default="Question received.")
    
    @property
    def subject(self):
        return u'Question received: %s' % self.context.subject

    @property
    def condition(self):
        return self.context.receive_notification

    @property
    def from_address(self):
        return prefs.getClerksOfficeEmail()
    
class SendNotificationToClerkUponSubmit(Notification):
    """Send notification to Clerk's office upon submit.

    We need to settings from a global registry to determine whether to
    send this notification and where to send it to.
    """

    component.adapts(interfaces.IQuestionSubmittedEvent)

    body = _('notification_email_to_clerk_upon_submit_of_question',
             default="Question submitted.")

    @property
    def subject(self):
        return u'Question submitted: %s' % self.context.subject

    @property
    def condition(self):
        return prefs.getClerksOfficeRecieveNotification()
    
    @property
    def recipient_address(self):
        return prefs.getClerksOfficeEmail()

class SendNotificationToMemberUponReject(Notification):
    """Issued when a question was rejected by the speakers office.
    Sends a notice that the Question was rejected"""

    component.adapts(interfaces.IQuestionRejectedEvent)

    body = _('notification_email_to_member_upon_rejection_of_question',
             default="Question rejected.")

    @property
    def subject(self):
        return u'Question rejected: %s' % self.context.subject

    @property
    def condition(self):
        return self.context.receive_notification
    
    @property
    def from_address(self):
        return prefs.getSpeakersOfficeEmail()

class SendNotificationToMemberUponNeedsClarification(Notification):
    """Issued when a question needs clarification by the MP
    sends a notice that the question needs clarification"""

    component.adapts(interfaces.IQuestionClarifyEvent)

    body = _('notification_email_to_member_upon_need_clarification_of_question',
             default="Your question needs to be clarified.")

    @property
    def subject(self):
        return u'Question needs clarification: %s' % self.context.subject

    @property
    def condition(self):
        return self.context.receive_notification
    
    @property
    def from_address(self):
        return prefs.getClerksOfficeEmail()

class SendNotificationToMemberUponDeferred(Notification):
    """Issued when a question was deferred by Clerk's office."""

    component.adapts(interfaces.IQuestionDeferredEvent)

    body = _('notification_email_to_member_upon_defer_of_question',
             default="Question deferred.")

    @property
    def subject(self):
        return u'Question deferred: %s' % self.context.subject

    @property
    def condition(self):
        return self.context.receive_notification
    
    @property
    def from_address(self):
        return prefs.getSpeakersOfficeEmail()

class SendNotificationToMemberUponSchedule(Notification):
    """Issued when a question was scheduled by Speakers office.
    Sends a Notice that the question is scheduled for ... """

    component.adapts(interfaces.IQuestionScheduledEvent)

    body = _('notification_email_to_member_upon_schedule_of_question',
             default="Question scheduled.")

    @property
    def subject(self):
        return u'Question scheduled: %s' % self.context.subject

    @property
    def condition(self):
        return self.context.receive_notification
    
    @property
    def from_address(self):
        return prefs.getClerksOfficeEmail()

class SendNotificationToMemberUponPostponed(Notification):
    """Issued when a question was postponed by the speakers office.
    sends a notice that the question could not be debated and was postponed"""

    component.adapts(interfaces.IQuestionPostponedEvent)

    body = _('notification_email_to_member_upon_postpone_of_question',
             default="Question postponed.")

    @property
    def subject(self):
        return u'Question postponed: %s' % self.context.subject

    @property
    def condition(self):
        return self.context.receive_notification
    
    @property
    def from_address(self):
        return prefs.getClerksOfficeEmail()

class SendNotificationToMemberUponComplete(Notification):
    """The question is marked as “complete” and is made available /
    forwarded to the Speaker's Office for reviewing and to make it
    “admissible”."""
    
    component.adapts(interfaces.IQuestionCompleteEvent)

    body = _('notification_email_to_member_upon_complete_of_question',
             default="Question completed for review at the speakers office.")
    
    @property
    def subject(self):
        return u"Question forwarded to Speaker's Office: %s" % self.context.subject

    @property
    def condition(self):
        return self.context.receive_notification
    
    @property
    def from_address(self):
        return prefs.getClerksOfficeEmail()

class SendNotificationToMinistryUponComplete(Notification):
    """At the same time the question is also forwarded to the
    ministry."""

    component.adapts(interfaces.IQuestionCompleteEvent)
    
    body = _('notification_email_to_ministry_upon_complete_question',
             default=u"Question assigned to ministry.")

    @property
    def subject(self):
        return u'Question asked to ministry: %s' % self.context.subject

    @property
    def condition(self):
        return self.context.ministry_id
    
    @property
    def from_address(self):
        return prefs.getClerksOfficeEmail()

    @property
    def recipient_address(self):
        session = Session()
        ministry = session.query(domain.Ministry).get(
            self.context.ministry_id)
        return dbutils.getMinsiteryEmails(ministry)

class SendNotificationToMemberUponSentToMinistry(Notification):
    """Issued when a question was sent to a ministry for written
    response.  sends a notice that the question was sent to the
    ministry ... for a written response"""
    
    component.adapts(interfaces.IQuestionSentToMinistryEvent)

    body = _('notification_email_to_member_upon_sent_to_ministry_of_question',
             default="Question sent to ministry for a written answer.")
    
    @property
    def subject(self):
        return u"Question sent to ministry: %s" % self.context.subject

    @property
    def condition(self):
        return self.context.receive_notification
    
    @property
    def from_address(self):
        return prefs.getClerksOfficeEmail()

class SendNotificationToMemberUponAnswer(Notification):
    """Issued when a questions answer was reviewed by Clerk's office.
    sends a notice that the question was either debated or recieved a
    written answer by the ministry and that the answer is available
    ..."""
    
    component.adapts(interfaces.IQuestionAnsweredEvent)

    body = _('notification_email_to_member_upon_answer_of_question',
             default="Question answered.")
    
    @property
    def subject(self):
        return u"Question answered: %s" % self.context.subject

    @property
    def condition(self):
        return self.context.receive_notification
    
    @property
    def from_address(self):
        return prefs.getClerksOfficeEmail()
