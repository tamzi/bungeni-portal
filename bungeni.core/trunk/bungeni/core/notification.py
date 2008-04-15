from zope import component
from zope.i18n import translate

from bungeni.core.workflows.interfaces import IQuestionReceivedEvent
from bungeni.core.workflows.interfaces import IQuestionSubmittedEvent
from bungeni.core.domain import User

from email.mime.text import MIMEText
from bungeni.server.smtp import dispatch

from ore.alchemist import Session

portal_from_address = "Bungeni Portal <bungeni@localhost>"

@component.adapter(IQuestionReceivedEvent)
def sendNotificationToMemberUponReceipt(event):
    question = event.object

    if not question.receive_notification:
        return
    
    session = Session()
    owner = session.query(User).get(question.owner_id)
    
    text = translate('notification_email_to_member_upon_receipt_of_question',
                     target_language='en',
                     domain='bungeni.core',
                     default="Question received.")
    
    msg = MIMEText(text)

    recipient_address = '"%s %s" <%s>' % \
         (owner.first_name, owner.last_name, owner.email)

    msg['Subject'] = u'Question received: %s' % question.subject
    msg['From'] = portal_from_address
    msg['To'] = recipient_address

    dispatch(msg)

@component.adapter(IQuestionSubmittedEvent)
def sendNotificationToClerkUponSubmit(event):
    """Send notification to Clerk's office upon submit.

    We need to settings from a global registry to determine whether to
    send this notification and where to send it to.
    """

        
