"""
$Id$

"""
from zope.viewlet.manager import WeightOrderedViewletManager
from zope.app.publisher.browser.menu import getMenu
from ploned.ui.interfaces import IStructuralView


# viewlet managers

class WeightBasedSorter(WeightOrderedViewletManager):
    """
    No need to do a custom sort implementation - it did not work anyway
    """

# viewlets

class StructureAwareViewlet(object):
    def __init__(self, context, request, view, manager):
        if IStructuralView.providedBy(view):
            context = context.__parent__
        super(StructureAwareViewlet, self).__init__(
            context, request, view, manager)

# specific content

class ContentViewsViewlet(StructureAwareViewlet):
    def update(self):
        # retrieve menu
        self.context_actions = getMenu("context_actions", self.context, self.request)

