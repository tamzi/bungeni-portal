# -*- coding: utf-8 -*-

from zope.interface import Interface

##code-section HEAD
##/code-section HEAD

class IMinistry(Interface):
    """Marker interface for .Ministry.Ministry
    """

class IPortfolio(Interface):
    """Marker interface for .Portfolio.Portfolio
    """

class IGovernment(Interface):
    """Marker interface for .Government.Government
    """

class IMinister(Interface):
    """Marker interface for .Minister.Minister
    """

class IAssistantMinister(Interface):
    """Marker interface for .AssistantMinister.AssistantMinister
    """

##code-section FOOT
##/code-section FOOT