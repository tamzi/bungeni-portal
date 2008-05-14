# encoding: utf-8

from zope.viewlet import viewlet
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.interface.verify import verifyObject
from zope.security import proxy

from ore.alchemist.interfaces import IAlchemistContainer, IAlchemistContent
from ore.alchemist.model import queryModelDescriptor
from alchemist.traversal.managed import ManagedContainerDescriptor

import pdb

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
        self.navigation_root_url ='/'

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
    
class NavigationTreeViewlet( viewlet.ViewletBase ):
    """
    render a navigation tree
    
    """ 
    template = ViewPageTemplateFile('contained-constraint-navigation.pt')
        
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.path = []
        self.name  =''
        
    def _get_menu ( self, context ):
        """
        Return the navigation tree as a list of dictionaries:
        name, url, node       
        """
        items = []
        context = proxy.removeSecurityProxy( context )
        
        if context.__parent__ is not None:                    
            url = '../'
            if IAlchemistContent.providedBy(context.__parent__):             
                context_class = context.__parent__.__class__
                context_class = proxy.removeSecurityProxy( context_class )                
                #pdb.set_trace()
                for k, v in context_class.__dict__.items():
                    if isinstance( v, ManagedContainerDescriptor ):                    
                        domain_model = v.domain_container._class 
                        descriptor = queryModelDescriptor( domain_model )
                        if descriptor:
                            name = getattr( descriptor, 'display_name', None)
                        if not name:
                            name = domain_model.__name__
                        current='odd'
                        if domain_model == context._class:
                            current='even'   
                        i = { 'name' : name,
                              'url'  : url + k,
                              'current': current }
                        items.append( i ) 
            self.name = getattr(context.__parent__, 'short_name', None )                                                                              
        return items       
   
   
    def update( self ):
        """
        prepare the data needed to render the viewlet.        
        """
        self.menu = self._get_menu(self.context)    
          
    
    def render( self ):
        return self.template()
        
        
