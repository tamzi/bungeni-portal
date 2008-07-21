
from z3c.menu.ready2go import item
from zope import component
from zope.app.component.hooks import getSite
from zope.app.security.interfaces import IUnauthenticatedPrincipal
from zope.app.publisher.browser.menu import BrowserMenu

class GlobalMenuItem( item.GlobalMenuItem ):
    #cssActive = "menubarSelected"
    #cssInactive = "menubar"
    #css = "menubar"
    pass
    
class LoginAction( GlobalMenuItem ):
    
    @property
    def available( self ):
        available = IUnauthenticatedPrincipal.providedBy( self.request.principal )
        return available

class LogoutAction( GlobalMenuItem ):
    
    @property
    def available( self ):
        authenticated = not IUnauthenticatedPrincipal.providedBy( self.request.principal )
        return authenticated
        
class DashboardAction( GlobalMenuItem ):
    
    @property
    def title( self ):
        return self.request.principal.id
        
    @property
    def available( self ):
        authenticated = not IUnauthenticatedPrincipal.providedBy( self.request.principal )
        return authenticated

class AdminAction( GlobalMenuItem ):
    
    def getURLContext( self ):
        site = getSite()
        return site['admin']

class TaskMenu(BrowserMenu):
    def getMenuItems(self, object, request):
        spec = self.getMenuItemType()
        return [item for name, item in \
                component.getAdapters((object, request), spec)]
    
# 
# class TaskMenu( managr.MenuManager ):
#     
#     def update(self):
#         """See zope.contentprovider.interfaces.IContentProvider"""
#         self.__updated = True
# 
#         viewlets = self._getViewlets()
#             
#         viewlets = self.filter(viewlets)
#         viewlets = self.sort(viewlets)
#         # Just use the viewlets from now on
#         self.viewlets=[]
#         for name, viewlet in viewlets:
#             if ILocation.providedBy(viewlet):
#                 viewlet.__name__ = name
#             self.viewlets.append(viewlet)
#         self._updateViewlets()
# 
#     def _getViewlets( self ):
#         interaction = getInteraction()
#         # Find all content providers for the region
#         viewlets = component.getAdapters(
#             (self.context, self.request, self.__parent__, self),
#             interfaces.IViewlet)
        
