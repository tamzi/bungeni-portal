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
from bungeni.models.utils import get_user
from bungeni.core import interfaces

def setUpSubscriber(obj, event):
    initializer = model_interfaces.IBungeniSetup(obj)
    initializer.setUp()

class BungeniApp(Application):
    implements(model_interfaces.IBungeniApplication)

class BungeniAdmin(SampleContainer):
    implements(model_interfaces.IBungeniAdmin )

class AppSetup(object):
    
    implements(model_interfaces.IBungeniSetup)
    
    def __init__(self, context):
        self.context = context
    
    def setUp(self):
        
        import index
        # ensure indexing facilities are setup(lazy)
        index.setupFieldDefinitions(index.indexer)
        
        sm = site.LocalSiteManager(self.context)
        self.context.setSiteManager(sm)
        
        # !+ where is the view name for the app root (slash) set?
        # NOTE: when logged in "/" is redirected to "/workspace/"
        
        # top-level sections
        workspace = self.context["workspace"] = Section(
            title=_(u"Workspace"),
            description=_(u"Current parliamentary activity"),
            default_name=u"workspace-index")
        
        business = self.context["business"] = Section(
            title=_(u"Business"),
            description=_(u"Daily operations of the parliament"),
            default_name=u"whats-on")

        members = self.context["members"] = Section(
            title=_(u"Members"),
            description=_(u"Records on members of parliament"),
            default_name=u"current")

        archive = self.context["archive"] = Section(
            title=_(u"Archive"),
            description=_(u"Parliament records and documents"),
            default_name=u"browse")

        admin = self.context["admin"] = Section(
            title=_(u"Administration"),
            description=_(u"Administer bungeni settings"),
            marker=model_interfaces.IBungeniAdmin,
            default_name=u"content" 
            )
        
        # workspace section
        ws_index = workspace["index"] = Section(
            title=_(u"Parliamentary items"),
            description=_(u"Current parliamentary activity"),
            default_name="workspace-index")
        ws_archive = workspace["my-archive"] = Section(
            title=_(u"My archive"),
            description=_(u"My archive personal items"),
            default_name="workspace-archive")
        ws_calendar = workspace[u"calendar"] = QueryContent(
            container_getter(get_current_parliament, 'sittings'),
            title=_(u"Scheduling"),
            description=_(u"View the sittings of the current parliament"))
        
        # for all the following, we want to keep title=None so that 
        # no menu item for the entry will be displayed
        ws_questions = workspace["questions"] = QueryContent(
            container_getter(get_current_parliament, 'questions'),
            #title=_(u"Questions"),
            description=_(u"Questions"))
        ws_motions = workspace["motions"] = QueryContent(
            container_getter(get_current_parliament, 'motions'),
            #title=_(u"Motions"),
            description=_(u"Motions"))
        ws_committees = workspace["committees"] = QueryContent(
            container_getter(get_current_parliament, 'committees'),
            #title=_(u"Committees"), # title=None to not show up in menu
            description=_(u"Committees"))
        ws_tableddocuments = workspace["tableddocuments"] = QueryContent(
            container_getter(get_current_parliament, 'tableddocuments'),
            #title=_(u"Tabled documents"),
            description=_(u"Tabled documents"))
        ws_bills = workspace["bills"] = QueryContent(
            container_getter(get_current_parliament, 'bills'),
            #title=_(u"Bills"),
            description=_(u"Bills"))
        ws_agendaitems = workspace["agendaitems"] = QueryContent(
            container_getter(get_current_parliament, 'agendaitems'),
            #title=_(u"Agenda items"),
            description=_(u" items"))
        
        # for all the following, we want to keep title=None so that 
        # no menu item for the entry will be displayed
        wsmya_questions = ws_archive["questions"] = QueryContent(
            container_getter(get_user, 'questions'),
            #title=_(u"Questions"),
            description=_(u"Questions"))
        wsmya_motions = ws_archive["motions"] = QueryContent(
            container_getter(get_user, 'motions'),
            #title=_(u"Motions"),
            description=_(u"Motions"))
        wsmya_tableddocuments = ws_archive["tableddocuments"] = QueryContent(
            container_getter(get_user, 'tableddocuments'),
            #title=_(u"Tabled documents"),
            description=_(u"Tabled documents"))
        wsmya_bills = ws_archive["bills"] = QueryContent(
            container_getter(get_user, 'bills'),
            #title=_(u"Bills"),
            description=_(u"Bills"))
        wsmya_agendaitems = ws_archive["agendaitems"] = QueryContent(
            container_getter(get_user, 'agendaitems'),
            #title=_(u"Agenda items"),
            description=_(u" items"))
        
        # business section
        whatson = business["whats-on"] = Section(
            title=_(u"What's on"),
            description=_(u"Current parliamentary activity"),
            default_name="whats-on")

        committees = business[u"committees"] = QueryContent(
            container_getter(get_current_parliament, 'committees'),
            title=_(u"Committees"),
            marker=interfaces.ICommitteeAddContext,
            description=_(u"View committees created by the current parliament"))

        bills = business[u"bills"] = QueryContent(
            container_getter(get_current_parliament, 'bills'),
            title=_(u"Bills"),
            marker=interfaces.IBillAddContext,
            description=_(u"View bills issued by the current parliament"))

        questions = business[u"questions"] = QueryContent(
            container_getter(get_current_parliament, 'questions'),
            title=_(u"Questions"),
            marker=interfaces.IQuestionAddContext,
            description=_(u"View questions issued by the current parliament"))

        motions = business[u"motions"] = QueryContent(
            container_getter(get_current_parliament, 'motions'),
            title=_(u"Motions"),
            marker=interfaces.IMotionAddContext,
            description=_(u"View motions issued by the current parliament"))


        tableddocuments = business[u"tableddocuments"] = QueryContent(
            container_getter(get_current_parliament, 'tableddocuments'),
            title=_(u"Tabled documents"),
            marker=interfaces.ITabledDocumentAddContext,
            description=_(u"View the tabled documents of the current parliament"))     

        agendaitems = business[u"agendaitems"] = QueryContent(
            container_getter(get_current_parliament, 'agendaitems'),
            title=_(u"Agenda items"),
            marker=interfaces.IAgendaItemAddContext,
            description=_(u"View the agenda items of the current parliament"))

       # sessions = business[u"sessions"] = QueryContent(
       #     container_getter(get_current_parliament, 'sessions'),
       #     title=_(u"Sessions"),
       #     marker=interfaces.ISessionAddContext,
       #     description=_(u"View the sessions of the current parliament."))

        sittings = business[u"sittings"] = QueryContent(
            container_getter(get_current_parliament, 'sittings'),
            title=_(u"Sittings"),
            description=_(u"View the sittings of the current parliament"))
            
        #Parliamentary reports
        preports =  business[u"preports"] = QueryContent(
            container_getter(get_current_parliament, 'preports'),
            title=_(u"Parliamentary publications"),
            marker=interfaces.IReportAddContext,
            description=_(u"View Agenda and Minutes reports of the current parliament"))
        
        
        # members section
        current = members[u"current"] = QueryContent(
            container_getter(get_current_parliament, 'parliamentmembers'),
            title=_(u"Current"),
            description=_(u"View current parliament members (MPs)"))

        political_groups = members[u"political-groups"] = QueryContent(
            container_getter(get_current_parliament, 'politicalparties'),
            title=_(u"Political groups"),
            description=_(u"View current political groups"))

        # archive
        records = archive[u"browse"] = Section(
            title=_(u"Browse"),
            description=_(u"Current and historical records"),
            default_name="browse-archive")

        documents = archive["documents"] = Section(
            title=_(u"Documents"),
            description=_(u"Visit the digital document repository"),
            default_name="browse-archive")


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
        
        documents[u"reports"] = domain.ReportContainer()
        provideAdapter(location.ContainerLocation(tableddocuments, documents[u"reports"]),
                       (implementedBy(domain.Report), ILocation))
        
        records[u"parliaments"] = domain.ParliamentContainer()
        provideAdapter(location.ContainerLocation(records[u"parliaments"]),
                       (implementedBy(domain.Parliament), ILocation))
        
        records[u"parties"] = domain.PoliticalPartyContainer()
        provideAdapter(location.ContainerLocation(records[u"parties"]),
                       (implementedBy(domain.PoliticalParty), ILocation))

        records[u"constituencies"] = domain.ConstituencyContainer()
        provideAdapter(location.ContainerLocation(records[u"constituencies"]),
                       (implementedBy(domain.Constituency), ILocation))
                                                                     
        
        records[u"committees"] = domain.CommitteeContainer()
        provideAdapter(location.ContainerLocation(committees, records[u"committees"]),
                       (implementedBy(domain.Committee), ILocation))

        #records[u"mps"] = domain.MemberOfParliamentContainer()
        #provideAdapter(location.ContainerLocation(records[u"mps"]),
        #               (implementedBy(domain.MemberOfParliament), ILocation))
        
        ##########
        # Admin User Interface
        # Administration section
        
        content = admin["content"] = Section(
            title=_(u"Content"),
            description=_(u"browse the content"),
            default_name="browse-archive")

        settings = admin["settings"] = Section(
            title=_(u"Settings"),
            description=_(u"settings"),
            marker=model_interfaces.IBungeniAdmin,            
            default_name="settings")

        content[u"parliaments"] = domain.ParliamentContainer()
        provideAdapter(location.ContainerLocation(content[u"parliaments"]),
                       (implementedBy(domain.Parliament), ILocation))
        
        content[u'users'] = domain.UserContainer()
        provideAdapter(location.ContainerLocation(content[u"users"]),
                       (implementedBy(domain.User), ILocation))    

        content[u'headings'] = domain.HeadingContainer()
        provideAdapter(location.ContainerLocation(content[u"headings"]),
                       (implementedBy(domain.Heading), ILocation))                           

        content[u"provinces"] = domain.ProvinceContainer()
        provideAdapter(location.ContainerLocation(content[u"provinces"]),
                       (implementedBy(domain.Province), ILocation))
                       
        content[u"regions"] = domain.RegionContainer()
        provideAdapter(location.ContainerLocation(content[u"regions"]),
                       (implementedBy(domain.Region), ILocation))

        content[u"constituencies"] = domain.ConstituencyContainer()
        provideAdapter(location.ContainerLocation(content[u"constituencies"]),
                       (implementedBy(domain.Constituency), ILocation))     
                       
                                             
   

