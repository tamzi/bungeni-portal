from zope.interface import implements
from zope.component import adapts
from zope.exceptions.interfaces import UserError
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('marginalia')

from zope.app.container.btree import BTreeContainer
from marginalia.interfaces import IAnnotationsContainer
from zope.app.container.contained import NameChooser

class AnnotationsFolder(BTreeContainer):
    implements(IAnnotationsContainer)

class AnnotationNameChooser(NameChooser):
    adapts(IAnnotationsContainer)

    def checkName(self, name, object):
        if name != object.name:
            raise UserError(_(u"Given name and annotation name do not match!"))
        return super(AnnotationNameChooser, self).checkName(name, object)

    def chooseName(self, name, object):
        name = object.name
        self.checkName(name, object)
        return name
