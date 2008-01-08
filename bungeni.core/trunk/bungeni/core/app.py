"""
$Id: $
"""

from zope import interface, event, lifecycleevent
from zope.app.authentication import PluggableAuthentication
from zope.app.component import site
from ore.wsgiapp.app import Application

import interfaces



class BungeniApp( Application ):

    interface.implements( interfaces.IBungeniApplication )

    def __init__( self ):
        super( BungeniApp, self).__init__()
        event.notify( lifecycleevent.ObjectCreatedEvent( self ) )

def setUpSubscriber( object, event ):
    initializer = interfaces.IBungeniSetup( object )
    initializer.setUp()
    
class AppSetup( object ):

    interface.implements( interfaces.IBungeniSetup )

    def __init__( self, context ):
        self.context = context
        
    def setUp( self ):
        sm = site.LocalSiteManager( self.context )
        self.context.setSiteManager( sm )

        # setup authentication plugin
        auth = PluggableAuthentication()
        auth.credentialsPlugins = ('Cookie Credentials',)
        auth.authenticatorPlugins = ('bungeni-rdb-auth',)
        sm.registerUtility( auth, IAuthentication )

        
