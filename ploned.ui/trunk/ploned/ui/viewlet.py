"""
$Id:

"""
from zope.viewlet.manager import WeightOrderedViewletManager

class WeightBasedSorter( WeightOrderedViewletManager ):
    """
    No need to do a custom sort implementation - it did not work anyway
    """
 
