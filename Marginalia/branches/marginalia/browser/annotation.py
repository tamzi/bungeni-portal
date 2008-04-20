from zope.component import createObject, getMultiAdapter
from zope.publisher.browser import BrowserPage, BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile
from ore.alchemist.vocabulary import DatabaseSource, ObjectSource, Session

class ViewAnnotation(BrowserPage):

    __call__ = ViewPageTemplateFile('annotationview.pt')

    def renderQuote(self):
        plaintext = createObject('zope.source.plaintext',
                                 self.context.quote)
        view = getMultiAdapter((plaintext, self.request), name=u'')
        return view.render()

from zope.formlib.form import EditForm, AddForm, Fields, applyChanges
from zope.formlib.namedtemplate import NamedTemplate
from zope.formlib.namedtemplate import NamedTemplateImplementation
from marginalia.interfaces import IAnnotation, IAnnotatable, IAnnotatableAdaptor
from zope.interface import implements
from zope.component import adapts

class AnnotationEditForm(EditForm):
    form_fields = Fields(IAnnotation).omit('__parent__', '__name__')
    label = u"Edit annotation"

    template = NamedTemplate('annotation.form')

class AnnotationAddForm(AddForm):
    form_fields = Fields(IAnnotation).omit('__parent__', '__name__')
    label = u"Add annotation"

    template = NamedTemplate('annotation.form')

    def create(self, data):
        annotation = createObject(u'marginalia.Annotation')
        applyChanges(annotation, self.form_fields, data)
        return annotation

class AnnotationView(BrowserView):
    """Annotation View Class. """
    def getOwnerList(self, request):
        """Return a list of members who have added annotations."""
        return []

    def getAuthenticatedUser(self):
        """Returns the currently authenticated member."""
        return "test"

    def getAnnotatedUrl(self, url):
        """Returns annotated url."""
        obj = IAnnotatableAdaptor(self.context)
        return obj.getAnnotatedUrl(url)

    def getBodyText(self):
        """Returns annotated url."""
        obj = IAnnotatableAdaptor(self.context)
        return obj.getBodyText()

    def isAnnotatable(self):
        """
        """
        obj = IAnnotatableAdaptor(self.context)
        return obj.isAnnotatable()

class AnnotationAdaptor(object):
    """
    """
    implements(IAnnotatable)
    #adapt(IAnnotatableAdaptor)

    def __init__(self, context):
        self.context = context

    def getBodyText(self):
        return self.context.description
        
    def getAnnotatedUrl(self, url ):
        """Returns annotated url."""        
        x = url.find( '/annotate' )
        if -1 != x:
            url = url[ : x ]
        return url

    def isAnnotatable(self):
        """
        """
        return True


form_template = NamedTemplateImplementation(
    ViewPageTemplateFile('form.pt'))
