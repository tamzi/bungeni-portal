#!/usr/bin/env python
# encoding: utf-8
"""
domain.py

Created by Kapil Thangavelu on 2007-11-22.

"""

import md5, random, string

from zope import interface, location, component
from ore.alchemist import model
from ore.workflow.interfaces import IWorkflowInfo
from alchemist.traversal.managed import one2many

import logging
import interfaces

logger = logging.getLogger('bungeni.core')

#####

class Entity( object ):

    interface.implements( location.ILocation )

    __name__ = None
    __parent__ = None
    
    def __init__( self, **kw ):
        
        domain_schema = model.queryModelInterface( self.__class__ )
        known_names = [ k for k,d in domain_schema.namesAndDescriptions(1)]
        
        for k,v in kw.items():
            if k in known_names:
                setattr( self, k, v)
            else:
                logger.warn("invalid attribute on %s %s"%(self.__class__.__name__, k) )
                
class User( Entity ):
    """
    Domain Object For A User
    """
    
    interface.implements( interfaces.IBungeniUser  )
    
    def __init__( self,  login=None, **kw ):
        if login:
            self.login = login
        super( User, self ).__init__( **kw )
        self.salt = self._makeSalt()
    
    def _makeSalt( self ):
        return ''.join( random.sample( string.letters, 12) )
        
    def setPassword( self, password ):
        self.password = self.encode( password )
        
    def encode( self, password ):
        return md5.md5( password + self.salt ).hexdigest()
        
    def checkPassword( self, password_attempt ):
        attempt = self.encode( password_attempt )
        return attempt == self.password


class ParliamentMember( User ):
    """ an MP
    """

    # groups

    # committees

    # ministries

    @property
    def short_name( self ):
        return u"%s %s"%( self.first_name, self.last_name )

class MemberOfParliament ( object ):    
    """
    defined by groupmembership and aditional data
    """


class HansardReporter( User ):
    """ a reporter who reports on parliamentary procedings
    """

    # rotas

    # takes
    
######    

class Group( Entity ):
    """ an abstract collection of users
    """
    interface.implements( interfaces.IBungeniGroup )

    users = one2many("users", "bungeni.core.domain.GroupMembershipContainer", "group_id")
    
class GroupMembership( Entity ):
    """ a user's membership in a group
    """
        
class GroupSitting( Entity ):
    """ a scheduled meeting for a group (parliament, committee, etc)
    """
    attendance = one2many( "attendance", "bungeni.core.domain.GroupSittingAttendanceContainer", "sitting_id" )
    
    @property
    def short_name( self ):
        return u"%s - %s"%( self.start_date, self.end_date )
    
class SittingType( object ):
    """ Type of sitting
    morning/afternoon/... """    
    
class GroupSittingAttendance( object ):
    """ a record of attendance at a meeting 
    """
    
class AttendanceType( object ):
    """
    lookup for attendance type
    """    
    
class GroupItemAssignment( object ):
    """ the assignment of a parliamentary content object to a group
    """

#############

class Government( Group ):
    """ a government
    """
    ministries = one2many("ministries", "bungeni.core.domain.MinistryContainer", "government_id")
    
class Parliament( Group ):
    """ a parliament
    """    
    sessions = one2many("sessions", "bungeni.core.domain.ParliamentSessionContainer", "parliament_id")
    committees = one2many("comittees", "bungeni.core.domain.CommitteeContainer", "parliament_id")
    #mps = one2many("mps","bungeni.core.domain.GroupMembershipContainer", "group_id")
    governments = one2many("governments","bungeni.core.domain.GovernmentContainer", "parliament_id")
    parliamentmembers = one2many("parliamentmembers", 
                                 "bungeni.core.domain.MemberOfParliamentContainer", "group_id")
    extensionmembers = one2many("extensionmembers", "bungeni.core.domain.ExtensionGroupContainer",
                                 "parliament_id")
    

    
class PoliticalParty( Group ):
    """ a political party
    """
    partymembers = one2many("partymembers","bungeni.core.domain.PartyMemberContainer", "group_id")

class PartyMember( Entity ):
    """ 
    Member of a political party, defined by its group membership 
    """
        
    
class Ministry( Group ):
    """ a government ministry
    """
    #sittings = one2many("sittings", "bungeni.core.domain.GroupSittingContainer", "group_id")
    ministers = one2many("Ministers","bungeni.core.domain.MinisterContainer", "group_id")
    
class Minister( Entity ):
    """ A Minister
    defined by its user_group_membership in a ministry (group)
    """    

class Committee( Group ):
    """ a parliamentary committee of MPs
    """
    #sittings = one2many("sittings", "bungeni.core.domain.GroupSittingContainer", "group_id")
    committeemembers = one2many("committeemembers", "bungeni.core.domain.CommitteeMemberContainer", "group_id")

class CommitteeMember( Entity ):
    """ A Member of a committee
    defined by its membership to a committee (group)""" 
    
class CommitteeType( object):
    """ Type of Committee """
        
class ExtensionGroup( Group ):
    """ Extend selectable users for a group membership """
    extmembers = one2many("extmembers", "bungeni.core.domain.ExtensionMemberContainer", "group_id") 
    
class ExtensionMember( Entity ):
    """ Users for Extension group """    

#############

class ItemLog( object ):
    """ an audit log of events in the lifecycle of a parliamentary content
    """
    @classmethod
    def makeLogFactory( klass, name ):
        factory = type( name, (klass,), {} )
        return factory

class ItemVersions( object ):
    """a collection of the versions of a parliamentary content object
    """
    @classmethod
    def makeVersionFactory( klass, name ):
        factory = type( name, (klass,), {} )    
        interface.classImplements( factory, interfaces.IVersion )
        return factory
        
class ItemVotes( object ):
    """
    """
    
class ParliamentaryItem( object ):

    interface.implements( interfaces.IBungeniContent )
    # votes

    # schedule

    # object log

    # versions

    
    @property
    def workflow( self ):
        return component.getAdapter( self, IWorkflowInfo )

class Question( ParliamentaryItem ):

    interface.implements( interfaces.IQuestion )
    #responses = one2many("responses", "bungeni.core.domain.ResponseContainer", "question_id")

QuestionChange = ItemLog.makeLogFactory( "QuestionChange")
QuestionVersion = ItemVersions.makeVersionFactory("QuestionVersion")


class Response( Entity ):
    """
    Response to a Question
    """


class Motion( ParliamentaryItem ):
    
    interface.implements( interfaces.IMotion )
    #motionamendment = one2many("motionamendment", "bungeni.core.domain.MotionAmendmentContainer", "motion_id")

MotionChange = ItemLog.makeLogFactory( "MotionChange")
MotionVersion = ItemVersions.makeVersionFactory("MotionVersion")

class MotionAmendment( Entity ):
    """
    Amendment to a Motion
    """

class Bill( ParliamentaryItem ):

    interface.implements( interfaces.IBill )


BillChange = ItemLog.makeLogFactory( "BillChange")
BillVersion = ItemVersions.makeVersionFactory("BillVersion")


#############

class ParliamentSession( Entity ):
    """
    """
    sittings = one2many("sittings", "bungeni.core.domain.GroupSittingContainer", "session_id")
    
class Rota( object ):
    """
    """

class Take( object ):
    """
    """

class TakeMedia( object ):
    """
    """

class Transcript( object ):
    """
    """    


class ObjectSubscriptions( object ):
    """
    """

# ###############

class Constituency( Entity ):
    """ a locality region, which elects an MP 
    """
    cdetail = one2many("cdetail", "bungeni.core.domain.ConstituencyDetailContainer", "constituency_id")
    
ConstituencyChange = ItemLog.makeLogFactory( "ConstituencyChange")
ConstituencyVersion = ItemVersions.makeVersionFactory("ConstituencyVersion")

class Region( Entity ):
    """
    Region of the constituency
    """
    constituencies = one2many( "constituencies", "bungeni.core.domain.ConstituencyContainer", "region" ) 
    
class Province( Entity ):
    """
    Province of the Constituency
    """
    constituencies = one2many( "constituencies", "bungeni.core.domain.ConstituencyContainer", "province" )
    
class Country( object ):
    """
    Country of Birth
    """ 
    pass   
    
class ConstituencyDetail( object ):
    """
    Details of the Constituency like population and voters at a given time
    """
    pass       
    
    
# ##########

    
class MemberTitle( object ):
    """ Titles for members in groups"""
    pass
    
class Keyword( object ):
    """ Keywords for groups """
        
        
    
