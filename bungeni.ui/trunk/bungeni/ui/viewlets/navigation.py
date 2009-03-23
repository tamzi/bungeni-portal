# encoding: utf-8

from zope import component
from zope.location.interfaces import ILocation
from zope.dublincore.interfaces import IDCDescriptiveProperties
from zope.security import proxy
from zope.viewlet import viewlet
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.app.component.hooks import getSite
from ore.alchemist.interfaces import IAlchemistContainer, IAlchemistContent
from ore.alchemist.model import queryModelDescriptor
from ore.wsgiapp.interfaces import IApplication
from alchemist.traversal.managed import ManagedContainerDescriptor

from bungeni.ui.utils import getDisplayDate
from bungeni.core.app import BungeniApp
from bungeni.core import location

import datetime
from zope.traversing.browser import absoluteURL 

class GlobalSectionsViewlet(viewlet.ViewletBase):
    render = ViewPageTemplateFile( 'templates/sections.pt' )
    selected_portal_tab = None
    
    def update(self):
        base_url = absoluteURL(getSite(), self.request)
        item_url = self.request.getURL()

        assert item_url.startswith(base_url)
        path = item_url[len(base_url):]

        self.portal_tabs = []
        seen = set()
        menu = component.getUtility(IBrowserMenu, "site_actions")
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
        self.site_url = absoluteURL(getSite(), self.request)
        self.user_name = ''

    def _get_path( self, context):
        """
        Return the current path as a list
        """

        descriptor = None
        name = None 
        path = []

        context = proxy.removeSecurityProxy( context )
        if context.__parent__ is not None:
            path.extend(
                self._get_path(context.__parent__))

        url = absoluteURL(context, self.request)
        
        if  IAlchemistContent.providedBy(context):
            path.append({
                'name' : getattr(context, 'short_name', None ),
                'url' : url})
            
        elif IAlchemistContainer.providedBy(context):                        
            domain_model = context._class 
            try:
                descriptor = queryModelDescriptor( domain_model )
            except:
                descriptor = None
                name = ""                
            if descriptor:
                name = getattr(descriptor, 'container_name', None)
                if name is None:
                    name = getattr(descriptor, 'display_name', None)
            if not name:
                name = getattr( context, '__name__', None)  
            path.append({
                'name' : name,
                'url' : url,
                })

        elif ILocation.providedBy(context) and \
             IDCDescriptiveProperties.providedBy(context):
            path.append({
                'name' : context.title,
                'url' : url,
                })

        return path
        
    def update(self):
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
        self.tree = []
        self.name = ''

    def update(self):
        """Creates a navigation tree for ``context``.

        Recursively, by visiting the parent chain in reverse order,
        the tree is built. The siblings of managed containers are
        included.
        """

        chain = []
        context = proxy.removeSecurityProxy(self.context)

        while context is not None:
            chain.append(context)
            context = context.__parent__

        self.nodes = self.expand(chain)

    def expand(self, chain):
        if len(chain) == 0:
            return ()
        
        context = chain.pop()
        items = []

        if IApplication.providedBy(context):
            items.extend(self.expand(chain))

        elif IAlchemistContent.providedBy(context):
            url = absoluteURL(context, self.request)
            items.append(
                {'title': context.short_name,
                 'url': url,
                 'current': True,
                 'selected': len(chain) == 0,
                 'kind': 'content',
                 'nodes': self.expand(chain),
                 })

        elif IAlchemistContainer.providedBy(context):
            # loop through all managed containers of the parent
            # object, and include the present container as the
            # 'current' node.
            parent = context.__parent__
            assert parent is not None
            url = absoluteURL(parent, self.request)

            # append managed containers as child nodes
            kls = type(proxy.removeSecurityProxy(parent))

            if IApplication.providedBy(parent):
                containers = [
                    (name, parent[name])
                    for name in location.model_to_container_name_mapping.values()
                    if name in parent]
            else:
                containers = [
                    (key, getattr(parent, key))
                    for key, value in kls.__dict__.items()
                    if isinstance(value, ManagedContainerDescriptor)]

            seen_context = False
            
            for key, container in containers:
                descriptor = queryModelDescriptor(container.domain_model)
                if descriptor:
                    name = getattr(descriptor, 'container_name', None)
                    if name is None:
                        name = getattr(descriptor, 'display_name', None)

                if not name:
                    name = container.domain_model.__name__

                current = container.__name__ == context.__name__
                selected = len(chain) == 0 and current
                
                if current:
                    seen_context = True
                    nodes = self.expand(chain)
                else:
                    nodes = ()
                
                items.append(
                    {'title': name,
                     'url': "%s/%s" % (url.rstrip('/'), key),
                     'current': current,
                     'selected': selected,
                     'kind': 'container',
                     'nodes': nodes,
                     })

            if not seen_context:
                import pdb; pdb.set_trace()
                
        elif ILocation.providedBy(context):
            url = absoluteURL(context, self.request)
            props = IDCDescriptiveProperties.providedBy(context) and \
                context or IDCDescriptiveProperties(context)

            props = proxy.removeSecurityProxy(props)

            items.append(
                {'title': props.title,
                 'url': url,
                 'current': True,
                 'selected': len(chain) == 0,
                 'kind': 'location',
                 'nodes': self.expand(chain),
                 })

        return items
