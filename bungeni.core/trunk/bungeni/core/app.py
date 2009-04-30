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
from bungeni.models import interfaces as model_interfaces

from bungeni.core import location
from bungeni.core.content import Section
from bungeni.core.content import QueryContent
from bungeni.core.i18n import _
from bungeni.models.queries import get_current_parliament
from bungeni.models.queries import container_getter
from bungeni.core.interfaces import IAddContext
from bungeni.core import interfaces

def setUpSubscriber(object, event):
    initializer = model_interfaces.IBungeniSetup(object)
    initializer.setUp()

class BungeniApp(Application):
    implements(model_interfaces.IBungeniApplication)

class BungeniAdmin(SampleContainer):
    implements(model_interfaces.IBungeniAdmin )
    
class AppSetup(object):
    implements(model_interfaces.IBungeniSetup)

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

        # top-level sections
        business = self.context["business"] = Section(
            title=_(u"Business"),
            description=_(u"Daily operations of the parliament."),
            default_name=u"whats-on")

        members = self.context["members"] = Section(
            title=_(u"Members"),
            description=_(u"Records on members of parliament."),
            default_name=u"current")

        archive = self.context["archive"] = Section(
            title=_(u"Archive"),
            description=_(u"Parliament records and documents."),
            default_name=u"browse")

        # business section
        whatson = business["whats-on"] = Section(
            title=_(u"What's on"),
            description=_(u"Current parliamentary activity."),
            default_name="@@whats-on")

        committees = business[u"committees"] = QueryContent(
            container_getter(get_current_parliament, 'committees'),
            title=_(u"Committees"),
            marker=interfaces.ICommitteeAddContext,
            description=_(u"View committees created by the current parliament."))

        bills = business[u"bills"] = QueryContent(
            container_getter(get_current_parliament, 'bills'),
            title=_(u"Bills"),
            marker=interfaces.IBillAddContext,
            description=_(u"View bills issued by the current parliament."))

        questions = business[u"questions"] = QueryContent(
            container_getter(get_current_parliament, 'questions'),
            title=_(u"Questions"),
            marker=interfaces.IQuestionAddContext,
            description=_(u"View questions issued by the current parliament."))

        motions = business[u"motions"] = QueryContent(
            container_getter(get_current_parliament, 'motions'),
            title=_(u"Motions"),
            marker=interfaces.IMotionAddContext,
            description=_(u"View motions issued by the current parliament."))

        # members section
        current = members[u"current"] = QueryContent(
            container_getter(get_current_parliament, 'parliamentmembers'),
            title=_(u"Current"),
            description=_(u"View current parliament members (MPs)."))

        political_groups = members[u"political-groups"] = QueryContent(
            container_getter(get_current_parliament, 'politicalparties'),
            title=_(u"Political groups"),
            description=_(u"View current political groups."))

        # archive
        records = archive[u"browse"] = Section(
            title=_(u"Browse"),
            description=_(u"Current and historical records."),
            default_name="@@browse-archive")

        documents = archive["documents"] = Section(
            title=_(u"Documents"),
            description=_(u"Visit the digital document repository."))

        # archive/records
        bills = records[u"bills"] = domain.BillContainer()
        provideAdapter(location.ContainerLocation(bills),
                       (implementedBy(domain.Bill), ILocation))

        motions = records[u"motions"] = domain.MotionContainer()
        provideAdapter(location.ContainerLocation(motions),
                       (implementedBy(domain.Motion), ILocation))

        questions = records[u"questions"] = domain.QuestionContainer()
        provideAdapter(location.ContainerLocation(questions),
                       (implementedBy(domain.Question), ILocation))

        parliaments = records[u"parliaments"] = domain.ParliamentContainer()
        provideAdapter(location.ContainerLocation(parliaments),
                       (implementedBy(domain.Parliament), ILocation))

        members = records[u"members"] = domain.UserContainer()
        provideAdapter(location.ContainerLocation(members),
                       (implementedBy(domain.User), ILocation))
        
        parties = records[u"parties"] = domain.PoliticalPartyContainer()
        provideAdapter(location.ContainerLocation(parties),
                       (implementedBy(domain.PoliticalParty), ILocation))

        constituencies = records[u"constituencies"] = \
                         domain.ConstituencyContainer()
        provideAdapter(location.ContainerLocation(constituencies),
                       (implementedBy(domain.Constituency), ILocation))
        
        offices = records[u"offices"] = Section(
            title=_(u"Offices"),
            description=_(u"Overview of parliamentary offices."))

        committees = records[u"committees"] = domain.CommitteeContainer()
        provideAdapter(location.ContainerLocation(committees),
                       (implementedBy(domain.Committee), ILocation))

        governments = records[u"governments"] = domain.GovernmentContainer()
        provideAdapter(location.ContainerLocation(governments),
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


