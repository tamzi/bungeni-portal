"""
$Id: $
"""

import os
from os import path

from zope import interface
from zope.app.security.interfaces import IAuthentication


#from from zope.app.authentication import PluggableAuthentication
from zope.app.component import site
from zope.app.container.sample import SampleContainer

from ore.wsgiapp.app import Application
from ore.svn import repos
from ore.library.library import Library

from auth import PluggableAuthentication
import domain
import interfaces

class BungeniApp( Application ):

    interface.implements( interfaces.IBungeniApplication )

class BungeniAdmin( SampleContainer ):

    interface.implements( interfaces.IBungeniAdmin  )
    
def setUpSubscriber( object, event ):
    initializer = interfaces.IBungeniSetup( object )
    initializer.setUp()

    
class AppSetup( object ):

    interface.implements( interfaces.IBungeniSetup )

    def __init__( self, context ):
        self.context = context
        
    def setUp( self ):

        # ensure indexing facilities are setup ( lazy )
        import index
        
        # ensure version file are setup
        import files
        files.setup()
        
        sm = site.LocalSiteManager( self.context )
        self.context.setSiteManager( sm )

        # setup authentication plugin
        auth = PluggableAuthentication()
        auth.credentialsPlugins = ('Cookie Credentials',)
        auth.authenticatorPlugins = ('rdb-auth', 'global-auth')
        sm.registerUtility( auth, IAuthentication )

        # setup app structure
        # 

        # domain objects
        #governments = domain.GovernmentContainer()
        #self.context['governments'] = governments
        
        parliaments = domain.ParliamentContainer()
        self.context['parliament'] = parliaments
        
        #committees = domain.CommitteeContainer()
        #self.context['committees'] = committees
        
        bills = domain.BillContainer()
        self.context['bills'] = bills
        
        motions = domain.MotionContainer()
        self.context['motions'] = motions
        
        questions = domain.QuestionContainer()
        self.context['questions'] = questions
        
        #users = domain.UsersContainer()
        #self.context['users'] = users
        
        parliament_members = domain.ParliamentMemberContainer()
        self.context['persons'] = parliament_members
        
        staff_members = domain.StaffMemberContainer()
        self.context['staff'] = staff_members        
        
        #groups = domain.GroupContainer()       
        #self.context['groups'] = groups
        
        constituency = domain.ConstituencyContainer()
        self.context['constituencies'] = constituency
        
        provinces = domain.ProvinceContainer()
        self.context['provinces'] = provinces
        
        regions = domain.RegionContainer()
        self.context['regions'] = regions
        
        #ministries = domain.MinistryContainer()
        #self.context['ministries'] = ministries
        
        #parties = domain.PoliticalPartyContainer()
        #self.context['politicalparties'] = parties
        
        self.context['sessions'] = domain.ParliamentSessionContainer()
        
        countries = domain.CountryContainer()
        self.context['countries'] = countries
        self.context['repository'] = Library( repository_storage )

        ##########
        # Admin User Interface
        self.context['admin'] = admin = BungeniAdmin()
        admin['users'] = admin_user = domain.UserContainer()
        interface.directlyProvides( admin_user, interfaces.IAdminUserContainer )

        admin['groups'] = domain.GroupContainer()
        ##########
        
        #titles = domain.MemberTitleContainer()
        #self.context('titles') = titles
        
        # todo separate out to url module
        #url.setupResolver( self.context )
        # 
        # provide a url resolver for object urls
        
        ######### does this cause the multiadapter error? ########
        
        #url_resolver = url.AbsoluteURLFactory( self.context )
        #sm.registerAdapter( factory=url_resolver, 
        #                    required=(IAlchemistContent, IHTTPRequest), 
        #                    provided=IAbsoluteURL, name="absolute_url")
                           
        #sm.registerAdapter( factory=url_resolver, 
        #                    required=(IAlchemistContent, IHTTPRequest),
        #                    provided=IAbsoluteURL )

# we store files in buildout/parts/repository
# 
def setupStorageDirectory( ):
    # we start in buildout/src/bungeni.core/bungeni/core
    # we end in buildout/parts/repository    
    store_dir = __file__
    x = 0
    while x < 5:
        x += 1
        store_dir = path.split( store_dir )[0]

    store_dir = path.join( store_dir, 'parts', 'repository')
    if path.exists( store_dir ):
        assert path.isdir( store_dir )
    else:
        try:
            repos.create( store_dir )
        except:
            import pdb, sys, traceback
            traceback.print_exc()
            pdb.post_mortem(sys.exc_info()[-1])
            raise
    return store_dir


repository_storage = setupStorageDirectory()
