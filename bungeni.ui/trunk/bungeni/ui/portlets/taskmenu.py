from zope import component

from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.viewlet import viewlet
import bungeni.core.globalsettings as prefs


class TaskMenuViewlet(object):
    render = ViewPageTemplateFile("templates/taskmenu.pt")
    
    def update(self):
        self.menu = component.getUtility(IBrowserMenu, name='task_actions')

    def items(self):
        return self.menu.getMenuItems(self.context, self.request)
        
    def available(self):
        items = self.items()
        return bool(items)
        
        
class ClerksTaskMenuViewlet( viewlet.ViewletBase ):  
    render = ViewPageTemplateFile("templates/clerks-task-menu.pt")      
    
    
class MpsTaskMenuViewlet( viewlet.ViewletBase ):  
    render = ViewPageTemplateFile("templates/mps-task-menu.pt")          
    
class SpeakersTaskMenuViewlet( viewlet.ViewletBase ):  
    render = ViewPageTemplateFile("templates/speakers-task-menu.pt")        
    
