import urllib

from zope import interface
from zope import component
from zope.component import queryMultiAdapter
from zope.component import getMultiAdapter
from zope.component import getSiteManager
from zope.traversing.namespace import view
from zope.traversing.browser.absoluteurl import SiteAbsoluteURL
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.annotation.interfaces import IAnnotations
from zope.publisher.interfaces.browser import IHTTPRequest
from zope.proxy import sameProxiedObjects
from zope.publisher.http import DEFAULT_PORTS
from zope.app.publication.interfaces import IBrowserRequestFactory
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.publisher.browser import BrowserRequest, BrowserResponse
from zope.publisher.browser import isHTML
from zope.app.component.hooks import getSite
from zope.component import getMultiAdapter
from zope.traversing.browser.interfaces import IAbsoluteURL
from zc.resourcelibrary import publication
from zc.resourcelibrary import getIncluded
from zope.location.interfaces import ISite

from bungeni.models.interfaces import IBungeniApplication

annotation_key = "rh"
_safe = '@+' # see ``zope.traversing.browser.absoluteurl``

class Request(BrowserRequest):
    interface.classProvides(IBrowserRequestFactory)

    def _createResponse(self):
        response = Response()
        self.resource_libraries = response.resource_libraries = []
        return response

class Response(publication.Response):
    """Custom response-class which uses ``IAbsoluteURL`` adapter to
    generate URLs for resources.

    This has been committed upstream to ``zc.resourcelibrary`` in
    r99596; if accepted and a release is issued, this component can go
    away.
    """

    def _generateIncludes(self, libraries):
        # generate the HTML that will be included in the response
        site = getSite()
        if site is None:
            raise RuntimeError(
                "Unable to locate resources; no site has been set.")

        # look up resources view factory
        factory = getSiteManager().adapters.lookup(
            (ISite, interface.providedBy(self._request)),
            interface.Interface, name="")

        if IBrowserPublisher.implementedBy(factory):
            resources = factory(site, self._request)
        else:
            # a setup with no resources factory is supported; in this
            # case, we manually craft a URL to the resource publisher
            # (see ``zope.app.publisher.browser.resource``).
            resources = None
            base = queryMultiAdapter(
                (site, self._request), IAbsoluteURL, name="resource")
            if base is None: 
                baseURL = str(getMultiAdapter(
                    (site, self._request), IAbsoluteURL))
            else:
                baseURL = str(base)

        html = []
        for lib in libraries:
            if resources is not None:
                library_resources = resources[lib]

            included = getIncluded(lib)
            for file_name in included:
                if resources is not None:
                    url = library_resources[file_name]()
                else:
                    url = "%s/@@/%s/%s" % (baseURL, lib, file_name)
                if file_name.endswith('.js'):
                    html.append('<script src="%s" ' % url)
                    html.append('    type="text/javascript">')
                    html.append('</script>')
                elif file_name.endswith('.css'):
                    html.append('<style type="text/css" media="all">')
                    html.append('  <!--')
                    html.append('    @import url("%s");' % url)
                    html.append('  -->')
                    html.append('</style>')
                elif file_name.endswith('.kss'):
                    html.append('<link type="text/kss" href="%s" rel="kinetic-stylesheet" />' % url)
                else:
                    # shouldn't get here; zcml.py is supposed to check includes
                    raise RuntimeError('Resource library doesn\'t know how to '
                                       'include this file: "%s"' % file_name)

        return '\n    '.join(html)


class ResourceHost(object):
    def __init__(self, host, proto, port):
        if port and str(port) != DEFAULT_PORTS.get(proto):
            host = '%s:%s' % (host, port)
        self.host = "%s://%s" % (proto, host)
        
    def setVirtualHostRoot(self, app_names):
        self.app_names = tuple(app_names)

    @property
    def url(self):
        return "/".join((self.host,)+self.app_names)
            
class rh(view):
    def traverse(self, name, ignored):
        traversal_stack = self.request.getTraversalStack()
        app_names = []

        if not name:
            return self.context
        
        try:
            proto, host, port = name.split(":")
        except ValueError:
            raise ValueError("Vhost directive should have the form "
                             "++vh++protocol:host:port")

        rhost = IAnnotations(self.request)[annotation_key] = ResourceHost(
            host, proto, port)

        if '++' in traversal_stack:
            segment = traversal_stack.pop()
            while segment != '++':
                app_names.append(segment)
                segment = traversal_stack.pop()
            self.request.setTraversalStack(traversal_stack)
        else:
            raise ValueError(
                "Must have a path element '++' after a virtual host "
                "directive.")

        rhost.setVirtualHostRoot(app_names)

        return self.context

class ResourceSiteAbsoluteURL(SiteAbsoluteURL):
    component.adapts(IBungeniApplication, IHTTPRequest)
    interface.implementsOnly(IAbsoluteURL)

    rhost = None
    
    def __new__(cls, context, request):
        rhost = IAnnotations(request).get(annotation_key)
        if rhost is not None:
            inst = object.__new__(cls, context, request)
            inst.rhost = rhost
            return inst
    
    def __str__(self):
        return self.rhost.url

    __call__ = __str__
