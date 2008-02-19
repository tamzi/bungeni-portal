"""
$Id: $
"""

from zope import interface
from zope.app.security.interfaces import IAuthentication
from zope.app.authentication import PluggableAuthentication
from zope.app.component import site
from ore.alchemist.interfaces import IAlchemistContent
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.publisher.interfaces.http import IHTTPRequest
from ore.wsgiapp.app import Application

import domain
import interfaces
import url


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
        auth.authenticatorPlugins = ('rdb-auth',)
        sm.registerUtility( auth, IAuthentication )

        # setup app structure
        # 

        # domain objects
        governments = domain.GovernmentContainer()
        self.context['governments'] = governments
        
        parliaments = domain.ParliamentContainer()
        self.context['parliament'] = parliaments
        
        committees = domain.CommitteeContainer()
        self.context['committees'] = committees
        
        bills = domain.BillContainer()
        self.context['bills'] = bills
        
        motions = domain.MotionContainer()
        self.context['motions'] = motions
        
        questions = domain.QuestionContainer()
        self.context['questions'] = questions
        
        #users = domain.UsersContainer()
        #self.context['users'] = users
        
        parliament_members = domain.ParliamentMemberContainer()
        self.context['members'] = parliament_members
        
        #groups = domain.GroupContainer()       
        #self.context['groups'] = groups
        
        constituency = domain.ConstituencyContainer()
        self.context['constituencies'] = constituency
        
        provinces = domain.ProvinceContainer()
        self.context['provinces'] = provinces
        
        regions = domain.RegionContainer()
        self.context['regions'] = regions
        
        ministries = domain.MinistryContainer()
        self.context['ministries'] = ministries
        
        parties = domain.PoliticalPartyContainer()
        self.context['politicalparties'] = parties
        
        self.context['sessions'] = domain.ParliamentSessionContainer()
        
        # todo separate out to url module
        #url.setupResolver( self.context )
        # 
        # provide a url resolver for object urls
        url_resolver = url.AbsoluteURLFactory( self.context )
        sm.registerAdapter( factory=url_resolver, 
                            required=(IAlchemistContent, IHTTPRequest), 
                            provided=IAbsoluteURL, name="absolute_url")
                           
        sm.registerAdapter( factory=url_resolver, 
                            required=(IAlchemistContent, IHTTPRequest),
                            provided=IAbsoluteURL )

