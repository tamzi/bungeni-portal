from zope.publisher.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile

class Workspace(BrowserView):
    __call__ = ViewPageTemplateFile("templates/workspace.pt")

    

