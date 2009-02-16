import os

try:
    from plone.maintemplate import Layout
except ImportError:
    from chameleon.html.template import DynamicHTMLFile as Layout

from zope import interface
from zope import component
from zope.app.component.hooks import getSite
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.app.publisher.browser.directoryresource import DirectoryResourceFactory

from bungeni import portal

bungeni = Layout(
    os.path.join(
        portal.__path__[0], 'static', 'html', 'bungeni.html'))

def get_url(context, request, path):
    """Return a URL for a given file-system resource ``path``; if a
    base host is not provided explicitly, it will be set to the
    request URL path."""

    path = os.path.abspath(path)
    gsm = component.getSiteManager()
    site_url = str(component.getMultiAdapter(
        (getSite(), request), IAbsoluteURL))
    
    for name, resource in gsm.adapters.lookupAll(
        (interface.providedBy(request),), interface.Interface):

        if not isinstance(resource, DirectoryResourceFactory):
            continue
        
        resource = resource(request)
        try:
            directory = resource.context.path
        except AttributeError:
            continue
            
        if path.startswith(directory):
            relative_path = path[len(directory)+1:]
            return "/".join(
                (site_url.rstrip('/'), '++resource++%s' % name, relative_path))

