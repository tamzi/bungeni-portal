#!/usr/bin/env python
# encoding: utf-8

from zope.app.basicskin.standardmacros import StandardMacros
from zope.publisher.browser import BrowserView
from zope.viewlet import viewlet
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.security.proxy import removeSecurityProxy
from zope.traversing.browser import absoluteURL

from ore.library.browser import container
from ore.library import interfaces
from zc.table import column

from bungeni.ui.i18n import _

class LibraryMacros( StandardMacros ):

    macro_pages = ('bungeni.lib_macros', 'library_template') + StandardMacros.macro_pages

def iconLink( value, item, formatter ):
    icon_url = formatter.getIcon( item )
    link = absoluteURL( item, formatter.request )   
    flink = link +'/@@download' 
    if interfaces.ILibraryFile.providedBy( item ):
        cssclass = "file"
        return '<a href="%s" class="%s"><img src="%s" alt="%s"/>%s</a>'%( 
            flink, cssclass, icon_url, _(u"File"), value )        
    else:
        cssclass = "dir"
        return '<a href="%s" class="%s"><img src="%s" alt="%s"/>%s</a>'%( 
            link, cssclass, icon_url, _(u"Directory"), value )

class LogGetter( object ):
    __slots__ = ('name',)
    key = 'ore.library.log'  
    def __init__(self, name):
        self.name = name
    def __call__(self, item, formatter ):
        log = item.last_log
        formatter.annotations[self.key] = log  
        return getattr( formatter.annotations[self.key], self.name, '')

ListingColumns = [
    column.GetterColumn( title=_(u"Name"), 
        getter=container.Decorate(lambda item, formatter: item.__name__, iconLink)), 
    #column.GetterColumn( title=_(u"Revision"), getter=container.Decorate(
    #    container.getColumnRevision, container.changeLink) ),
    column.GetterColumn( title=_(u"Type"), getter=container.getMimeType ),
    column.GetterColumn( title=_(u"Size"), getter=container.getSize ),

    column.GetterColumn( title=_(u"Modified"), getter=container.Decorate( 
        LogGetter( 'date' ), lambda x,y,z: container.format_date(x))),

    column.GetterColumn( title=_(u"Message"), getter=container.Decorate(
        LogGetter( 'message' ), lambda x,y,z: container.shortLog(x) ) ),
    ]

class LibraryViewlet (viewlet.ViewletBase, container.ContainerFormatView):
    render = ViewPageTemplateFile ('templates/library-container.pt')  
    for_display = True
    form_name = _(u"attached files")    
    columns = ListingColumns
        
    def __init__( self,  context, request, view, manager ):        

        self.context = context.files
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None

class FileDownload( BrowserView ):

    def __call__( self ):
        self.request.response.setHeader('Content-Type', self.context.mime_type)
        self.request.response.setHeader('Content-Length', self.context.size )
        self.request.response.setHeader('Content-Disposition',
                         'attachment; filename=%s'%(self.context.getId()))
        trusted = removeSecurityProxy(self.context)                                         
        f = trusted.openTempFile()                                         
        return f.read()
        
