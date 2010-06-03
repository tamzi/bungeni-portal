"""
$Id$

"""
from zope.viewlet.manager import WeightOrderedViewletManager
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

'''
# specific content

from zope.app.publisher.browser.menu import getMenu
from bungeni.ui import z3evoque
from zope.app.pagetemplate import ViewPageTemplateFile

class ContentViewsViewlet(StructureAwareViewlet):
    # evoque
    render = z3evoque.ViewTemplateFile("ploned.html#content_actions",
                collection="bungeni.ui.viewlets", i18n_domain="bungeni.ui")
    
    # zpt
    #render = ViewPageTemplateFile(
    #    "../../../bungeni.ui/bungeni/ui/viewlets/templates/portlet-contentactions.pt")
    
    def update(self):
        # retrieve menu
        self.context_actions = getMenu("context_actions", self.context, self.request)
'''

