"""
workflow ui components
"""

from zope import component
from alchemist.ui.core import BaseForm
from zope.security.proxy import removeSecurityProxy
from zope.app.pagetemplate import ViewPageTemplateFile
from ore.workflow import interfaces
from bungeni.core.i18n import _
from zope.formlib import form
from zope.viewlet.manager import WeightOrderedViewletManager
from zope.viewlet import viewlet
import zope.interface
from interfaces import IWorkflowViewletManager

class WorkflowViewletManager( WeightOrderedViewletManager ):
    """
    implements the Workflowviewlet
    """
    zope.interface.implements(IWorkflowViewletManager)

class WorkflowViewlet( viewlet.ViewletBase ):
    """"
    implements the workflowviewlet
    this viewlet shows the current workflow state.
    """
    
    def __init__( self, context, request, view, manager ):
        self.weight = 0
        self.context = context
        #self.request = request
        self.__parent__= view
        #self.manager = manager
        self.wf_status = 'new'
        
    def update(self):
        try:
            wf_state =interfaces.IWorkflowState( removeSecurityProxy(self.context) ).getState()
        except:
            wf_state = 'undefined'            
        self.wf_status = wf_state       
        
    def render ( self ):
        return ( self.wf_status )


#################################
# workflow transition 2 formlib action bindings
class TransitionHandler( object ):

    def __init__( self, transition_id, wf_name=None):
        self.transition_id = transition_id
        self.wf_name = wf_name

    def __call__( self, form, action, data ):
        context = getattr( form.context, '_object', form.context )

        if self.wf_name:
            info = component.getAdapter( context, interfaces.IWorkflowInfo, self.wf_name )
        else:
            info = interfaces.IWorkflowInfo( context )
        info.fireTransition( self.transition_id )
        form.setupActions()

def bindTransitions( form_instance, transitions, wf_name=None, wf=None):
    """ bind workflow transitions into formlib actions """

    if wf_name:
        success_factory = lambda tid: TransitionHandler( tid, wf_name )
    else:
        success_factory = TransitionHandler

    actions = []
    for tid in transitions:
        d = {}
        if success_factory:
            d['success'] = success_factory( tid )
        if wf is not None:
            action = form.Action( _(unicode(wf.getTransitionById( tid ).title) ) )
        else:
            action = form.Action( tid, **d )
        action.form = form_instance
        action.__name__ = "%s.%s"%(form_instance.prefix, action.__name__)
        actions.append( action )
    return actions

class Workflow( BaseForm ):
    
    template = ViewPageTemplateFile('templates/workflow.pt')
    form_name = "Workflow"
    form_fields = form.Fields()
    
    def update( self ):
        self.setupActions()   
        super( Workflow, self).update()
        self.setupActions()  # after we transition we have different actions      
        wf_state =interfaces.IWorkflowState( removeSecurityProxy(self.context) ).getState()
        self.wf_status = wf_state
        
    def setupActions( self ):
        self.wf = interfaces.IWorkflowInfo( self.context )
        transitions = self.wf.getManualTransitionIds()
        self.actions = bindTransitions( self, transitions )
