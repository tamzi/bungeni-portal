from zope.publisher.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile

class ArchiveBrowserView(BrowserView):
    __call__ = ViewPageTemplateFile("templates/archive.pt")
