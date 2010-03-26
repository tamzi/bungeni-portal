from zope import interface
from zope.container.ordered import OrderedContainer
from zope.container.traversal import ItemTraverser
from zope.dublincore.interfaces import IDCDescriptiveProperties
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.app.publisher.browser import getDefaultViewName

from bungeni.core.proxy import NavigationProxy
from bungeni.core.proxy import DublinCoreDescriptivePropertiesProxy

from interfaces import ISection
from interfaces import IQueryContent

class Section(OrderedContainer):
    """A site section, e.g. 'Business'.
    
    Note that items are not persisted.
    
    """
    interface.implements(ISection, IDCDescriptiveProperties, IBrowserPublisher)
    
    def __init__(self, title=None, description=None, default_name=None, marker=None):
        super(Section, self).__init__()
        self.title = title
        self.description = description
        self.default_name = default_name
        if marker is not None:
            interface.alsoProvides(self, marker)
    # !+ section.title is duplicated in ZCML menuItem definitions
    # Section should be modified to just get its title from the associated
    # view descriptor (via default_name)
    
    def __getitem__(self, key):
        item = super(Section, self).__getitem__(key)
        if IQueryContent.providedBy(item):
            obj = item.query(self)
            obj.__name__ = item.__name__
            obj.__parent__ = DublinCoreDescriptivePropertiesProxy(
                NavigationProxy(obj.__parent__, item.__parent__),
                title=self.title, description=self.description)
            return obj
        return item
    
    def __setitem__(self, key, value):
        super(Section, self).__setitem__(key, value)
        value.__parent__ = self
        value.__name__ = key
    
    def browserDefault(self, request):
        """See zope.container.traversal.ContainerTraverser.
            -> context, (view_uri,)
        """
        default_name = self.default_name
        if default_name is None:
            default_name = getDefaultViewName(self, request)
        return self, (default_name,)
    
    # !+ all methods should indicate what the expected input parameter 
    # types and return value types should be e.g. by adopting a 
    # python3-style type annotations as a doc string, 
    # as indicated in the SAMPLE docstring here:
    def publishTraverse(self, request, name):
        """ (request:IRequest, name:str) -> IView
        """
        traverser = ItemTraverser(self, request)
        return traverser.publishTraverse(request, name)

class QueryContent(object):
    interface.implements(IQueryContent, IDCDescriptiveProperties)

    def __init__(self, query, title=None, description=None, marker=None):
        if marker is not None:
            def query(parent, query=query):
                obj = query(parent)
                interface.alsoProvides(obj, marker)
                return obj
        self.query = query
        self.title = title
        self.description = description
     
