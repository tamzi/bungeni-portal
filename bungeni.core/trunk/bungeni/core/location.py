from zope import interface
from zope import component
from zope.location.interfaces import ILocation

from bungeni.core.interfaces import IParliamentaryItemsContainerContext
from bungeni.core.proxy import LocationProxy
from bungeni.models import domain

from ore.alchemist.container import stringKey

# this is the authoritative mapping of type to container name
model_to_container_name_mapping = {
    domain.Question: 'questions',
    domain.Bill: 'bills',
    domain.Motion: 'motions',
    domain.Parliament: 'parliaments',
    domain.AgendaItem: 'agendaitems',
    domain.Person: 'persons',
    domain.User: 'users',
    domain.StaffMember: 'staff',
    domain.Constituency: 'constituencies',
    domain.Province: 'provinces',
    domain.Region: 'regions',
    domain.ParliamentSession: 'sessions',
    domain.Country: 'countries',
    }

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

@interface.implementer(ILocation)
@component.adapter(interface.Interface, IParliamentaryItemsContainerContext)
def get_location_from_container(context, location):
    try:
        name = model_to_container_name_mapping[type(context)]
    except KeyError:
        raise TypeError("Unable to find location for %s." % repr(context))
    
    container = getattr(location, name)
    
    return LocationProxy(context, container, stringKey(context))
