from zope import interface

from zope.app.publisher.browser.menu import BrowserMenu
from zope.app.publisher.browser.menu import BrowserSubMenuItem

from zope.traversing.browser import absoluteURL

from ore.workflow.interfaces import IWorkflow, IWorkflowInfo
  
from plone.memoize.instance import memoize

from interfaces import IWorkflowSubMenuItem
from interfaces import IWorkflowMenu

from bungeni.ui.i18n import MessageFactory as _

class WorkflowSubMenuItem(BrowserSubMenuItem):
    interface.implements(IWorkflowSubMenuItem)

    title = _(u'label_state', default=u'State:')
    submenuId = 'plone_contentmenu_workflow'
    order = 40

    def __init__(self, context, request):
        BrowserSubMenuItem.__init__(self, context, request)
        self.context = context
        
    @property
    def extra(self):
        info = IWorkflowInfo(self.context)
        state = info.state().getState()
        
        return {'id'         : 'plone-contentmenu-workflow',
                'class'      : 'state-%s' % state,
                'state'      : state,
                'stateTitle' : state,} # TODO: should be translated

    @property
    def description(self):
        """TODO: Migrate to ore.workflow."""
        
        #if self._manageSettings() or len(self._transitions()) > 0:
        #    return _(u'title_change_state_of_item', default=u'Change the state of this item')
        #else:
        #    return u''

        return u''

    @property
    def action(self):
        """TODO: Migrate."""

        #if self._manageSettings() or len(self._transitions()) > 0:
        #    return self.context.absolute_url() + '/content_status_history'
        #else:
        #    return ''

        return u''
    
    @memoize
    def available(self):
        return bool(IWorkflow(self.context, None))
    
    def selected(self):
        return False

class WorkflowMenu(BrowserMenu):
    interface.implements(IWorkflowMenu)

    def getMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""

        results = []

        wf = IWorkflow(context)
        state = IWorkflowInfo(context).state().getState()
        transitions = wf.getTransitions(state)

        url = absoluteURL(context, request)

        for transition in transitions:

            tid = transition.transition_id
            transition_url = url + '/change_workflow_state?transition_id=%s' % tid

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
