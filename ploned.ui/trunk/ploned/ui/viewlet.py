"""
$Id:

"""
from zope.viewlet.manager import WeightOrderedViewletManager
from ploned.ui.interfaces import IStructuralView

class WeightBasedSorter( WeightOrderedViewletManager ):
    """
    No need to do a custom sort implementation - it did not work anyway
    """
 
class ContentTabsViewlet(object):
    def __init__(self, context, request, view, manager):
        if IStructuralView.providedBy(view):
            context = context.__parent__
        super(ContentTabsViewlet, self).__init__(
            context, request, view, manager)

