# encoding: utf-8

from zope.viewlet import viewlet
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.interface.verify import verifyObject
from zope.security import proxy

from ore.alchemist.interfaces import IAlchemistContainer, IAlchemistContent
from ore.alchemist.model import queryModelDescriptor

class BreadCrumbsViewlet( viewlet.ViewletBase ):
    """
    render the Breadcrumbs to show a user his current context
    """
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.path = []


    def _get_path( self, context, url = '' ): 
        """
        Return the current path as a list
        """
        path = []
        context = proxy.removeSecurityProxy( context )
        if context.__parent__ is not None:            
            path = path + self._get_path(context.__parent__, '../' + url )
        #if context != self.context:           
        if  IAlchemistContent.providedBy(context):
            path.append( {'name' : getattr(context, 'short_name', None ), 'url' : url})
        if IAlchemistContainer.providedBy(context):                        
            domain_model = context._class 
            descriptor = queryModelDescriptor( domain_model )
            if descriptor:
                name = getattr( descriptor, 'display_name', None)
            if not name:
                name = getattr( context, '__name__', None)  
            path.append({'name' : name, 'url' : url} )                         
        return path
        
        
        
    def update( self ):
        """
        prepare the data needed to render the viewlet.        
        """
        self.path = self._get_path(self.context)       
        
    render = ViewPageTemplateFile( 'breadcrumbs.pt' )        
    
    
