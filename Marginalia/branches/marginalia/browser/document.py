
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.component import createObject, getMultiAdapter
from zope.formlib.form import EditForm, AddForm, Fields, applyChanges
from zope.formlib.namedtemplate import NamedTemplate
from zope.formlib.namedtemplate import NamedTemplateImplementation
from zope.publisher.browser import BrowserPage

from marginalia.interfaces import ISimpleDocument

class ViewDocument(BrowserPage):

    __call__ = ViewPageTemplateFile('documentview.pt')

    def renderDescription(self):
        plaintext = createObject('zope.source.plaintext',
                                 self.context.description)
        view = getMultiAdapter((plaintext, self.request), name=u'')
        return view.render()

class DocumentEditForm(EditForm):
    form_fields = Fields(ISimpleDocument)
    label = u"Edit document"

    template = NamedTemplate('simpledocument.form')

class DocumentAddForm(AddForm):
    form_fields = Fields(ISimpleDocument)
    label = u"Add document"

    template = NamedTemplate('simpledocument.form')

    def create(self, data):
        document = createObject(u'marginalia.SimpleDocument')
        applyChanges(document, self.form_fields, data)
        return document

form_template = NamedTemplateImplementation(
    ViewPageTemplateFile('form.pt'))
