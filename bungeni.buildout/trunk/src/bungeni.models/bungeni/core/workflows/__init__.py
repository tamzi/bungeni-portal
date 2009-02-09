"""
$Id: $
"""
from zope import interface
from ore.workflow import workflow
from ore.workflow.interfaces import IWorkflowInfo
from ore.workflow.interfaces import IWorkflowState
from zope.security.proxy import removeSecurityProxy

def initializeWorkflow( object, event):
    """ in response to object created events """
    workflow = IWorkflowInfo( object )
    workflow.fireAutomatic()

def fireAutomaticTransitions( object, event ):
    """ fire automatic transitions for a new state """
    workflow = IWorkflowInfo( object )
    workflow.fireAutomatic()

class NullVersions( workflow.WorkflowVersions ):

    def hasVersionId( self, id): return False

class WorkflowState( object ):

    interface.implements( IWorkflowState )
    
    __slots__ = ('context',)
    
    def __init__( self, context ):
        self.context = context
        
    def initialize( self ):
        return
        
    def setState( self, state):
        if state != self.getState():
            context = removeSecurityProxy(self.context)
            context.status = state
            
    def setId( self, id ):
        pass # print "setting id", id
        
    def getState( self ):
        return self.context.status
        
    def getId( self ):
        return "1"

        
    
    
    
