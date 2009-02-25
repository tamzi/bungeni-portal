from zope.publisher.browser import BrowserView
from zope.security import checkPermission

class PloneView(BrowserView):
    def showEditableBorder(self):
        return checkPermission("zope.ManageContent", self.context)  
