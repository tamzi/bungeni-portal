from zope import interface
from zope import component

from bungeni.core.interfaces import ISchedulingContext
from bungeni.models.interfaces import IBungeniApplication

class PrincipalGroupSchedulingContext(object):
    interface.implements(ISchedulingContext)

    group_id = None

    def __init__(self, context):
        self.__parent__ = context

    def get_sittings(self):
        pass

class PlenarySchedulingContext(PrincipalGroupSchedulingContext):
    component.adapts(IBungeniApplication)

    group_id = "bungeni.Plenary"    
        
