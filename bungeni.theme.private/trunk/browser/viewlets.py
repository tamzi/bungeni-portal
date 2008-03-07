from zope.component import getMultiAdapter
from zope.pagetemplate import ViewPageTemplateFile
from zope.viewlet.viewlet import ViewletBase

class LogoViewlet(ViewletBase):
    render = ViewPageTemplateFile('publiclogo.pt')

