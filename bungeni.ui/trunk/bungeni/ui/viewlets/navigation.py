# encoding: utf-8

from zope import component
from zope.security import proxy
from zope.viewlet import viewlet
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.app.component.hooks import getSite
from ore.alchemist.interfaces import IAlchemistContainer, IAlchemistContent
from ore.alchemist.model import queryModelDescriptor
from alchemist.traversal.managed import ManagedContainerDescriptor

from bungeni.ui.utils import getDisplayDate
from bungeni.core.app import BungeniApp

import datetime
from zope.traversing.browser import absoluteURL 

class GlobalSectionsViewlet(viewlet.ViewletBase):
    render = ViewPageTemplateFile( 'templates/sections.pt' )
    selected_portal_tab = None
    
    def update(self):
        base_url = absoluteURL(getSite(), self.request)
        path = self.request['PATH_INFO']
        menu = component.getUtility(IBrowserMenu, "site_actions")
        
        self.portal_tabs = []
        seen = set()
        for item in menu.getMenuItems(self.context, self.request):
            if item['action'] in seen:
                continue
            seen.add(item['action'])
            item['url'] = item.setdefault('url', base_url + item['action'])
            item['id'] = item['action'].strip('/')
            item['name'] = item['title']
            self.portal_tabs.append(item)
            if path.startswith(item['action']):
                self.selected_portal_tab = item['id']
        
class BreadCrumbsViewlet(viewlet.ViewletBase):
    """Breadcrumbs.
    
    Render the breadcrumbs to show a user his current location.
    """

    render = ViewPageTemplateFile( 'templates/breadcrumbs.pt' )        

    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.path = []
        self.navigation_root_url ='/'
        self.user_name = ''

    def _get_path( self, context, url = '' ): 
        """
        Return the current path as a list
        """
        descriptor = None
        name = None 
        path = []
        context = proxy.removeSecurityProxy( context )
        if context.__parent__ is not None:            
            path = path + self._get_path(context.__parent__, '../' + url )
        #if context != self.context:           
        if  IAlchemistContent.providedBy(context):
            path.append( {'name' : getattr(context, 'short_name', None ), 'url' : url})
        if IAlchemistContainer.providedBy(context):                        
            domain_model = context._class 
            try:
                descriptor = queryModelDescriptor( domain_model )
            except:
                descriptor = None
                name = ""                
            if descriptor:
                name = getattr( descriptor, 'display_name', None)
            if not name:
                name = getattr( context, '__name__', None)  
            path.append({'name' : name, 'url' : url} )                         
        return path
        
    def update( self ):
        self.path = self._get_path(self.context)    
        try:
            self.user_name = self.request.principal.login          
        except:
            pass
        
class NavigationTreeViewlet( viewlet.ViewletBase ):
    """Render a navigation tree."""

    render = ViewPageTemplateFile( 'templates/bungeni-navigation-tree.pt' )
    template = ViewPageTemplateFile('templates/contained-constraint-navigation.pt')

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
            url = absoluteURL( context, self.request ) + '/'
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
        if len(path) == 0:
            return items
        url = path[0]['url']
        if IAlchemistContent.providedBy(path[0]['obj']):                     
            item = {'name' : getattr(path[0]['obj'], 'short_name', None ), 'url' : url, 'current': 'navTreeItemInPath'}
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
                              'node' : None,
                              'script': True }                                          
                        if domain_model == context_class: 
                            i['current'] = 'navTreeCurrentItem'                              
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
                            'current': 'navTreeItemInPath', 
                            'script': False,
                             } 
                if len(path) > 1:
                    item['node'] = self._append_child(path[1:])
                else:
                    item['node'] = None
                    item['current'] = 'navTreeCurrentItem'
                items.append(item)                     
                return items

                         
            context_class = path[0]['obj'].__parent__.__class__
            context_class = proxy.removeSecurityProxy( context_class )                
            for k, v in context_class.__dict__.items():
                if isinstance( v, ManagedContainerDescriptor ):
                    domain_model = v.domain_container._class 
                    descriptor = queryModelDescriptor( domain_model )                    
                    if len(path) == 1:
                        current = 'navTreeItemInPath'
                    else:
                        current = 'navTreeCurrentItem'
                    if descriptor:
                        name = getattr( descriptor, 'display_name', None)
                    if not name:
                        name = domain_model.__name__
                    if domain_model == path[0]['obj']._class:   
                        item = { 'name' : name,
                            'url'  : url + '../' + k,
                            'current': 'navTreeItemInPath', 
                            'script': False,
                             }
                        if len(path) > 1:
                            item['node'] = self._append_child(path[1:])
                        else:
                            item['node'] = None
                            item['current'] = 'navTreeCurrentItem' 
                    else:                            
                        item = { 'name' : name,
                              'current' : '',
                              'node' : None,
                              'url'  : url + '../' + k,
                              'script': False, }
                    items.append( item )  
        return items                                          

    def _appendSortFilter2URL(self, url):
        """
        get the filters from url and add them if applicable        
        """
        filter_by = ''
        displayDate = getDisplayDate(self.request)        
        if displayDate:
            filter_by='?date=' + datetime.date.strftime(displayDate,'%Y-%m-%d')
            return url + filter_by               
        else:
            return url                    

            
    def _tree2html(self, items, level = 0):
        #level = level +1
        if level >= 0:
            htmlstr = '<ul class="navTree navTreeLevel' + str(level) + '">'
        else:
            #if item['script']:
            #    htmlstr = '<noscript>'
            #else:                
            htmlstr = '' 
        for item in items:
            htmlstr = htmlstr + '<li class="navTreeItem ' + item['current'] +'" >'
            htmlstr = htmlstr + '<div><a href="' + self._appendSortFilter2URL(item['url']) + '"' + ' class="'  + item['current'] +'" >'
            htmlstr = htmlstr + str( item['name'] )   
            htmlstr = htmlstr + '</a></div>'           
            if item['node']:
                htmlstr = htmlstr + self._tree2html(item['node'], level + 1) 
            htmlstr = htmlstr +  '</li>'           
        if level >= 0:
            htmlstr = htmlstr +  '</ul>'
        return htmlstr
                    
    def _get_tree ( self, context, url = ''):
        items = []
        path = self._get_object_path(context)
        items = self._append_child( path)
        return self._tree2html(items)
               
    def update(self):
        self.tree = self._get_tree(self.context)  
