"""
zope3 authenticator plugin against a relational database
"""

from zope import interface
from zope.app.authentication import interfaces
from zope.app.container.contained import Contained

from ore.alchemist import Session

from domain import User

class PrincipalInfo( object ):

    interface.implements(interfaces.IPrincipalInfo)
    
    def __init__(self, id, login, title, description, auth_plugin=None):
        self.id = id
        self.login = login
        self.title = title
        self.description = description
        self.authenticatorPlugin = auth_plugin
        
    def __repr__(self):
        return 'PrincipalInfo(%r)' % self.id

class DatabaseAuthentication( Contained ):
    
    interface.implements( interfaces.IAuthenticatorPlugin )

    def authenticateCredentials( self, credentials ):
        if not credentials:
            return None
        login, password = credentials.get('login'), credentials.get('password')
        results = Session().query( User ).filter_by( username = unicode(login) ).all()

        if len(results) != 1:
            return None

        user = results[0]
        if not user.checkPassword( password ):
            return None

        return self._makeInfo( user )
        
    def principalInfo( self, id ):
        results = Session().query( User ).filter_by( username = id ).all()
        if len(results) != 1: # unique index on column
            return None

        user = results[0]
        return self._makeInfo( user )

    def _makeInfo( self, user ):

        return PrincipalInfo( "users.%s"%user.username, # userid
                              user.username,            # login
                              user.username,            # title
                              user.email_address,       # description
                              self                      # auth plugin
                              )
        
        
    def __repr__(self):
        return "<DatabaseAuthPlugin>"
