# -*- coding: utf-8 -*-

from zope.interface import Interface

##code-section HEAD
##/code-section HEAD

class IMemberOfPublic(Interface):
    """Marker interface for .MemberOfPublic.MemberOfPublic
    """

class IBungeniMember(Interface):
    """Marker interface for .BungeniMember.BungeniMember
    """

class IMemberOfParliament(Interface):
    """Marker interface for .MemberOfParliament.MemberOfParliament
    """

class IBungeniMembershipTool(Interface):
    """Marker interface for .BungeniMembershipTool.BungeniMembershipTool
    """

class IStaff(Interface):
    """Marker interface for .Staff.Staff
    """

##code-section FOOT
##/code-section FOOT