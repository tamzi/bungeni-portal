#!/usr/bin/env python
# encoding: utf-8
"""
domain.py

Created by Kapil Thangavelu on 2007-11-22.

"""


from ore.alchemist import Session
from alchemist.traversal.managed import ManagedContainer

import md5, random, string
#####

class Entity( object ):

    @property
    def query( self ):
        return Session().query( self.__class__)
    
class User( object ):
    """
    Domain Object For A User
    """
    def __init__( self, login=None ):
        self.login = login
        self.salt = ''.join( random.sample( string.letters, 12) )
    
    def checkPassword( self, password_attempt ):
        attempt = md5.md5( password_attempt + self.salt ).hexdigest()
        return attempt == self.password

    @property
    def name( self ):
        return u"%s %s"%( self.first_name, self.last_name )

class ParliamentMember( User ):
    """
    """

    # groups

    # committees

    # ministries

class Constiuencies( object ):
    """
    """

class HansardReporter( User ):
    """
    """

    # rotas

    # takes
    
######    

class Group( object ):
    """
    """
    
class GroupMembership( object ):
    """
    """
    def __init__( self, user, group ):
        self.user = user
        self.group = group
        
class GroupSitting( object ):
    """ a scheduled meeting for a group (parliament, committee, etc)
    """
    
class GroupSittingAttendance( object ):
    """ a record of attendance at a meeting 
    """
    
class GroupItemAssignment(object):
    """ the assignment of a parliamentary content object to a group
    """

#############

class Government( Group ):
    """
    """

class Parliament( Group ):
    """
    """

    members = ManagedContainer("members", "bungeni.core.domain.ParliamentMemberContainer", "parliaments.parliament_id")
    sessions = ManagedContainer("sessions", "bungeni.core.domain.SessionContainer", "parliaments.parliament_id")

class PoliticalParty( Group ):
    """
    """

class Ministry( Group ):
    """
    """

class Committee( Group ):
    """
    """
    
#############

class ItemLog( object ):
    """
    """
    @classmethod
    def makeLogFactory( klass, name ):
        return type( name, (klass,), {} )

class ItemVersions( object ):
    """
    """
    @classmethod
    def makeVersionFactory( klass, name ):
        return type( name, (klass,), {} )    


class ItemVotes( object ):
    """
    """
    
class ParliamentaryItem( object ):

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

class ParliamentSession( object ):
    """
    """
    sittings = ManagedContainer("sittings", "bungeni.core.domain.GroupSittingContainer", "sessions.session_id")
    
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

###############

class ObjectSubscriptions( object ):
    """
    """
