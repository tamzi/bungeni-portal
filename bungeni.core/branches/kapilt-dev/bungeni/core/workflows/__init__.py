"""
$Id: $
"""
from zope import interface
from ore.workflow import interfaces, workflow

def initializeWorkflow( object, event):
    """ in response to object created events """
    workflow = interfaces.IWorkflowInfo( object )
    workflow.fireAutomatic()

def fireAutomaticTransitions( object, event ):
    """ fire automatic transitions for a new state """
    workflow = interfaces.IWorkflowInfo( object )
    workflow.fireAutomatic()

class NullVersions( workflow.WorkflowVersions ):

    def hasVersionId( self, id): return False

class WorkflowState( object ):

    interface.implements( interfaces.IWorkflowState )
    
    __slots__ = ('context',)
    
    def __init__( self, context ):
        self.context = context
        
    def initialize( self ):
        return
        
    def setState( self, state):
        if state != self.getState():
            self.context.status = state
            
    def setId( self, id ):
        print "setting id", id
        
    def getState( self ):
        return self.context.status
        
    def getId( self ):
        return "1"

        
    
    
    