#!/usr/bin/env python
# encoding: utf-8
"""
domain.py

Created by Kapil Thangavelu on 2007-11-22.

"""


from ore.alchemist import Session
#####

class Entity( object ):

    @property
    def query( self ):
        return Session().query( self.__class__)
    
class User( object ):
    """
    """

class ParliamentMember( User ):
    """
    """

    # groups

    # committees

    # ministries

class Consituencies( object ):
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

class GroupSitting( object ):
    """
    """
    
class GroupSittingAttendance( object ):
    """
    """
    
class GroupItemAssignment(object):
    """
    """

#############

class Government( Group ):
    """
    """

class Parliament( Group ):
    """
    """

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
