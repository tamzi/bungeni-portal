#!/usr/bin/env python
# encoding: utf-8


from zope.viewlet import viewlet
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.security.proxy import removeSecurityProxy
from zope.traversing.browser import absoluteURL

from bungeni.ui.i18n import _

class LibraryViewlet (viewlet.ViewletBase):
    render = ViewPageTemplateFile ('templates/attached-files.pt')  
    form_name = _(u"attached files")    
        
    def __init__( self,  context, request, view, manager ):        

        self.context = context.attached_files
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None
        self.for_display = len(self.context) > 0

    def results(self):
        return self.context
    
        
