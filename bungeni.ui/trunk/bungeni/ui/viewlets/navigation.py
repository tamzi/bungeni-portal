# encoding: utf-8

from zope import interface
from zope import component
from zope.location.interfaces import ILocation
from zope.dublincore.interfaces import IDCDescriptiveProperties
from zope.container.interfaces import IReadContainer
from zope.security import proxy
from zope.proxy import sameProxiedObjects
from zope.viewlet import viewlet
from zope.app.component.hooks import getSite
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.app.component.hooks import getSite
from ore.alchemist.interfaces import IAlchemistContainer, IAlchemistContent
from ore.alchemist.model import queryModelDescriptor
from ore.wsgiapp.interfaces import IApplication
from alchemist.traversal.managed import ManagedContainerDescriptor
from zope.publisher.interfaces import IDefaultViewName
from zope.app.publisher.browser import queryDefaultViewName

from ploned.ui.menu import make_absolute
from ploned.ui.menu import is_selected
from ploned.ui.interfaces import IStructuralView

from bungeni.ui.utils import getDisplayDate
from bungeni.core.app import BungeniApp
from bungeni.core import location

import datetime
from zope.traversing.browser import absoluteURL 

def get_parent_chain(context):
    context = proxy.removeSecurityProxy(context)

    chain = []
    while context is not None:
        chain.append(context)
        context = context.__parent__

    return chain

class SecondaryNavigationViewlet(object):
    render = ViewPageTemplateFile("templates/secondary-navigation.pt")

    def update(self):
        chain = get_parent_chain(self.context)
        length = len(chain)
        if length < 2:
            return

        container = chain[-2]
        assert container.__name__ is not None

        if length > 2:
            context = chain[-3]
        else:
            context = None
            
        url = absoluteURL(container, self.request)
        self.items = items = self.get_menu_items(
            container, "%s_navigation" % container.__name__)
        
        for name, item in container.items():
            if context is None:
                selected = False
            else:
                selected = context.__name__ == name

            if IDCDescriptiveProperties.providedBy(item):
                title = item.title
            else:
                props = IDCDescriptiveProperties(item)
                title = props.title

            items.append({
                'title': title,
                'selected': selected,
                'url': "%s/%s" % (url, name)})

        default_view_name = queryDefaultViewName(container, self.request)
        default_view = component.getMultiAdapter(
            (container, self.request), name=default_view_name)

        if hasattr(default_view, "title"):
            items.insert(0, {
                'title': default_view.title,
                'selected': sameProxiedObjects(container, self.context),
                'url': url})

    def get_menu_items(self, container, name):
        menu = component.getUtility(IBrowserMenu, name=name)
        items = menu.getMenuItems(container, self.request)

        local_url = absoluteURL(container, self.request)
        site_url = absoluteURL(getSite(), self.request)
        request_url = self.request.getURL()

        default_view_name = queryDefaultViewName(container, self.request)

        for item in items:
            action = item['action']

            if default_view_name == action.lstrip('@@'):
                url = local_url
                selected = sameProxiedObjects(container, self.context)
            else:
                url = make_absolute(action, local_url, site_url)
                selected = is_selected(
                    item, action, request_url)
                
            item['url'] = url
            item['selected'] = selected and u'selected' or u''

        return items

class WorkspaceNavigationViewlet(SecondaryNavigationViewlet):
    def __init__(self, context, request, view, manager):
        if IStructuralView.providedBy(view):
            context = context.__parent__
        super(WorkspaceNavigationViewlet, self).__init__(
            context, request, view, manager)
    
    def update(self):
        self.items = self.get_menu_items(self.context, 'workspace_navigation')

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

    def _get_path(self, context):
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
            if IDCDescriptiveProperties.providedBy(context):
                title = context.title
            else:
                props = IDCDescriptiveProperties(context, None)
                if props is not None:
                    title = props.title
                else:
                    title = context.short_name
                    
            path.append({
                'name' : title,
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

        # if the view is a location, append this to the breadcrumbs
        if ILocation.providedBy(self.__parent__) and \
               IDCDescriptiveProperties.providedBy(self.__parent__):
            self.path.append({
                'name': self.__parent__.title,
                'url': None,
                })

        try:
            self.user_name = self.request.principal.login          
        except:
            pass
        
class NavigationTreeViewlet( viewlet.ViewletBase ):
    """Render a navigation tree."""

    render = ViewPageTemplateFile( 'templates/bungeni-navigation-tree.pt' )
    template = ViewPageTemplateFile('templates/contained-constraint-navigation.pt')
    path = ()
    
    def __init__(self, context, request, view, manager):
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.name = ''

    def update(self):
        """Creates a navigation tree for ``context``.

        Recursively, by visiting the parent chain in reverse order,
        the tree is built. The siblings of managed containers are
        included.
        """

        chain = get_parent_chain(self.context)
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
            if IDCDescriptiveProperties.providedBy(context):
                title = context.title
            else:
                props = IDCDescriptiveProperties(context, None)
                if props is not None:
                    title = props.title
                else:
                    title = context.short_name

            selected = len(chain) == 0
            
            if chain:
                nodes = self.expand(chain)
            else:
                kls = context.__class__
                containers = [
                    (key, getattr(context, key))
                    for key, value in kls.__dict__.items()
                    if isinstance(value, ManagedContainerDescriptor)]
                nodes = []
                self.expand_containers(nodes, containers, url, chain, None)

            items.append(
                {'title': title,
                 'url': url,
                 'current': True,
                 'selected': selected,
                 'kind': 'content',
                 'nodes': nodes,
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
            elif IReadContainer.providedBy(parent):
                containers = list(parent.items())
            else:
                containers = [
                    (key, getattr(parent, key))
                    for key, value in kls.__dict__.items()
                    if isinstance(value, ManagedContainerDescriptor)]

            self.expand_containers(items, containers, url, chain, context)

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

        elif IReadContainer.providedBy(context):
            items.extend(self.expand(chain))

        return items

    def expand_containers(self, items, containers, url, chain=(), context=None):
        seen_context = False
        current = False
        
        for key, container in containers:
            if IAlchemistContainer.providedBy(container):
                descriptor = queryModelDescriptor(
                    proxy.removeSecurityProxy(container).domain_model)
                if descriptor:
                    name = getattr(descriptor, 'container_name', None)
                    if name is None:
                        name = getattr(descriptor, 'display_name', None)
                        
                if not name:
                    name = container.domain_model.__name__
            else:
                assert IDCDescriptiveProperties.providedBy(container)
                name = container.title

            if context is not None:
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
