from zope import interface
from zope import component
from zope.location.interfaces import ILocation

from bungeni.core.proxy import LocationProxy
from ore.alchemist.container import stringKey

def location_wrapped(context, location):
    """Provides location information to ``context`` based on the
    existing ``location`` tree using a location proxy."""

    return component.getMultiAdapter(
        (context, location), ILocation)

@interface.implementer(ILocation)
@component.adapter(interface.Interface, ILocation)
def get_location_from_parent(context, location):
    return component.getMultiAdapter(
        (context, location.__parent__), ILocation)

class LocationProxyAdapter(object):
    def __init__(self, container):
        self.container = container
        interface.implementer(ILocation)(self)
        
    def __call__(self, context, location):
        return LocationProxy(context, self.container, stringKey(context))
