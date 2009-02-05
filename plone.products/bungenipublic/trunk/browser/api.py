from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets.portlets import navigation

class NavigationView(BrowserView):
    """This view renders a navigation tree portlet."""
    
    def __call__(self, top_level=1):
        data = navigation.Assignment(
            topLevel=int(top_level)).__of__(self)
        renderer = navigation.Renderer(
            self.context, self.request, self, None, data)
        renderer = renderer.__of__(self.context)
        renderer.update()
        return renderer.render()
