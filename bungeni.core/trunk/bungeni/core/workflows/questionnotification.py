# encoding: utf-8
from zope import component
from zope.i18n import translate

import bungeni.core.workflows.interfaces as interfaces
import bungeni.core.domain as domain
import bungeni.core.globalsettings as prefs
import bungeni.core.workflows.dbutils as dbutils
from email.mime.text import MIMEText
from bungeni.server.smtp import dispatch

from ore.alchemist import Session


def getQuestionOwnerEmail(question):
    session = Session()
    owner = session.query(domain.User).get(question.owner_id)
    return  '"%s %s" <%s>' % (owner.first_name, owner.last_name, owner.email)

@component.adapter(interfaces.IQuestionReceivedEvent)
def sendNotificationToMemberUponReceipt(event):
    question = event.object

    if not question.receive_notification:
        return
    
    text = translate('notification_email_to_member_upon_receipt_of_question',
                     target_language='en',
                     domain='bungeni.core',
                     default="Question received.")
    
    msg = MIMEText(text)

    recipient_address = getQuestionOwnerEmail(question)

    msg['Subject'] = u'Question received: %s' % question.subject
    msg['From'] = prefs.getClerksOfficeEmail()
    msg['To'] = recipient_address

    dispatch(msg)
    #print msg

@component.adapter(interfaces.IQuestionSubmittedEvent)
def sendNotificationToClerkUponSubmit(event):
    """Send notification to Clerk's office upon submit.

    We need to settings from a global registry to determine whether to
    send this notification and where to send it to.
    """
    if not prefs.getClerksOfficeRecieveNotification():
        return
    question = event.object
      
    text = translate('notification_email_to_clerk_upon_submit_of_question',
                     target_language='en',
                     domain='bungeni.core',
                     default="Question submitted.")
    
    msg = MIMEText(text)

    qowner_address =getQuestionOwnerEmail(question)         

    msg['Subject'] = u'Question submitted: %s' % question.subject
    msg['From'] = qowner_address
    msg['To'] = prefs.getClerksOfficeEmail()

    dispatch(msg)  
    #print msg            

@component.adapter(interfaces.IQuestionRejectedEvent)
def sendNotificationToMemberUponReject(event):
    """Issued when a question was rejected by the speakers office.
    Sends a notice that the Question was rejected"""
    question = event.object

    if not question.receive_notification:
        return
    
    text = translate('notification_email_to_member_upon_rejection_of_question',
                     target_language='en',
                     domain='bungeni.core',
                     default="Question rejected.")
    
    msg = MIMEText(text)

    recipient_address = getQuestionOwnerEmail(question)

    msg['Subject'] = u'Question rejected: %s' % question.subject
    msg['From'] = prefs.getSpeakersOfficeEmail()
    msg['To'] = recipient_address

    dispatch(msg)
    #print msg    

@component.adapter(interfaces.IQuestionClarifyEvent)
def sendNotificationToMemberUponNeedsClarification(event):
    """Issued when a question needs clarification by the MP
    sends a notice that the question needs clarification"""
    
    question = event.object

    if not question.receive_notification:
        return
    
    text = translate('notification_email_to_member_upon_need_clarification_of_question',
                     target_language='en',
                     domain='bungeni.core',
                     default="Your question needs to be clarified.")
    
    msg = MIMEText(text)

    recipient_address = getQuestionOwnerEmail(question)

    msg['Subject'] = u'Question needs clarification: %s' % question.subject
    msg['From'] = prefs.getClerksOfficeEmail()
    msg['To'] = recipient_address

    dispatch(msg)
    #print msg
        
@component.adapter(interfaces.IQuestionDeferredEvent)
def sendNotificationToMemberUponDeferred(event):
    """Issued when a question was deferred by Clerk's office."""
    
    question = event.object

    if not question.receive_notification:
        return
    
    text = translate('notification_email_to_member_upon_defer_of_question',
                     target_language='en',
                     domain='bungeni.core',
                     default="Question defferred.")
    
    msg = MIMEText(text)

    recipient_address = getQuestionOwnerEmail(question)

    msg['Subject'] = u'Question deferred: %s' % question.subject
    msg['From'] = prefs.getSpeakersOfficeEmail()
    msg['To'] = recipient_address

    dispatch(msg)
    #print msg
        
@component.adapter(interfaces.IQuestionScheduledEvent)
def sendNotificationToMemberUponSchedule(event):    
    """Issued when a question was scheduled by Speakers office.
    Sends a Notice that the question is scheduled for ... """
    
    question = event.object

    if not question.receive_notification:
        return
    
    text = translate('notification_email_to_member_upon_schedule_of_question',
                     target_language='en',
                     domain='bungeni.core',
                     default="Question scheduled.")
    
    msg = MIMEText(text)

    recipient_address = getQuestionOwnerEmail(question)

    msg['Subject'] = u'Question scheduled: %s' % question.subject
    msg['From'] = prefs.getClerksOfficeEmail()
    msg['To'] = recipient_address

    dispatch(msg)
    #print msg
    
@component.adapter(interfaces.IQuestionPostponedEvent)
def sendNotificationToMemberUponPostponed(event):
    """Issued when a question was postponed by the speakers office.
    sends a notice that the question could not be debated and was postponed"""

    question = event.object

    if not question.receive_notification:
        return
    
    text = translate('notification_email_to_member_upon_postpone_of_question',
                     target_language='en',
                     domain='bungeni.core',
                     default="Question postponed.")
    
    msg = MIMEText(text)

    recipient_address = getQuestionOwnerEmail(question)

    msg['Subject'] = u'Question postponed: %s' % question.subject
    msg['From'] = prefs.getClerksOfficeEmail()
    msg['To'] = recipient_address

    dispatch(msg)
    #print msg

@component.adapter(interfaces.IQuestionCompleteEvent)
def sendNotificationsUponComplete(event):
    """
    the question is marked as “complete” and is made available / forwarded to the Speaker's Office 
    for reviewing and to make it “admissible”. 
    At the same time the question is also forwarded to the ministry. 
    """
    question = event.object
    session = Session()
    if question.ministry_id:
        ministry = session.query(domain.Ministry).get(question.ministry_id)
        recipient_address = dbutils.getMinsiteryEmails(ministry)
        text = translate('notification_email_to_ministry_upon_complete_question',
                         target_language='en',
                         domain='bungeni.core',
                         default="Question assigned to ministry")
        
        msg = MIMEText(text)
        msg['Subject'] = u'Question asked to ministry: %s' % question.subject
        msg['From'] = prefs.getClerksOfficeEmail()
        msg['To'] = recipient_address

        dispatch(msg)
    if question.receive_notification:  
        text = translate('notification_email_to_member_upon_complete_of_question',
                         target_language='en',
                         domain='bungeni.core',
                         default="Question completed for review at the speakers office.")
        
        msg = MIMEText(text)

        recipient_address = getQuestionOwnerEmail(question)

        msg['Subject'] = u'Question forwarded to speakers office: %s' % question.subject
        msg['From'] = prefs.getClerksOfficeEmail()
        msg['To'] = recipient_address

        dispatch(msg)      
    
    #XXX
    
@component.adapter(interfaces.IQuestionSentToMinistryEvent)
def sendNotificationToMemberUponSentToMinistry(event):
    """Issued when a question was sent to a ministry for written response.
    sends a notice that the question was sent to the ministry ... for a written response"""
    question = event.object

    if not question.receive_notification:
        return
    
    text = translate('notification_email_to_member_upon_sent_to_ministry_of_question',
                     target_language='en',
                     domain='bungeni.core',
                     default="Question sent to ministry for a written answer.")
    
    msg = MIMEText(text)

    recipient_address = getQuestionOwnerEmail(question)

    msg['Subject'] = u'Question sent to ministry: %s' % question.subject
    msg['From'] = prefs.getClerksOfficeEmail()
    msg['To'] = recipient_address

    dispatch(msg)
    #print msg
    
@component.adapter(interfaces.IQuestionAnsweredEvent)
def sendNotificationToMemberUponAnswer(event):                
    """Issued when a questions answer was reviewed by Clerk's office.
    sends a notice that the question was either debated or recieved a written answer 
    by the ministry and that the answer is available ..."""
    
    question = event.object

    if not question.receive_notification:
        return
    
    text = translate('notification_email_to_member_upon_answer_of_question',
                     target_language='en',
                     domain='bungeni.core',
                     default="Question answered.")
    
    msg = MIMEText(text)

    recipient_address = getQuestionOwnerEmail(question)

    msg['Subject'] = u'Question answered: %s' % question.subject
    msg['From'] = prefs.getClerksOfficeEmail()
    msg['To'] = recipient_address

    dispatch(msg)
    #print msg
        
    


