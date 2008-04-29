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
        self.url = absoluteURL(context, request)
        
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
        return u''

    @property
    def action(self):
        return self.url + '/workflow'
    
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
