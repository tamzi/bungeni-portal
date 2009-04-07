"""
$Id:

"""
from zope.viewlet.manager import WeightOrderedViewletManager
from zope.app.publisher.browser.menu import getMenu
from zope.traversing.browser import absoluteURL
from ploned.ui.interfaces import IStructuralView
from ploned.ui.menu import is_selected

class StructureAwareViewlet(object):
    def __init__(self, context, request, view, manager):
        if IStructuralView.providedBy(view):
            context = context.__parent__
        super(StructureAwareViewlet, self).__init__(
            context, request, view, manager)

class WeightBasedSorter( WeightOrderedViewletManager ):
    """
    No need to do a custom sort implementation - it did not work anyway
    """

class ContentViewsViewlet(StructureAwareViewlet):
    def update(self):
        # define the request url as the computed view url
        request_url = absoluteURL(self.__parent__, self.request)

        # retrieve menu
        menu = getMenu("context_actions", self.context, self.request)

        # compute selected menu
        for item in menu:
            selected = is_selected(item, item['action'], request_url)
            item['selected'] = selected and 'selected' or ''

        self.context_actions = menu
