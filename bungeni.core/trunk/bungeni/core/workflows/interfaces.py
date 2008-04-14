from zope.component.interfaces import IObjectEvent

class IQuestionReceivedEvent(IObjectEvent):
    """Issued when a question was received by Clerk's office."""
