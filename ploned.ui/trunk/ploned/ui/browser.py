from zope import interface
from zope import component
from zope.publisher.browser import BrowserView
from zope.security import checkPermission
from zope.viewlet.interfaces import IViewlet
from zope.viewlet.interfaces import IViewletManager

class PloneView(BrowserView):
    def show_editable_border(self):
        return checkPermission("zope.ManageContent", self.context)  

    def have_viewlets(self, view, name):
        gsm = component.getSiteManager()

        specification = map(interface.providedBy, (self.context, self.request, view))
        manager = gsm.adapters.lookup(specification, IViewletManager, name=name)

        iface = tuple(interface.implementedBy(manager))[0]
        specification.append(iface)

        for viewlet in  gsm.adapters.lookupAll(specification, IViewlet):
            return True

        return False

    def __call__(self):
        """Return ``self`` such that templates don't need an explicit
        ``nocall`` pragma."""
        
        return self
