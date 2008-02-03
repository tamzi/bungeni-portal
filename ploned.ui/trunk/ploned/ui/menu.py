"""
$Id: $

replacement of the default menu implementation for our global tabs, since
we ran into issues on traversability checks done when we're doing site relative
addressing in these tabs.

---
Kapil Thangavelu 

"""


import zope.component
import zope.interface.interfaces

from zope.security.proxy import removeSecurityProxy
from zope.interface import providedBy, Interface
from zope.app.publisher.interfaces.browser import IBrowserSubMenuItem
from zope.app.publisher.browser.menu import BrowserMenu, getMenu

class AppSectionsMenu( BrowserMenu ):


    def getMenuItems( self, object, request ):

        result = []
        for name, item in zope.component.getAdapters((object, request),
                                                     self.getMenuItemType()):
            #if item.available():
            result.append(item)

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
        result = [(iface_index(item), item.order, item.title, item)
                  for item in result]
        result.sort()

        result = [
            {'title': title,
             'description': item.description,
             'action': item.action,
             'selected': (self.selected(item) and u'selected') or u'',
             'icon': item.icon,
             'extra': item.extra,
             'submenu': (IBrowserSubMenuItem.providedBy(item) and
                         getMenu(item.submenuId, object, request)) or None}
            for index, order, title, item in result]

        return result
        
    def selected( self, item ):
        request_url = item.request.getURL()

        normalized_action = item.action

        # hack hardcode home action..
        if item.title == 'Home' and request_url.count('/') != 3:
            return False
        
        if normalized_action in request_url:
            return True
        if request_url.endswith( normalized_action ):
            return True
        if request_url.endswith('/'+normalized_action):
            return True
        if request_url.endswith('/++view++'+normalized_action):
            return True
        if request_url.endswith('/@@'+normalized_action):
            return True

        return False
