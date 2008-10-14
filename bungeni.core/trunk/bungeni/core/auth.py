"""
zope3 authenticator plugin against a relational database
"""

from zope import interface, component
from domain import User
from alchemist.security.interfaces import IAlchemistUser, IAlchemistAuth
from wc.cookiecredentials.plugin import CookieCredentialsPlugin

from zope.app.authentication.interfaces import IAuthenticatorPlugin
from zope.app.security.interfaces import IAuthentication, PrincipalLookupError
from zope.app.authentication.principalfolder import PrincipalInfo
from zope.app.authentication.interfaces import IFoundPrincipalFactory, IAuthenticatorPlugin, IAuthenticatedPrincipalFactory

import zope.app.authentication.authentication

@interface.implementer( IAlchemistUser )
@component.adapter( IAlchemistAuth )
def authUser( util ):
    return User


class CookieCredentials( CookieCredentialsPlugin ):

    loginpagename = 'login'


class PluggableAuthentication( zope.app.authentication.authentication.PluggableAuthentication ):
    """
    id prefix mangling 
    """
    def getPrincipal( self, id ):
        if not id.startswith(self.prefix):
            next = component.queryNextUtility( None, IAuthentication)
            if next is None:
                raise PrincipalLookupError(id)
            return next.getPrincipal(id)
        id = id[len(self.prefix):]
        for name, authplugin in self.getAuthenticatorPlugins():
            info = authplugin.principalInfo(id)
            if info is None:
                continue
            info.credentialsPlugin = None
            info.authenticatorPlugin = authplugin
            principal = IFoundPrincipalFactory(info)(self)
            principal.id = self.prefix + info.id
            return principal
        next = component.queryNextUtility(self, IAuthentication)
        if next is not None:
            return next.getPrincipal(self.prefix + id)
        raise PrincipalLookupError(id)

    def authenticate(self, request):
        
        authenticatorPlugins = [p for n, p in self.getAuthenticatorPlugins()]
        for name, credplugin in self.getCredentialsPlugins():
            credentials = credplugin.extractCredentials(request)
            for authplugin in authenticatorPlugins:
                if authplugin is None:
                    continue
                info = authplugin.authenticateCredentials(credentials)
                if info is None:
                    continue
                info.credentialsPlugin = credplugin
                info.authenticatorPlugin = authplugin
                principal = component.getMultiAdapter((info, request),
                    IAuthenticatedPrincipalFactory)(self)
                
                if '.' in info.id:
                    principal.id = info.id
                    return principal
                principal.id = self.prefix + info.id
                return principal
        return None
    

class GlobalAuthDelegate( object ):
    """
    we where having some issues authenticating with users defined in zcml, tracing it down
    appeared to be an issue in doing lookups for authentication plugins properly. this authenticator
    plugin is usedin the pft application as a local site component, and in turn delegates authentication
    to the implementation in the global root.
    """

    interface.implements( IAuthenticatorPlugin )
    
    def authenticateCredentials( self, credentials ):
        if not isinstance( credentials, dict ):
            return None
        
        if ( not 'login' in credentials ) or \
           ( not 'password' in credentials ):
            return
        site = component.getGlobalSiteManager()
        root_auth = site.queryUtility( IAuthentication )
        try:
            principal = root_auth.getPrincipalByLogin( credentials['login']  )
        except PrincipalLookupError:
            return None
        if principal.validate( credentials['password'] ):
            info = PrincipalInfo( principal.id, principal.getLogin(), principal.title, "")
            return info
        
    def principalInfo( self, id ):
        prefix, name = id.split('.')
        return PrincipalInfo( id, name, name.upper(), "")

    
