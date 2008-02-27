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

from bungeni.core import audit
from sqlalchemy import orm
from zc.table import batching, column
import sqlalchemy as rdb

class WorkflowViewletManager( WeightOrderedViewletManager ):
    """
    implements the Workflowviewlet
    """
    zope.interface.implements(IWorkflowViewletManager)

class WorkflowHistoryViewlet( viewlet.ViewletBase ):
    """"
    implements the workflowHistoryviewlet
    this viewlet shows the current workflow state.
    and the workflowhistory
    """
    
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.wf_status = u'new'
        self.has_status = False
        # table to display the workflow history
        self.formatter_factory = batching.Formatter    
        self.columns = [            
            column.GetterColumn( title=_(u"date"), getter=lambda i,f: i['date'] ),
            column.GetterColumn( title=_(u"user"), getter=lambda i,f:i['user_id'] ),
            column.GetterColumn( title=_(u"description"), getter=lambda i,f:i['description'] ),
            ]    
        
    def update(self):
        has_wfstate = False
        try:
            wf_state =interfaces.IWorkflowState( removeSecurityProxy(self.context) ).getState()
            has_wfstate = True
        except:
            wf_state = u'undefined'                        
        if wf_state is None:
           wf_state =u'undefined'
           has_wfstate = False
        self.wf_status = wf_state       
        self.has_status = has_wfstate                
       
    
    render = ViewPageTemplateFile ('templates/workflowhistory_viewlet.pt')
    
    def listing( self ):
        columns = self.columns
        formatter = self.formatter_factory( self.context,
                                            self.request,
                                            self.getFeedEntries(),
                                            prefix="results",
                                            visible_column_names = [c.name for c in columns],
                                            #sort_on = ('name', False)
                                            columns = columns )
        formatter.cssClasses['table'] = 'listing'
        formatter.updateBatching()
        return formatter()
        
    @property
    def _log_table( self ):
        auditor = audit.getAuditor( self.context )
        return auditor.change_table
        
    def getFeedEntries( self ):
        instance = removeSecurityProxy( self.context )        
        mapper = orm.object_mapper( instance )
        
        query = self._log_table.select().where(
            rdb.and_( self._log_table.c.content_id == rdb.bindparam('content_id'),
            rdb.and_(self._log_table.c.action == 'workflow') )
            )

        content_id = mapper.primary_key_from_instance( instance )[0] 
        content_changes = query.execute( content_id = content_id )
        return map( dict, content_changes)
    
        

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

class WorkflowActionViewlet( BaseForm, viewlet.ViewletBase ):
    """
    display workflow status and actions
    """
    form_name = "Workflow"
    form_fields = form.Fields()

    render = ViewPageTemplateFile ('templates/workflowaction_viewlet.pt')
    
    def update( self ):
        self.setupActions()   
        super( WorkflowActionViewlet, self).update()
        self.setupActions()  # after we transition we have different actions      
        wf_state =interfaces.IWorkflowState( removeSecurityProxy(self.context) ).getState()
        self.wf_status = wf_state
        
    def setupActions( self ):
        self.wf = interfaces.IWorkflowInfo( self.context )
        transitions = self.wf.getManualTransitionIds()
        self.actions = bindTransitions( self, transitions )     

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
        
