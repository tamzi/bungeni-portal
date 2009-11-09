from zope import interface
from zope import component
from zope.app.publication.interfaces import IBeforeTraverseEvent

import re
import interfaces


mapping = (
    (re.compile(r'^archive(/.*)?$'), interfaces.IArchiveSectionLayer),
    #Matches "business/" or "business"    
    (re.compile(r'^business(/)?$'), interfaces.IBusinessWhatsOnSectionLayer),
    #Matches "business/" followed by anything but whats-on
    (re.compile(r'^business/(?!whats-on)(/.*)+$'), interfaces.IBusinessSectionLayer),
    #Matches "business/whats-on"    
    (re.compile(r'^business/whats-on(/.*)?$'), interfaces.IBusinessWhatsOnSectionLayer),
    (re.compile(r'^members(/.*)?$'), interfaces.IMembersSectionLayer), 
    (re.compile(r'^admin(/.*)?$'), interfaces.IAdminSectionLayer),        
    )

@component.adapter(IBeforeTraverseEvent)
def apply_request_layers_by_url(event):
    """Apply request layers by URL.

    This subscriber applies request-layers on the ``request`` object
    based on the request to allow layer-based component registration
    of user interface elements.
    """

    request = event.request
    path = "/".join(reversed(request.getTraversalStack()))

    for condition, layer in mapping:
        if condition.match(path) is not None:
            interface.alsoProvides(request, layer)
