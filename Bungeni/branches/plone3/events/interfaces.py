# -*- coding: utf-8 -*-

from zope.interface import Interface

##code-section HEAD
##/code-section HEAD

class IMotion(Interface):
    """Marker interface for .Motion.Motion
    """

class IParliamentaryEvent(Interface):
    """Marker interface for .ParliamentaryEvent.ParliamentaryEvent
    """

class IQuestion(Interface):
    """Marker interface for .Question.Question
    """

class IResponse(Interface):
    """Marker interface for .Response.Response
    """

class IOrderOfBusiness(Interface):
    """Marker interface for .OrderOfBusiness.OrderOfBusiness
    """

class IAgendaItem(Interface):
    """Marker interface for .AgendaItem.AgendaItem
    """

class ISitting(Interface):
    """Marker interface for .Sitting.Sitting
    """

class ISession(Interface):
    """Marker interface for .Session.Session
    """

class ICommitteeFolder(Interface):
    """Marker interface for .CommitteeFolder.CommitteeFolder
    """

class IParliamentaryDocument(Interface):
    """Marker interface for .ParliamentaryDocument.ParliamentaryDocument
    """

##code-section FOOT
##/code-section FOOT