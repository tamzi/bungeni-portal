
from z3c.menu.ready2go import item, manager
from zope import interface, component
from zope.location.interfaces import ILocation
from zope.viewlet import interfaces
from zope.security.management import getInteraction
from zope.app.security.interfaces import IUnauthenticatedPrincipal

class LoginAction( item.SiteMenuItem ):
    
    @property
    def available( self ):
        available = IUnauthenticatedPrincipal.providedBy( self.request.principal )
        return available
        
class LogoutAction( item.SiteMenuItem ):
    
    @property
    def available( self ):
        authenticated = not IUnauthenticatedPrincipal.providedBy( self.request.principal )
        return authenticated
        
class DashboardAction( item.SiteMenuItem ):
    
    @property
    def title( self ):
        return self.request.principal.id
        
    @property
    def available( self ):
        authenticated = not IUnauthenticatedPrincipal.providedBy( self.request.principal )
        return authenticated

class AdminAction( item.SiteMenuItem ):
    
    def getURLContext( self ):
        site = getSite()
        return site['admin']
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
        