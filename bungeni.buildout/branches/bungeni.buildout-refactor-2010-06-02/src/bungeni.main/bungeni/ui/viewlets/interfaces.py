# -*- coding: utf-8 -*-
"""$Id: interfaces.py 6504 2010-04-28 17:42:44Z mario.ruggier $
"""

from zope.viewlet.interfaces import IViewlet
from zope.viewlet.interfaces import IViewletManager
from zope.publisher.interfaces.browser import IBrowserView


class IWorkspaceManager(IViewletManager):
    """Workspace viewlet manager."""


class IWorkspaceArchiveManager(IViewletManager):
    """Workspace-archive viewlet manager."""


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

