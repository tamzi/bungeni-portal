from zope import interface
from zope.container.ordered import OrderedContainer
from zope.dublincore.interfaces import IDCDescriptiveProperties

from interfaces import ISection
from interfaces import IQueryContent

class Section(OrderedContainer):
    """Represents a site section, e.g. 'Business'.

    Note that items are not persisted.
    """

    interface.implements(ISection, IDCDescriptiveProperties)
    
    def __init__(self, title=None, description=None, marker=None):
        super(Section, self).__init__()
        self.title = title
        self.description = description

        if marker is not None:
            interface.alsoProvides(self, marker)

    def __getitem__(self, key):
        item = super(Section, self).__getitem__(key)
        if IQueryContent.providedBy(item):
            obj = item.query(self)
            obj.__name__ = item.__name__
            obj.__parent__ = item.__parent__
            return obj
        return item

class QueryContent(object):
    interface.implements(IQueryContent, IDCDescriptiveProperties)
    
    def __init__(self, query, title=None, description=None):
        self.query = query
        self.title = title
        self.description = description
        

    
