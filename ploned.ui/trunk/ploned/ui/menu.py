"""
$Id: $

replacement of the default menu implementation for our global tabs, since
we ran into issues on traversability checks done when we're doing site relative
addressing in these tabs.

---
Kapil Thangavelu 

"""


import zope.component

from zope.security.proxy import removeSecurityProxy
from zope.interface import providedBy, Interface
from zope.app.publisher.interfaces.browser import IBrowserSubMenuItem
from zope.app.publisher.browser.menu import BrowserMenu, getMenu
from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.app.component.hooks import getSite
from zope.traversing.browser import absoluteURL
from zope.app.pagetemplate import ViewPageTemplateFile

from ploned.ui.interfaces import IViewView

def is_selected(item, action, request_url):
    normalized_action = action.lstrip('.').lstrip('@@')
    index = request_url.rfind(normalized_action)
    if index == -1:
        return False
    return index

def action_to_id(action):
    return action.\
           strip('/').\
           replace('/', '-').\
           replace('.', '').\
           strip('-')

def make_absolute(action, local_url, site_url):
    if action.startswith('http://') or action.startswith('https://'):
        return action
    if action.startswith('.'):
        return "%s/%s" % (local_url, action[1:].lstrip('/'))
    if action.startswith('/'):
        return "%s/%s" % (site_url, action[1:])
    return "%s/%s" % (local_url, action)
    
class PloneBrowserMenu(BrowserMenu):
    """This menu class implements the ``getMenuItems`` to conform with
    Plone templates."""
    
    def getMenuItems(self, object, request):
        menu = tuple(zope.component.getAdapters(
            (object, request), self.getMenuItemType()))
        result = [item for name, item in menu]

        # Now order the result. This is not as easy as it seems.
        #
        # (1) Look at the interfaces and put the more specific menu entries
        #     to the front. 
        # (2) Sort unambigious entries by order and then by title.
        ifaces = list(providedBy(removeSecurityProxy(object)).__iro__)
        max_key = len(ifaces)
        def iface_index(item):
            iface = item._for
            if not iface:
                iface = Interface
            if zope.interface.interfaces.IInterface.providedBy(iface):
                return ifaces.index(iface)
            if isinstance(removeSecurityProxy(object), item._for):
                # directly specified for class, this goes first.
                return -1
            # no idea. This goes last.
            return max_key
        result = [(item.order, iface_index(item), item.title, item)
                  for item in result]
        result.sort()

        local_url = absoluteURL(object, request)
        site_url = absoluteURL(getSite(), request)
        request_url = request.getURL()

        items = []
        selected = None
        current_pos = -1

        for index, (order, iface_index, title, item) in enumerate(result):
            extra = item.extra or {'id': action_to_id(item.action)}
            if IBrowserSubMenuItem.providedBy(item):
                submenu = getMenu(item.submenuId, object, request)
            else:
                submenu = None
                extra['hideChildren'] = True

            url = make_absolute(item.action, local_url, site_url)
            
            if submenu:
                for menu in submenu:
                    menu['url'] = make_absolute(
                        menu['action'], local_url, site_url)

            pos = is_selected(item, item.action, request_url)
            if pos > current_pos:
                current_pos = pos
                selected = index

            items.append({
                'title': title,
                'description': item.description,
                'action': item.action,
                'url': url,
                'selected': u'',
                'icon': item.icon,
                'extra': extra,
                'submenu': submenu})

        if selected is not None:
            items[selected]['selected'] = u'selected'

        return items
    
class ContentMenuProvider(object):
    """Content menu."""
    
    def __init__(self, context, request, view):
        self.__parent__ = view
        self.view = view
        self.context = context
        self.request = request

    def update(self):
        pass

    render = ViewPageTemplateFile('templates/contentmenu.pt')

    def available(self):
        return IViewView.providedBy(self.view)

    def menu(self):
        menu = zope.component.getUtility(IBrowserMenu, name='plone_contentmenu')
        items = menu.getMenuItems(self.context, self.request)
        items.reverse()
        return items
