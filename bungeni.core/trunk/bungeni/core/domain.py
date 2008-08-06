#!/usr/bin/env python
# encoding: utf-8
"""
domain.py

Created by Kapil Thangavelu on 2007-11-22.

"""

import md5, random, string

from zope import interface, location, component
from ore.alchemist import model, Session
from ore.workflow.interfaces import IWorkflowInfo
from alchemist.traversal.managed import one2many

import logging
import interfaces

logger = logging.getLogger('bungeni.core')



#####

def object_hierarchy_type( object ):
    if isinstance( object.__class__, User ):
        return "user"
    if isinstance( object.__class__, Group ):
        return "group"
    if isinstance( object.__class__, ParliamentaryItem ):
        return "item"
    return ""


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
    
    addresses = one2many( "addresses", "bungeni.core.domain.UserAddressContainer", "user_id" )
    sort_on = 'sort_by_name'
    sort_replace = {'user_id': 'sort_by_name'}
    
#
# sort_on is the column the query is sorted on by default
# sort_replace is a dictionary that maps one column to another
# so when the key is requested in a sort the value gets sorted
# eg: {'user_id':'sort_name'} when the sort on user_id is requested the 
# query gets sorted by sort_name
#

    
class Person( User ):
    """
    general representation of a person
    """
    sort_on = 'sort_by_name'
    sort_replace = {'user_id': 'sort_by_name'}    
    
class StaffMember( Person ):
    """
    A staff member
    """    
    sort_on = 'sort_by_name'
    sort_replace = {'user_id': 'sort_by_name'}
    
class MemberOfParliament ( Entity ):    
    """
    defined by groupmembership and aditional data
    """    
    sort_on = 'sort_by_name'
    sort_replace = {'user_id': 'sort_by_name', 'constituency_id':'constituency'}    
    titles = one2many( "titles", "bungeni.core.domain.MemberRoleTitleContainer", "membership_id" )
    party = one2many( "party", "bungeni.core.domain.MemberOfPartyContainer", "membership_id" )

class HansardReporter( User ):
    """ a reporter who reports on parliamentary procedings
    """
    sort_on = 'sort_by_name'
    sort_replace = {'user_id': 'sort_by_name'}    
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
    sort_on = 'sort_by_name'
    sort_replace = {'user_id': 'sort_by_name'}
                
class UserGroupMembership( Entity ):
    """ a user's membership in a group - abstract
    basis for ministers, committeemembers, etc
    """        
    sort_on = 'sort_by_name'
    sort_replace = {'user_id': 'sort_by_name'}
            
class StaffGroupMembership( Entity ):
    """ 
    staff assigned to groups (committees, ministries,...)
    """    
    sort_on = 'sort_by_name'
    sort_replace = {'user_id': 'sort_by_name'}
            
class CommitteeStaff( StaffGroupMembership ):
    """
    Comittee Staff
    """
    titles = one2many( "titles", "bungeni.core.domain.MemberRoleTitleContainer", "membership_id" )    
        
class GroupSitting( Entity ):
    """ a scheduled meeting for a group (parliament, committee, etc)
    """
    attendance = one2many( "attendance", "bungeni.core.domain.GroupSittingAttendanceContainer", "sitting_id" )
    #XXX
    #hack for Cairo demo
    #bills = one2many( "bills", "bungeni.core.domain.BillContainer", "sitting_id" )
    #questions = one2many( "questions", "bungeni.core.domain.QuestionContainer", "sitting_id" )
    #motions = one2many( "motions", "bungeni.core.domain.MotionContainer", "sitting_id" )
    #debates = one2many( "debates", "bungeni.core.domain.DebateContainer", "sitting_id" )
    
    @property
    def short_name( self ):
        return ( self.start_date ).strftime('%d %b %y %H:%M')
    
class SittingType( object ):
    """ Type of sitting
    morning/afternoon/... """    
    
class GroupSittingAttendance( object ):
    """ a record of attendance at a meeting 
    """
    sort_on = 'sort_by_name'
    sort_replace = {'member_id': 'sort_by_name'}
    
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
    sort_on = 'start_date'
    ministries = one2many("ministries", "bungeni.core.domain.MinistryContainer", "government_id")
    
class Parliament( Group ):
    """ a parliament
    """    
    sort_on = 'start_date'
    sessions = one2many("sessions", "bungeni.core.domain.ParliamentSessionContainer", "parliament_id")
    committees = one2many("committees", "bungeni.core.domain.CommitteeContainer", "parliament_id")
    #mps = one2many("mps","bungeni.core.domain.GroupMembershipContainer", "group_id")
    governments = one2many("governments","bungeni.core.domain.GovernmentContainer", "parliament_id")
    parliamentmembers = one2many("parliamentmembers", 
                                 "bungeni.core.domain.MemberOfParliamentContainer", "group_id")
    extensionmembers = one2many("extensionmembers", "bungeni.core.domain.ExtensionGroupContainer",
                                 "parliament_id")
    politicalparties = one2many("politicalparties", "bungeni.core.domain.PoliticalPartyContainer", "parliament_id")

    
class PoliticalParty( Group ):
    """ a political party
    """
    partymembers = one2many("partymembers","bungeni.core.domain.PartyMemberContainer", "group_id")

class PartyMember( UserGroupMembership ):
    """ 
    Member of a political party, defined by its group membership 
    """
    titles = one2many( "titles", "bungeni.core.domain.MemberRoleTitleContainer", "membership_id" )   
    
class MemberOfParty( UserGroupMembership ):
    """
    Membership of a user in a political party 
    """         
    
    
class Ministry( Group ):
    """ a government ministry
    """
    #sittings = one2many("sittings", "bungeni.core.domain.GroupSittingContainer", "group_id")
    ministers = one2many("ministers","bungeni.core.domain.MinisterContainer", "group_id")
    
class Minister( UserGroupMembership ):
    """ A Minister
    defined by its user_group_membership in a ministry (group)
    """    
    titles = one2many( "titles", "bungeni.core.domain.MemberRoleTitleContainer", "membership_id" )
    sort_replace = {'user_id': 'sort_by_name'}
    
class Committee( Group ):
    """ a parliamentary committee of MPs
    """
    sittings = one2many("sittings", "bungeni.core.domain.GroupSittingContainer", "group_id")
    committeemembers = one2many("committeemembers", "bungeni.core.domain.CommitteeMemberContainer", "group_id")
    committeestaff = one2many("committeestaff", "bungeni.core.domain.CommitteeStaffContainer", "group_id")

class CommitteeMember( UserGroupMembership ):
    """ A Member of a committee
    defined by its membership to a committee (group)""" 

    titles = one2many( "titles", "bungeni.core.domain.MemberRoleTitleContainer", "membership_id" )  
    sort_replace = {'user_id': 'sort_by_name'}
    
class CommitteeType( object):
    """ Type of Committee """
        
class ExtensionGroup( Group ):
    """ Extend selectable users for a group membership """
    extmembers = one2many("extmembers", "bungeni.core.domain.ExtensionMemberContainer", "group_id") 
    
class ExtensionMember( UserGroupMembership ):
    """ Users for Extension group """    
    sort_replace = {'user_id': 'sort_by_name'}   
   
class Debate( Entity ):
    """
    Debates
    """   

class AddressType( object ):
    """
    Address Types
    """

class UserAddress( Entity ):    
    """
    addresses of a user or official addresses for a official role
    """
    
        
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
    
class ParliamentaryItem( Entity ):

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
    responses = one2many("responses", "bungeni.core.domain.ResponseContainer", "question_id")
    @property
    def short_name( self ):
        return ( self.subject )

QuestionChange = ItemLog.makeLogFactory( "QuestionChange")
QuestionVersion = ItemVersions.makeVersionFactory("QuestionVersion")


class Response( Entity ):
    """
    Response to a Question
    """
   

class Motion( ParliamentaryItem ):
    
    interface.implements( interfaces.IMotion )
    motionamendment = one2many("motionamendment", "bungeni.core.domain.MotionAmendmentContainer", "motion_id")
    @property
    def short_name( self ):
        return ( self.title ) 
    @property
    def subject( self ):
        return ( self.title ) 
MotionChange = ItemLog.makeLogFactory( "MotionChange")
MotionVersion = ItemVersions.makeVersionFactory("MotionVersion")

class MotionAmendment( Entity ):
    """
    Amendment to a Motion
    """
    @property
    def short_name( self ):
        return ( self.title )     

class Bill( ParliamentaryItem ):

    interface.implements( interfaces.IBill )

    @property
    def short_name( self ):
        return ( self.title ) 
        
    @property
    def subject( self ):
        return ( self.title ) 

BillChange = ItemLog.makeLogFactory( "BillChange")
BillVersion = ItemVersions.makeVersionFactory("BillVersion")


#############

class ParliamentSession( Entity ):
    """
    """
    sort_on = 'start_date'
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
    
class MemberRoleTitle( Entity ):
    """
    The role title a member has in a specific context
    """    
    addresses = one2many( "addresses", "bungeni.core.domain.UserAddressContainer", "role_title_id" )    
    
#####################
# current parliament/gov/ministers/mps...

#class CurrentParliament( Entity ):
#    """
#    the current parliament 
#    """

class MinistryInParliament( object ):
    """
    auxilliary class to get the parliament and government for a ministry
    """
    
        
        
    
