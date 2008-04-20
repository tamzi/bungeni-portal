from persistent import Persistent
from zope.interface import implements
from marginalia.interfaces import IAnnotation

class Annotation(Persistent):
    implements(IAnnotation)

    __name__ = __parent__ = None

    url = u''
    start_block = u''
    start_xpath = u''
    start_word = u''
    start_char = u''
    end_block = u''
    end_xpath = u''
    end_word = u''
    end_char = u''
    note = u''
    access = u''
    action = u''
    edit_type = u''
    quote = u''
    quote_title = u''
    quote_author = u''
    link_title = u''
    indexed_url = u''
    link = u''

    def getUserName(self):
        pass

    def Title(self):
        pass

    def Description(self):
        pass

    def SearchableText(self):
        pass

    def getEditType(self):
        pass

    def getIndexed_url(self):
        pass

    def getLink(self):
        pass

    def getSequenceRange(self):
        pass
        
    def getXPathRange(self):
        pass    

from zope.component.factory import Factory

annotationFactory = Factory(
    Annotation,
    title=u"Create an Annotation.",
    description = u"This factory instantiates an Annotation."
    )
