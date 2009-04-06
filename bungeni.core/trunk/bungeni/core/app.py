"""
$Id: $
"""

from os import path

from zope.interface import implements
from zope.interface import implementedBy
from zope.component import provideAdapter

from zope.app.component import site
from zope.app.container.sample import SampleContainer
from zope.location.interfaces import ILocation

from ore.wsgiapp.app import Application
from ore.svn import repos
from ore.library.library import Library

from bungeni.models import domain
from bungeni.models import interfaces
from bungeni.core import location
from bungeni.core.content import Section
from bungeni.core.i18n import _

class BungeniApp(Application):
    implements(interfaces.IBungeniApplication)

class BungeniAdmin(SampleContainer):
    implements(interfaces.IBungeniAdmin )
    
def setUpSubscriber(object, event):
    initializer = interfaces.IBungeniSetup( object )
    initializer.setUp()

class AppSetup( object ):
    implements(interfaces.IBungeniSetup)

    def __init__( self, context ):
        self.context = context
        
    def setUp( self ):
        
        import index
        # ensure indexing facilities are setup ( lazy )
        index.setupFieldDefinitions(index.indexer)        

        # ensure version file are setup
        import files
        files.setup()
        
        sm = site.LocalSiteManager( self.context )
        self.context.setSiteManager( sm )

        # set up primary site structure
        business = self.context["business"] = Section(
            title=_(u"Business"),
            description=_(u"Daily operations of the parliament."))

        parliament = self.context["parliament"] = Section(
            title=_(u"Parliament"),
            description=_(u"Information on parliament."))

        # business section
        bills = business[u"bills"] = domain.BillContainer()
        provideAdapter(location.LocationProxyAdapter(bills),
                       (implementedBy(domain.Bill), ILocation))

        motions = business[u"motions"] = domain.MotionContainer()
        provideAdapter(location.LocationProxyAdapter(motions),
                       (implementedBy(domain.Motion), ILocation))

        questions = business[u"questions"] = domain.QuestionContainer()
        provideAdapter(location.LocationProxyAdapter(questions),
                       (implementedBy(domain.Question), ILocation))
        
        # parliament section
        members = parliament[u"members"] = domain.UserContainer()
        provideAdapter(location.LocationProxyAdapter(members),
                       (implementedBy(domain.User), ILocation))
        
        parties = parliament[u"parties"] = domain.PoliticalPartyContainer()
        provideAdapter(location.LocationProxyAdapter(parties),
                       (implementedBy(domain.PoliticalParty), ILocation))

        constituencies = parliament[u"constituencies"] = \
                         domain.ConstituencyContainer()
        provideAdapter(location.LocationProxyAdapter(constituencies),
                       (implementedBy(domain.Constituency), ILocation))
        
        offices = parliament[u"offices"] = Section(
            title=_(u"Offices"),
            description=_(u"Overview of parliamentary offices."))

        committees = parliament[u"committees"] = domain.CommitteeContainer()
        provideAdapter(location.LocationProxyAdapter(committees),
                       (implementedBy(domain.Committee), ILocation))

        government = parliament[u"government"] = domain.GovernmentContainer()
        provideAdapter(location.LocationProxyAdapter(government),
                       (implementedBy(domain.Government), ILocation))
        

        ##########
        # Admin User Interface
        self.context['admin'] = admin = BungeniAdmin()
        
        #admin['users'] = admin_user = domain.UserContainer()
        #interface.directlyProvides( admin_user, interfaces.IAdminUserContainer )
        #admin['groups'] = domain.GroupContainer()
        
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


