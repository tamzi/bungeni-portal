from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.app.publisher.interfaces.browser import IBrowserSubMenuItem

class IWorkflowSubMenuItem(IBrowserSubMenuItem):
    """The menu item linking to the workflow menu.
    """

class IWorkflowMenu(IBrowserMenu):
    """The workflow menu.

    This gets its menu items from the list of possible transitions in
    portal_workflow.
    """
