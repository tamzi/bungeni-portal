from zope.component import getMultiAdapter
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.viewlet.viewlet import ViewletBase

class LogoViewlet(ViewletBase):
    render = ViewPageTemplateFile('publiclogo.pt')

