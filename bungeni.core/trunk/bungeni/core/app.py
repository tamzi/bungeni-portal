"""
$Id: $
"""

from zope import interface
from zope.app.security.interfaces import IAuthentication
from zope.app.authentication import PluggableAuthentication
from zope.app.component import site

from ore.wsgiapp.app import Application

import domain
import interfaces


class BungeniApp( Application ):

    interface.implements( interfaces.IBungeniApplication )

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

        
        # setup app structure
        bills = domain.BillContainer()
        self.context['bills'] = bills
                
        motions = domain.MotionContainer()
        self.context['motions'] = motions
        
        
1