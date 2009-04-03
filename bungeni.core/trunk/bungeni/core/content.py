from zope import interface
from zope.dublincore.interfaces import IDCDescriptiveProperties
from zope.container.folder import Folder

class Section(Folder):
    """Represents a site section, e.g. 'Business'.

    Note that items are not persisted.
    """

    interface.implements(IDCDescriptiveProperties)

    def __init__(self, title=None, description=None):
        super(Section, self).__init__()
        self.title = title
        self.description = description
        
