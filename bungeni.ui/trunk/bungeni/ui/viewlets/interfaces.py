from zope.viewlet.interfaces import IViewlet
from zope.viewlet.interfaces import IViewletManager

class IWorkspaceManager(IViewletManager):
    """Workspace viewlet manager."""

class ISchedulingManager(IViewletManager):
    """Scheduling viewlet manager."""

class ISchedulingViewlet(IViewlet):
    """A scheduling viewlet renders table rows corresponding to
    schedulable items.

    Must render columns in order:

    - Type name
    - Title
    - Workflow state
    - Modification date

    The ``title`` should be linked to the URL of the item.
    """
