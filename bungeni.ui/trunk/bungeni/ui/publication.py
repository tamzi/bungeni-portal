# Bungeni Parliamentary Information System - http://www.bungeni.org/
# Copyright (C) 2010 - Africa i-Parliaments - http://www.parliaments.info/
# Licensed under GNU GPL v2 - http://www.gnu.org/licenses/gpl-2.0.txt

"""Manipulation of request publications

$Id$
"""
log = __import__("logging").getLogger("bungeni.ui.publication")

from zope import interface
from zope import component
from zope.app.publication.interfaces import IBeforeTraverseEvent
from zope.app.publication.interfaces import IEndRequestEvent

from ore.alchemist import Session

import re
import interfaces

from workspace import prepare_user_workspaces

'''
from bungeni.ui.utils import misc
def once_per_request(event_handler):
    """Wrap event_handler to limit execution of it to once per request."""
    # we use a Cache object as size limit is automatically managed
    cache = misc.Cache(maxsize=37)
    def event_handler_closure(event):
        key = id(event.request)
        if not cache.has(key):
            event_handler(event)
            cache.set(key, True)
    return event_handler_closure
prepare_user_workspaces = once_per_request(prepare_user_workspaces)
'''

@component.adapter(IBeforeTraverseEvent)
def on_before_traverse(event):
    """Subscriber to intercept traversal, and dispatch as needed to dedicated 
    request pre-processors. We intercept centrally and then call processors
    explicitly to guarantee execution order.
    """
    log.info("IBeforeTraverseEvent:%s:%s" % (id(event.request), event.object))
    apply_request_layers_by_url(event)
    prepare_user_workspaces(event)

#

@component.adapter(IEndRequestEvent)
def on_end_request(event):
    """Subscriber to catch end of request processing, and dispatch cleanup 
    tasks as needed. 
    """
    session = Session()
    log.info("""IEndRequestEvent:%s:%s
        closing SqlAlchemy session: %s""" % (
                                    id(event.request), event.object, session))
    session.close()


#

mapping = (
    (re.compile(r'^archive(/.*)?$'), interfaces.IArchiveSectionLayer),
    # Matches "workspace/" followed by anything other than my-archive
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
            log.debug("Adding %s layer to request for path <%s>" % (layer, path))
            interface.alsoProvides(request, layer)
            

