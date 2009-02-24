from zope import interface
from zope import component

from z3c.menu.ready2go import item

from zope.component.exceptions import ComponentLookupError
from zope.app.component.hooks import getSite
from zope.app.security.interfaces import IUnauthenticatedPrincipal
from zope.app.publisher.browser.menu import BrowserMenu
from zope.app.publisher.browser.menu import BrowserSubMenuItem
from zope.traversing.browser import absoluteURL

from ore.workflow.interfaces import IWorkflow, IWorkflowInfo

from plone.memoize.instance import memoize

from bungeni.ui.i18n import  _

class GlobalMenuItem( item.GlobalMenuItem ):
    #cssActive = "menubarSelected"
    #cssInactive = "menubar"
    #css = "menubar"
    pass
    
class LoginAction( GlobalMenuItem ):
    
    @property
    def available( self ):
        available = IUnauthenticatedPrincipal.providedBy( self.request.principal )
        return available

class LogoutAction( GlobalMenuItem ):
    
    @property
    def available( self ):
        authenticated = not IUnauthenticatedPrincipal.providedBy( self.request.principal )
        return authenticated
        
class DashboardAction( GlobalMenuItem ):
    
    @property
    def title( self ):
        return self.request.principal.id
        
    @property
    def available( self ):
        authenticated = not IUnauthenticatedPrincipal.providedBy( self.request.principal )
        return authenticated

class AdminAction( GlobalMenuItem ):
    
    def getURLContext( self ):
        site = getSite()
        return site['admin']

    #@property
    #def available( self ):
    #    context = self.getURLContext()
    #    return getInteraction().checkPermission( 'zope.ManageSite', context )  
        
class TaskMenu(BrowserMenu):
    def getMenuItems(self, object, request):
        spec = self.getMenuItemType()
        return [item for name, item in \
                component.getAdapters((object, request), spec)]
    
# 
# class TaskMenu( managr.MenuManager ):
#     
#     def update(self):
#         """See zope.contentprovider.interfaces.IContentProvider"""
#         self.__updated = True
# 
#         viewlets = self._getViewlets()
#             
#         viewlets = self.filter(viewlets)
#         viewlets = self.sort(viewlets)
#         # Just use the viewlets from now on
#         self.viewlets=[]
#         for name, viewlet in viewlets:
#             if ILocation.providedBy(viewlet):
#                 viewlet.__name__ = name
#             self.viewlets.append(viewlet)
#         self._updateViewlets()
# 
#     def _getViewlets( self ):
#         interaction = getInteraction()
#         # Find all content providers for the region
#         viewlets = component.getAdapters(
#             (self.context, self.request, self.__parent__, self),
#             interfaces.IViewlet)
        

class WorkflowSubMenuItem(BrowserSubMenuItem):
    title = _(u'label_state', default=u'State:')
    submenuId = 'context_workflow'
    order = 40


    def __new__(cls, context, request):
        # this is currently the only way to make sure this menu only
        # 'adapts' to a workflowed context; the idea is that the
        # component lookup will fail, which will propagate back to the
        # original lookup request
        workflow = IWorkflow(context, None)
        if workflow is None:
            return
        return object.__new__(cls, context, request)

    def __init__(self, context, request):
        BrowserSubMenuItem.__init__(self, context, request)
        self.context = context
        self.url = absoluteURL(context, request)
        
    @property
    def extra(self):
        info = IWorkflowInfo(self.context, None)
        if info is None:
            return {'id': 'plone-contentmenu-workflow'}

        state = info.state().getState()            
        stateTitle = info.workflow().workflow.states[state].title
        
        return {'id'         : 'plone-contentmenu-workflow',
                'class'      : 'state-%s' % state,
                'state'      : state,
                'stateTitle' : stateTitle,} # TODO: should be translated

    @property
    def description(self):
        return u''

    @property
    def action(self):
        return self.url + '/workflow'
    
    def selected(self):
        return False

class WorkflowMenu(BrowserMenu):
    def getMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""

        wf = IWorkflow(context, None)
        if wf is None:
            return ()
        
        state = IWorkflowInfo(context).state().getState()
        transitions = wf.getTransitions(state)

        url = absoluteURL(context, request)

        results = []
        for transition in transitions:
            tid = transition.transition_id
            transition_url = url + '/@@%s' % tid

            extra = {'id': 'workflow-transition-%s' % tid,
                     'separator': None,
                     'class': ''}
            
            results.append(
                dict(title=transition.title,
                     description="",
                     action=transition_url,
                     selected=False,
                     icon=None,
                     extra=extra,
                     submenu=None))
                     
        return results
