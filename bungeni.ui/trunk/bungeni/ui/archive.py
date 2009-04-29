from zope import interface
from zope.publisher.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile

from ploned.ui.interfaces import IViewView
from ploned.ui.interfaces import IStructuralView

class ArchiveBrowserView(BrowserView):
    __call__ = ViewPageTemplateFile("templates/archive.pt")

    interface.implements(IViewView, IStructuralView)
