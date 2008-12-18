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
    
    
class InteractMenuViewlet( viewlet.ViewletBase ):  
    render = ViewPageTemplateFile("templates/interact-menu.pt")       
    
    def getRootUrl(self):
        m_url = prefs.getPloneMenuUrl()
        r_url = '/'.join(m_url.split('/')[:-1])    
        r_url = r_url + '/Members/' + self.user_name 
        return r_url
        
    def update( self ):
        """
        prepare the data needed to render the viewlet.        
        """
        try:
            self.user_name = self.request.principal.login          
        except:
            pass
            
