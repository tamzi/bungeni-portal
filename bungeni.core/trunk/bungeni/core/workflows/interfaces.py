from zope.component.interfaces import IObjectEvent

class IQuestionSubmittedEvent(IObjectEvent):
    """Question was submitted to Clerk's office."""

class IQuestionReceivedEvent(IObjectEvent):
    """Issued when a question was received by Clerk's office."""

class IMotionReceivedEvent(IObjectEvent):
    """ Motion recieved by clerks office"""

class IMotionSubmittedEvent(IObjectEvent):
    """ Motion submitted to clerks office """
