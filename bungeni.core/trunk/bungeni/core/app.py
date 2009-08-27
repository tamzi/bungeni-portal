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

from bungeni.models import domain
from bungeni.models import interfaces as model_interfaces

from bungeni.core import location
from bungeni.core.content import Section
from bungeni.core.content import QueryContent
from bungeni.core.i18n import _
from bungeni.models.queries import get_current_parliament
from bungeni.models.queries import container_getter
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

        admin = self.context["admin"] = Section(
            title=_(u"Administration"),
            description=_(u"Administer bungeni settings."),
            marker=model_interfaces.IBungeniAdmin,
            default_name=u"index.html" 
            )

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

        sessions = business[u"sessions"] = QueryContent(
            container_getter(get_current_parliament, 'sessions'),
            title=_(u"Sessions"),
            marker=interfaces.ISessionAddContext,
            description=_(u"View the sessions of the current parliament."))

        tableddocuments = business[u"tableddocuments"] = QueryContent(
            container_getter(get_current_parliament, 'tableddocuments'),
            title=_(u"Tabled documents"),
            marker=interfaces.ITabledDocumentAddContext,
            description=_(u"View the tabled documents of the current parliament."))     

        agendaitems = business[u"agendaitems"] = QueryContent(
            container_getter(get_current_parliament, 'agendaitems'),
            title=_(u"Agenda items"),
            marker=interfaces.IAgendaItemAddContext,
            description=_(u"View the agenda items of the current parliament."))                       

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
            description=_(u"Visit the digital document repository."),
            default_name="@@browse-archive")

        ##########
        # Admin User Interface
        #self.context['admin'] = admin = BungeniAdmin()            

        # archive/records
        documents[u"bills"] = domain.BillContainer()
        provideAdapter(location.ContainerLocation(bills, documents[u"bills"]),
                       (implementedBy(domain.Bill), ILocation))

        documents[u"motions"] = domain.MotionContainer()
        provideAdapter(location.ContainerLocation(motions, documents[u"motions"]),
                       (implementedBy(domain.Motion), ILocation))

        documents[u"questions"] = domain.QuestionContainer()
        provideAdapter(location.ContainerLocation(questions, documents[u"questions"]),
                       (implementedBy(domain.Question), ILocation))

        documents[u"agendaitems"] = domain.AgendaItemContainer()
        provideAdapter(location.ContainerLocation(agendaitems, documents[u"agendaitems"]),
                       (implementedBy(domain.AgendaItem), ILocation))
                       
                       
        documents[u"tableddocuments"] = domain.TabledDocumentContainer()
        provideAdapter(location.ContainerLocation(tableddocuments, documents[u"tableddocuments"]),
                       (implementedBy(domain.TabledDocument), ILocation))                       


        records[u"parliaments"] = domain.ParliamentContainer()
        provideAdapter(location.ContainerLocation(records[u"parliaments"]),
                       (implementedBy(domain.Parliament), ILocation))

        #records[u"members"] = domain.UserContainer()
        #provideAdapter(location.ContainerLocation(current, records[u"members"]),
        #               (implementedBy(domain.User), ILocation))

        records[u"parties"] = domain.PoliticalPartyContainer()
        provideAdapter(location.ContainerLocation(records[u"parties"]),
                       (implementedBy(domain.PoliticalParty), ILocation))

        records[u"constituencies"] = domain.ConstituencyContainer()
        provideAdapter(location.ContainerLocation(records[u"constituencies"]),
                       (implementedBy(domain.Constituency), ILocation))

        records[u"offices"] = domain.OfficeContainer()
        provideAdapter(location.ContainerLocation(records[u"offices"]),
                       (implementedBy(domain.Office), ILocation))

        records[u"committees"] = domain.CommitteeContainer()
        provideAdapter(location.ContainerLocation(committees, records[u"committees"]),
                       (implementedBy(domain.Committee), ILocation))

        records[u"governments"] = domain.GovernmentContainer()
        provideAdapter(location.ContainerLocation(records[u"governments"]),
                       (implementedBy(domain.Government), ILocation))


        
        admin['users'] = domain.UserContainer()
        provideAdapter(location.ContainerLocation(admin[u"users"]),
                       (implementedBy(domain.User), ILocation))    
                           
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


