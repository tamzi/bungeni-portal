#!/usr/bin/env python
# encoding: utf-8
"""
domain.py

Created by Kapil Thangavelu on 2007-11-22.

"""

import md5, random, string

from zope import interface, location
from ore.alchemist import Session, model
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

    @property
    def name( self ):
        return u"%s %s"%( self.first_name, self.last_name )

class ParliamentMember( User ):
    """ an MP
    """

    # groups

    # committees

    # ministries


    

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
    
class GroupSittingAttendance( object ):
    """ a record of attendance at a meeting 
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

class PoliticalParty( Group ):
    """ a political party
    """

class Ministry( Group ):
    """ a government ministry
    """
    sittings = one2many("sittings", "bungeni.core.domain.GroupSittingContainer", "session_id")

class Committee( Group ):
    """ a parliamentary committee of MPs
    """
    sittings = one2many("sittings", "bungeni.core.domain.GroupSittingContainer", "session_id")

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
    pass
    

class Question( ParliamentaryItem ):
    pass


QuestionChange = ItemLog.makeLogFactory( "QuestionChange")
QuestionVersion = ItemVersions.makeVersionFactory("QuestionVersion")


class Motion( ParliamentaryItem ):
    pass

MotionChange = ItemLog.makeLogFactory( "MotionChange")
MotionVersion = ItemVersions.makeVersionFactory("MotionVersion")

class Bill( ParliamentaryItem ):
    pass

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

class Constituency( object ):
    """ a locality region, which elects an MP 
    """
    cdetail = one2many("cdetail", "bungeni.core.domain.ConstituencyDetailContainer", "constituency_id")
    
ConstituencyChange = ItemLog.makeLogFactory( "ConstituencyChange")
ConstituencyVersion = ItemVersions.makeVersionFactory("ConstituencyVersion")

class Region( object ):
    """
    Region of the constituency
    """
    pass
    
class Province( object ):
    """
    Province of the Constituency
    """
    pass
    
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
