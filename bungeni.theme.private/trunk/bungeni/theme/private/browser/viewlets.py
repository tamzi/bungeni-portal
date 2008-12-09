from zope.component import getMultiAdapter
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.viewlet.viewlet import ViewletBase

class LogoViewlet(ViewletBase):
    render = ViewPageTemplateFile('publiclogo.pt')
    
class AdminLogoViewlet(ViewletBase):   
    render = ViewPageTemplateFile('adminlogo.pt')

class MPLogoViewlet(ViewletBase):   
    render = ViewPageTemplateFile('mplogo.pt')

class ClerkLogoViewlet(ViewletBase):   
    render = ViewPageTemplateFile('clerklogo.pt')
 
class SpeakerLogoViewlet(ViewletBase):   
    render = ViewPageTemplateFile('speakerlogo.pt')
