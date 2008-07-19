# -*- coding: utf-8 -*-

from zope.interface import Interface

##code-section HEAD
##/code-section HEAD

class ICommittee(Interface):
    """Marker interface for .Committee.Committee
    """

class IPoliticalGroup(Interface):
    """Marker interface for .PoliticalGroup.PoliticalGroup
    """

class IReporters(Interface):
    """Marker interface for .Reporters.Reporters
    """

class IParliament(Interface):
    """Marker interface for .Parliament.Parliament
    """

class IOffice(Interface):
    """Marker interface for .Office.Office
    """

class IBungeniTeamSpace(Interface):
    """Marker interface for .BungeniTeamSpace.BungeniTeamSpace
    """

class IDebateRecordOffice(Interface):
    """Marker interface for .DebateRecordOffice.DebateRecordOffice
    """

class IBungeniTeam(Interface):
    """Marker interface for .BungeniTeam.BungeniTeam
    """

##code-section FOOT
##/code-section FOOT