from zope import component

from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.app.pagetemplate import ViewPageTemplateFile

class TaskMenuViewlet(object):
    render = ViewPageTemplateFile("taskmenu.pt")
    
    def update(self):
        self.menu = component.getUtility(IBrowserMenu, name='task_actions')

    def items(self):
        return self.menu.getMenuItems(self.context, self.request)
        
    def available(self):
        items = self.items()
        return bool(items)
