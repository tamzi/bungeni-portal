# -*- coding: utf-8 -*-

from zope.interface import Interface

##code-section HEAD
##/code-section HEAD

class ILegislationFolder(Interface):
    """Marker interface for .LegislationFolder.LegislationFolder
    """

class IBill(Interface):
    """Marker interface for .Bill.Bill
    """

class IBillPage(Interface):
    """Marker interface for .BillPage.BillPage
    """

class IBillSection(Interface):
    """Marker interface for .BillSection.BillSection
    """

class IAmendment(Interface):
    """Marker interface for .Amendment.Amendment
    """

##code-section FOOT
##/code-section FOOT