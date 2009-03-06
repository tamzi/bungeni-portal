"""
``repoze.who`` authenticator plugins against a relational database
"""

from zope import interface
from zope.app.security.principalregistry import principalRegistry
from zope.app.security.interfaces import PrincipalLookupError

from repoze.who.interfaces import IAuthenticator
from repoze.who.interfaces import IMetadataProvider

from ore.alchemist import Session
from sqlalchemy.exceptions import UnboundExecutionError

from bungeni.models.domain import User

import logging
log = logging.getLogger("bungeni.portal")

class AlchemistWhoPlugin(object):
    interface.implements(IAuthenticator, IMetadataProvider)
    
    def authenticate(self, environ, identity):
        if not ('login' in identity and 'password' in identity):
            return None
        
        user = self.get_user(identity['login'])

        if user and user.checkPassword(identity['password']):
            return identity['login']
            
    def get_user(self, login):
        try:
            session = Session()
        except UnboundExecutionError, e:
            log.warn(e)
            return
        
        results = session.query(User).filter_by(login=unicode(login)).all()

        if len(results) != 1:
            return None

        return results[0]

    def add_metadata(self, environ, identity):
        userid = identity.get('repoze.who.userid')
        user = self.get_user(userid)

        if user is not None:
            identity.update({
                'email': user.email,
                'title': u"%s, %s" % (user.last_name, user.first_name)
                })

class GlobalAuthWhoPlugin(object):
    interface.implements(IAuthenticator, IMetadataProvider)
    
    def authenticate(self, environ, identity):
        if not ('login' in identity and 'password' in identity):
            return None

        principal = self.get_principal_by_login(identity['login'])
        if principal and principal.validate(identity['password']):
            return identity['login']

    def get_principal(self, id):
        try:
            return principalRegistry.getPrincipal(id)
        except PrincipalLookupError:
            pass
        except KeyError:
            pass

    def get_principal_by_login(self, login):
        try:
            return principalRegistry.getPrincipalByLogin(login)
        except PrincipalLookupError:
            pass
        except KeyError:
            pass

    def add_metadata(self, environ, identity):
        login = identity.get('repoze.who.userid')
        principal = self.get_principal_by_login(login)

        if principal is not None:
            identity.update({
                'title': principal.title,
                'groups': tuple(principal.groups) + (principal.id,),
                })
