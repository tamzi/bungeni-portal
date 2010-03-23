from zope import interface
from zope import component
from zope.app.publication.interfaces import IBeforeTraverseEvent

import re
import interfaces


mapping = (
    (re.compile(r'^archive(/.*)?$'), interfaces.IArchiveSectionLayer),
    # Matches "workspace/" followed by anything other than my-archive
    (re.compile(r'^workspace(?!/my-archive).*$'), interfaces.IAddParliamentaryContentLayer),
    (re.compile(r'^workspace(/.*)?$'), interfaces.IWorkspaceSectionLayer),
    # Matches "business/" or "business"
    (re.compile(r'^business(/)?$'), interfaces.IBusinessWhatsOnSectionLayer),
    # Matches "business/" followed by anything but whats-on
    (re.compile(r'^business(?!/whats-on)(/.*)+$'), interfaces.IBusinessSectionLayer),
    # Matches "business/whats-on"    
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
    #print "gTS", request.getTraversalStack()
    #print "path", path
    for condition, layer in mapping:
        #print "for", condition, layer
        if condition.match(path) is not None:
            #print "MATCHES!"
            interface.alsoProvides(request, layer)
