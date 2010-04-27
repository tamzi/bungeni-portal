"""
$Id$

"""
from zope.viewlet.manager import WeightOrderedViewletManager
from zope.app.publisher.browser.menu import getMenu
from zope.app.pagetemplate import ViewPageTemplateFile

from bungeni.ui import z3evoque

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

# !+ define this in ui.viewlets for common use
class ViewTemplateFile(z3evoque.ViewTemplateFile):
    """Evoque file-based template that pre-sets the preferred collection and
    the i18n_domain. Viewlets here should use this ViewTemplateFile class.
    """
    collection = "bungeni.ui.viewlets"
    i18n_domain = "bungeni.ui"

class ContentViewsViewlet(StructureAwareViewlet):
    # evoque
    render = ViewTemplateFile("ploned.html#content_actions")
    
    # zpt
    #render = ViewPageTemplateFile(
    #    "../../../bungeni.ui/bungeni/ui/viewlets/templates/portlet-contentactions.pt")
    
    def update(self):
        # retrieve menu
        self.context_actions = getMenu("context_actions", self.context, self.request)


