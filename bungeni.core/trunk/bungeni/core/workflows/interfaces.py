from zope.component.interfaces import IObjectEvent

###############
# Questions
###############
class IQuestionSubmittedEvent(IObjectEvent):
    """Question was submitted to Clerk's office."""

class IQuestionReceivedEvent(IObjectEvent):
    """Issued when a question was received by Clerk's office."""

class IQuestionRejectedEvent(IObjectEvent):
    """Issued when a question was rejected by the speakers office."""

class IQuestionClarifyEvent(IObjectEvent):
    """Issued when a question needs clarification by the MP"""

class IQuestionDeferredEvent(IObjectEvent):
    """Issued when a question was deferred by Clerk's office."""

class IQuestionScheduledEvent(IObjectEvent):
    """Issued when a question was scheduled by Speakers office."""

class IQuestionPostponedEvent(IObjectEvent):
    """Issued when a question was postponed by the speakers office."""

class IQuestionSentToMinistryEvent(IObjectEvent):
    """Issued when a question was sent to a ministry for written response."""

class IQuestionAnsweredEvent(IObjectEvent):
    """Issued when a questions answer was reviewed by Clerk's office."""

###################
# Motions
###################

class IMotionReceivedEvent(IObjectEvent):
    """ Motion recieved by clerks office"""

class IMotionSubmittedEvent(IObjectEvent):
    """ Motion submitted to clerks office """
    
class IMotionRejectedEvent(IObjectEvent):
    """Issued when a Motion was rejected by the speakers office."""

class IMotionClarifyEvent(IObjectEvent):
    """Issued when a Motion needs clarification by the MP"""

class IMotionDeferredEvent(IObjectEvent):
    """Issued when a Motion was deferred by Clerk's office."""

class IMotionScheduledEvent(IObjectEvent):
    """Issued when a Motion was scheduled by Speakers office."""

class IMotionPostponedEvent(IObjectEvent):
    """Issued when a Motion was postponed by the speakers office."""

class IMotionDebatedEvent(IObjectEvent):
    """Issued when a Motions answer was debated"""
    
######################
# Bills
######################


    
