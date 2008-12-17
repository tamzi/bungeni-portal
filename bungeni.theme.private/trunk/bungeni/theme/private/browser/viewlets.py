from zope.component import getMultiAdapter
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.viewlet.viewlet import ViewletBase

class LogoViewlet(ViewletBase):
    def do_display(self):
        return self.request.principal.id != 'zope.manager'
        
    render = ViewPageTemplateFile('publiclogo.pt')
    
class AdminLogoViewlet(LogoViewlet):   
    render = ViewPageTemplateFile('adminlogo.pt')

class MPLogoViewlet(LogoViewlet):   
    render = ViewPageTemplateFile('mplogo.pt')

class ClerkLogoViewlet(LogoViewlet):   
    render = ViewPageTemplateFile('clerklogo.pt')
 
class SpeakerLogoViewlet(LogoViewlet):   
    render = ViewPageTemplateFile('speakerlogo.pt')
    
class AdminLogoViewlet(ViewletBase):   
    render = ViewPageTemplateFile('adminlogo.pt')    
