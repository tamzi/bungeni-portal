from persistent import Persistent
from zope.interface import implements
from marginalia.interfaces import ISimpleDocument

class SimpleDocument(Persistent):
    implements(ISimpleDocument)

    title = u''
    description = u''

from zope.component.factory import Factory

documentFactory = Factory(
    SimpleDocument,
    title=u"Create a simple document.",
    description = u"This factory instantiates a new document."
    )
