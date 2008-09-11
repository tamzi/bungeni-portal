from zope import component
from zope.i18n import translate

import bungeni.core.workflows.interfaces as interfaces
from bungeni.core.domain import User
import bungeni.core.globalsettings as prefs

from email.mime.text import MIMEText
from bungeni.server.smtp import dispatch

from ore.alchemist import Session


def getQuesitionOwnerEmail(motion):
    session = Session()
    owner = session.query(User).get(motion.owner_id)
    return  '"%s %s" <%s>' % (owner.first_name, owner.last_name, owner.email)

@component.adapter(interfaces.IMotionReceivedEvent)
def sendNotificationToMemberUponReceipt(event):
    motion = event.object

    if not motion.receive_notification:
        return
    
    text = translate('notification_email_to_member_upon_receipt_of_motion',
                     target_language='en',
                     domain='bungeni.core',
                     default="Motion received.")
    
    msg = MIMEText(text)

    recipient_address = getQuesitionOwnerEmail(motion)

    msg['Subject'] = u'Motion received: %s' % motion.title
    msg['From'] = prefs.getClerksOfficeEmail()
    msg['To'] = recipient_address

    dispatch(msg)
    #print msg

@component.adapter(interfaces.IMotionSubmittedEvent)
def sendNotificationToClerkUponSubmit(event):
    """Send notification to Clerk's office upon submit.

    We need to settings from a global registry to determine whether to
    send this notification and where to send it to.
    """
    if not prefs.getClerksOfficeRecieveNotification():
        return
    motion = event.object
      
    text = translate('notification_email_to_clerk_upon_submit_of_motion',
                     target_language='en',
                     domain='bungeni.core',
                     default="Motion submitted.")
    
    msg = MIMEText(text)

    qowner_address =getQuesitionOwnerEmail(motion)         

    msg['Subject'] = u'Motion submitted: %s' % motion.title
    msg['From'] = qowner_address
    msg['To'] = prefs.getClerksOfficeEmail()

    dispatch(msg)  
    #print msg            

@component.adapter(interfaces.IMotionRejectedEvent)
def sendNotificationToMemberUponReject(event):
    """Issued when a motion was rejected by the speakers office.
    Sends a notice that the Motion was rejected"""
    motion = event.object

    if not motion.receive_notification:
        return
    
    text = translate('notification_email_to_member_upon_rejection_of_motion',
                     target_language='en',
                     domain='bungeni.core',
                     default="Motion rejected.")
    
    msg = MIMEText(text)

    recipient_address = getQuesitionOwnerEmail(motion)

    msg['Subject'] = u'Motion rejected: %s' % motion.title
    msg['From'] = prefs.getSpeakersOfficeEmail()
    msg['To'] = recipient_address

    dispatch(msg)
    #print msg    

@component.adapter(interfaces.IMotionClarifyEvent)
def sendNotificationToMemberUponNeedsClarification(event):
    """Issued when a motion needs clarification by the MP
    sends a notice that the motion needs clarification"""
    
    motion = event.object

    if not motion.receive_notification:
        return
    
    text = translate('notification_email_to_member_upon_need_clarification_of_motion',
                     target_language='en',
                     domain='bungeni.core',
                     default="Your motion needs to be clarified.")
    
    msg = MIMEText(text)

    recipient_address = getQuesitionOwnerEmail(motion)

    msg['Subject'] = u'Motion needs clarification: %s' % motion.title
    msg['From'] = prefs.getClerksOfficeEmail()
    msg['To'] = recipient_address

    dispatch(msg)
    #print msg
        
@component.adapter(interfaces.IMotionDeferredEvent)
def sendNotificationToMemberUponDeferred(event):
    """Issued when a motion was deferred by Clerk's office."""
    
    motion = event.object

    if not motion.receive_notification:
        return
    
    text = translate('notification_email_to_member_upon_defer_of_motion',
                     target_language='en',
                     domain='bungeni.core',
                     default="Motion defferred.")
    
    msg = MIMEText(text)

    recipient_address = getQuesitionOwnerEmail(motion)

    msg['Subject'] = u'Motion deferred: %s' % motion.title
    msg['From'] = prefs.getSpeakersOfficeEmail()
    msg['To'] = recipient_address

    dispatch(msg)
    #print msg
        
@component.adapter(interfaces.IMotionScheduledEvent)
def sendNotificationToMemberUponSchedule(event):    
    """Issued when a motion was scheduled by Speakers office.
    Sends a Notice that the motion is scheduled for ... """
    
    motion = event.object

    if not motion.receive_notification:
        return
    
    text = translate('notification_email_to_member_upon_schedule_of_motion',
                     target_language='en',
                     domain='bungeni.core',
                     default="Motion scheduled.")
    
    msg = MIMEText(text)

    recipient_address = getQuesitionOwnerEmail(motion)

    msg['Subject'] = u'Motion scheduled: %s' % motion.title
    msg['From'] = prefs.getClerksOfficeEmail()
    msg['To'] = recipient_address

    dispatch(msg)
    #print msg
    
@component.adapter(interfaces.IMotionPostponedEvent)
def sendNotificationToMemberUponPostponed(event):
    """Issued when a motion was postponed by the speakers office.
    sends a notice that the motion could not be debated and was postponed"""

    motion = event.object

    if not motion.receive_notification:
        return
    
    text = translate('notification_email_to_member_upon_postpone_of_motion',
                     target_language='en',
                     domain='bungeni.core',
                     default="Motion postponed.")
    
    msg = MIMEText(text)

    recipient_address = getQuesitionOwnerEmail(motion)

    msg['Subject'] = u'Motion postponed: %s' % motion.title
    msg['From'] = prefs.getClerksOfficeEmail()
    msg['To'] = recipient_address

    dispatch(msg)
    #print msg
    
@component.adapter(interfaces.IMotionDebatedEvent)
def sendNotificationToMemberUponDebated(event):
    """Issued when a motion was debated """
    motion = event.object

    if not motion.receive_notification:
        return
    
    text = translate('notification_email_to_member_upon_debate_of_motion',
                     target_language='en',
                     domain='bungeni.core',
                     default="Motion was debated.")
    
    msg = MIMEText(text)

    recipient_address = getQuesitionOwnerEmail(motion)

    msg['Subject'] = u'Motion was debated: %s' % motion.title
    msg['From'] = prefs.getClerksOfficeEmail()
    msg['To'] = recipient_address

    dispatch(msg)
    #print msg
    

    


