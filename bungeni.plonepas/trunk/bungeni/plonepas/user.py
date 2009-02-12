
import random, md5, string

from AccessControl import ClassSecurityInfo
from AccessControl.SecurityManagement import getSecurityManager
from Globals import InitializeClass

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements

from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserAdderPlugin

from Products.PlonePAS.interfaces.plugins import IUserManagement
from Products.PlonePAS.interfaces.capabilities import IDeleteCapability
from Products.PlonePAS.interfaces.capabilities import IPasswordSetCapability

from Products.PluggableAuthService.permissions import ManageUsers
from Products.PluggableAuthService.permissions import SetOwnPassword

from Products.PageTemplates.PageTemplateFile import PageTemplateFile

import sqlalchemy as rdb
import schema

manage_addBungeniUserManagerForm = PageTemplateFile('zmi/user-plugin-add.pt', globals())

def manage_addBungeniUserManager(self, id, title='', REQUEST=None):
    """Add a BungeniUserManager to a Pluggable Auth Service."""
    um = UserManager(id, title )
    self._setObject(um.getId(), um)
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(
                                '%s/manage_workspace'
                                '?manage_tabs_message='
                                'BungeiUserManager+added.'
                            % self.absolute_url())

def generate_salt( ):
    return ''.join( random.sample( string.letters, 12 ) )

def encrypt( word, salt ):
    return md5.md5( word + salt).hexdigest()

def safeencode(v):
    if isinstance(v, unicode):
        return v.encode('utf-8')
    return v

class UserManager( BasePlugin ):

    meta_type = 'Bungeni User Manager'
    security = ClassSecurityInfo()

    def __init__(self, id, title=None):
        self.id = self.id = id
        self.title = title    

    security.declarePrivate('invalidateCacheForChangedUser')
    def invalidateCacheForChangedUser(self, user_id):
        pass

    #
    # IUserManagement implementation
    #

    security.declarePrivate('doChangeUser')
    def doChangeUser(self, login, password, **kw):
        # userSetPassword in PlonePAS expects a RuntimeError when a plugin doesn't hold the user.
        try:
            self.updateUserPassword(login, login, password)            
        except KeyError:
            raise RuntimeError, "User does not exist: %s"%login


    security.declarePrivate('doDeleteUser')
    def doDeleteUser(self, login):
        try:
            self.removeUser(login)
        except KeyError:
            return False
        return True
    
    #
    # IDeleteCapability implementation
    #

    def allowDeletePrincipal(self, id):
        return self._uid( id ) is not None


    #
    # IPasswordSetCapability implementation
    #
    def allowPasswordSet(self, id):
        return self._uid( id ) is not None

    #
    # IAuthenticationPlugin implementation
    #

    security.declarePrivate('authenticateCredentials')
    def authenticateCredentials(self, credentials):
        login = credentials.get('login')
        password = credentials.get('password')
        if not login or not password: return None
        
        res = self._uid( login, auth=True )
        if not res: return None
        
        if encrypt( password, res['salt'] ) == res['password']:
            return login, login
        return None
        
    #
    # IUserEnumerationPlugin implementation
    #
    security.declarePrivate('enumerateUsers')
    def enumerateUsers( self
                      , id=None
                      , login=None
                      , exact_match=False
                      , sort_by=None
                      , max_results=None
                      , **kw
                      ):
        """See IUserEnumerationPlugin.
        """
        if id is None:
            id = login
            
        # try to normalize the list of ids/logins into single sequence    
        if isinstance( login, (list, tuple ) ):
            if isinstance( id, (list, tuple ) ):
                ids = []
                ids.extend( id )
                ids.extend( login )
            else:
                ids = list( login )
                ids.append( id )
            id = ids
        elif isinstance( id, (list, tuple ) ) and login:
            id = list(id)
            id.append( login )
        elif id and login:
            id = [ id, login]
            
        if id is None and exact_match:
            return []
        elif id is None:
            clause = None
        elif isinstance( id, (list, tuple)) and exact_match:
            statements = []
            for i in id:
                statements.append( schema.users.c.login == i )
            clause = rdb.or_( *statements )
        elif isinstance( id, (list, tuple)) and not exact_match:
            clause = rdb.or_(*(map( schema.users.c.login.contains, id )))
        elif not exact_match:
            clause = schema.users.c.login.contains( id )
        else:
            clause = schema.users.c.login == id

        query = rdb.select( [ schema.users.c.login ],
                            rdb.and_(clause, schema.users.c.active_p == 'A') )

        if sort_by:
            assert sort_by in ('login', 'last_name')
            query = query.order_by( getattr( schema.users.c, sort_by ) )

        if max_results is not None and isinstance( max_results, int ):
            query =query.limit( max_results )
            
        return [ dict( id=safeencode(r[0]), login=safeencode(r[0]), pluginid=self.id ) for r in query.execute()]

    #
    # IUserAdderPlugin implementation
    #
    security.declarePrivate('doAddUser')
    def doAddUser(self, login, password):
        try:
            self.addUser(login, login, password)
        except KeyError:
            return False
        return True

    #
    # (notional)IZODBUserManager interface
    #
    security.declareProtected(ManageUsers, 'listUserIds')
    def listUserIds(self):
        users = schema.users.select( [schema.users.c.login ], schema.users.c.active_p == 'A').execute()
        return tuple([safeencode(r['login']) for r in users] )
    
    security.declareProtected(ManageUsers, 'listUserInfo')
    def listUserInfo(self):
        users = schema.users.select( [schema.users.c.login ], schema.users.c.active_p == 'A').execute()
        return [ dict( id=safeencode(r['login']),
                       login=safeencode(r['login']), pluginid=self.id ) for r in users]

    security.declareProtected(ManageUsers, 'getUserInfo')
    def getUserInfo(self, user_id ):
        uid = self._uid( user_id )
        if not uid:
            return None
        return dict( id=user_id, login=user_id, pluginid=self.id )

    security.declareProtected(ManageUsers, 'getLoginForUserId')
    def getLoginForUserId(self, user_id):
        return user_id
    
    security.declarePrivate('addUser')
    def addUser(self, user_id, login_name, password): # raises keyerror, lookup error
        salt = generate_salt()
        e_pass = encrypt( password, salt )
        if self._uid( login_name ):
            raise KeyError("Duplicate User Id: %s"%user_id)
        insert = schema.users.insert()
        insert.values( login = user_id, salt = salt, password = e_pass, type="user",
                       # dummy values for non null fields
                       first_name=u"unknown", last_name=u"unknown", email=u"unknown",
                       ).execute()
    
    security.declarePrivate('removeUser')
    def removeUser(self, user_id): # raises keyerror
        uid = self._uid( user_id )
        if not uid:
            raise KeyError("Invalid User"%uid)
        # update user to show as inactive
        schema.users.update().where( schema.users.c.user_id == uid ).values( active_p = 'I').execute()

    security.declarePrivate('updateUserPassword')
    def updateUserPassword(self, user_id, login_name, password): # raise keyerror, lookup error
        uid = self._uid( user_id )
        if uid is None:
            raise KeyError("Invalid User %s"%user_id )
        salt = generate_salt()
        e_pass = encrypt( password, salt )
        schema.users.update().where( schema.users.c.user_id == uid ).values(
            salt = salt,
            password = password
            ).execute()

   #
    # Allow users to change their own login name and password.
    #
    security.declareProtected(SetOwnPassword, 'getOwnUserInfo')
    def getOwnUserInfo(self):
        """Return current user's info."""
        user_id = getSecurityManager().getUser().getId()
        return self.getUserInfo(user_id)
    
    def _uid( self, login, auth=False ):
        cols = [ schema.users.c.user_id ]
        if auth:
            cols.extend( [schema.users.c.password, schema.users.c.salt ] )

        
        res = rdb.select( cols,
                          rdb.and_( schema.users.c.login == login,
                                    schema.users.c.active_p == 'A' )).execute()
                       
        uid_tuple = res.fetchone()
        if not uid_tuple:
            return None
        if auth:
            return uid_tuple
        return uid_tuple[0]
                         

classImplements( UserManager,
                 IAuthenticationPlugin,
                 IUserEnumerationPlugin,
                 IUserAdderPlugin,
                 IUserManagement,
                 IDeleteCapability,
                 IPasswordSetCapability)

InitializeClass( UserManager )        
