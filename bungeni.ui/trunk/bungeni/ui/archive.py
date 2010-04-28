from zope import interface
from zope.publisher.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile

from ploned.ui.interfaces import IViewView

class ArchiveBrowseContentView(BrowserView):
    __call__ = ViewPageTemplateFile("templates/archive.pt")

    interface.implements(IViewView)

# NOTE: AdminBrowseContentView is identical to ArchiveBrowseContentView
AdminBrowseContentView = ArchiveBrowseContentView
