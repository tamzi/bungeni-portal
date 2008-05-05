from persistent import Persistent
from zope.interface import implements
from marginalia.interfaces import ISimpleDocument
from marginalia.interfaces import IMarginaliaAnnotatableAdaptor
from zope.component import getMultiAdapter

from zope.interface import implements
from zope.component import adapts

class SimpleDocument(Persistent):
    implements(ISimpleDocument)

    title = u''
    description = u''

class SimpleDocumentAnnotationAdaptor(object):
    """Adapts Simple Document to be Annotatable."""
    implements(IMarginaliaAnnotatableAdaptor)
    adapts(ISimpleDocument)

    def __init__(self, context):
        self.context = context

    def getBodyText(self):
        """Returns the annotable text"""
        return self.context.description
        
    def isAnnotatable(self):
        """Returns a boolean True"""
        return True

    def getAnnotatedUrl(self, request=None):
        """Returns the annotated url """
        view = getMultiAdapter((self.context, request), name=u'absolute_url')
        return view()

from zope.component.factory import Factory

documentFactory = Factory(
    SimpleDocument,
    title=u"Create a simple document.",
    description = u"This factory instantiates a new document."
    )
