# encoding: utf-8

from zope.viewlet import viewlet
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.interface.verify import verifyObject
from zope.security import proxy

from ore.alchemist.interfaces import IAlchemistContainer, IAlchemistContent
from ore.alchemist.model import queryModelDescriptor
from alchemist.traversal.managed import ManagedContainerDescriptor
from bungeni.core.app import BungeniApp

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
        self.tree = []
        

   
    def _get_object_path(self, context, url=''):
        """
        traverse up the tree 
        """
        path = []
        context = proxy.removeSecurityProxy( context )
        if context.__parent__ is not None:            
            path = path + self._get_object_path(context.__parent__, '../' + url )     
        else:            
            return []
        path.append({'obj':context, 'url':url})            
        return path
   
   
        
        
    def _append_child( self, path):
        """
        build the navigation tree
        """
        items = []
        url = path[0]['url']
        if IAlchemistContent.providedBy(path[0]['obj']):                     
            item = {'name' : getattr(path[0]['obj'], 'short_name', None ), 'url' : url, 'current': 'navTreeCurrentNode'}
            if len(path) > 1:
                item['node'] = self._append_child(path[1:])
            else: 
                # leaf => append actions
                item['current'] = 'navTreeCurrentItem'                                        
                context_class = path[0]['obj'].__class__
                context_class = proxy.removeSecurityProxy( context_class )    
                
                citems =[]
                for k, v in context_class.__dict__.items():
                    if isinstance( v, ManagedContainerDescriptor ):
                        domain_model = v.domain_container._class 
                        descriptor = queryModelDescriptor( domain_model )
                        if descriptor:
                            name = getattr( descriptor, 'display_name', None)
                        if not name:
                            name = domain_model.__name__
                            
                        i = { 'name' : name,
                              'current' : '',
                              'url'  :  k, 
                              'node' : None}
                        citems.append( i )
                item['node'] = citems
            items.append(item)
        if IAlchemistContainer.providedBy(path[0]['obj']):                        
            if (path[0]['obj'].__parent__ is None) or (path[0]['obj'].__parent__.__class__ == BungeniApp): 
                #Navigation Root               
                domain_model = path[0]['obj']._class 
                descriptor = queryModelDescriptor( domain_model )
                if descriptor:
                    name = getattr( descriptor, 'display_name', None)
                if not name:
                    name = getattr( domain_model, '__name__', None) 
                item = { 'name' : name,
                            'url'  : url ,
                            'current': 'navTreeCurrentNode', 
                             } 
                if len(path) > 1:
                    item['node'] = self._append_child(path[1:])
                else:
                    item['node'] = None
                items.append(item)                     
                return items

                         
            context_class = path[0]['obj'].__parent__.__class__
            context_class = proxy.removeSecurityProxy( context_class )                
            for k, v in context_class.__dict__.items():
                if isinstance( v, ManagedContainerDescriptor ):
                    domain_model = v.domain_container._class 
                    descriptor = queryModelDescriptor( domain_model )                    
                    if descriptor:
                        name = getattr( descriptor, 'display_name', None)
                    if not name:
                        name = domain_model.__name__
                    if domain_model == path[0]['obj']._class:   
                        item = { 'name' : name,
                            'url'  : url + '../' + k,
                            'current': 'navTreeCurrentNode', 
                             }
                        if len(path) > 1:
                            item['node'] = self._append_child(path[1:])
                        else:
                            item['node'] = None
                            #item['current'] = 'navTreeCurrentItem' 
                    else:                            
                        item = { 'name' : name,
                              'current' : '',
                              'node' : None,
                              'url'  : url + '../' + k }
                    items.append( item )  
        return items                                          
            
    def _tree2html(self, items):
        htmlstr = '<ul class="navTree">'
        for item in items:
            htmlstr = htmlstr + '<li class="navTreeItem ' + item['current'] +'" >'
            htmlstr = htmlstr + '<div><a href="' + item['url'] + '"' + ' class="'  + item['current'] +'" >'
            htmlstr = htmlstr + str( item['name'] )   
            htmlstr = htmlstr + '</a></div>'
           
            if item['node']:
                htmlstr = htmlstr + self._tree2html(item['node']) 
            htmlstr = htmlstr +  '</li>'           
        htmlstr = htmlstr +  '</ul>'
        return htmlstr
                    
    def _get_tree ( self, context, url = ''):
        items = []
        path = self._get_object_path(context)
        items = self._append_child( path)
        return self._tree2html(items)
        
       
        
        
    
    def update( self ):
        """
        prepare the data needed to render the viewlet.        
        """       
        self.tree = self._get_tree(self.context)  
    
    
    def render( self ):
        return str(self.tree)
        

        
