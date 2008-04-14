from zope import component
from zope.i18n import translate
from bungeni.core.workflows.interfaces import IQuestionReceivedEvent

from email.mime.text import MIMEText

from collective.singing.interfaces import IDispatch

portal_from_address = "Bungeni Portal <bungeni@localhost>"

@component.adapter(IQuestionReceivedEvent)
def sendNotificationToMemberUponReceipt(event):
    question = event.object
    
    text = translate('notification_email_to_member_upon_receipt_of_question',
                     target_language='en',
                     domain='bungeni.core',
                     default="Question received.")
    
    msg = MIMEText(text)

    recipient_address = 'mborch@gmail.com'

    msg['Subject'] = u'Question received: %s' % question.subject
    msg['From'] = portal_from_address
    msg['To'] = recipient_address

    dispatcher = IDispatch(msg)
    status, messaage = dispatcher()
