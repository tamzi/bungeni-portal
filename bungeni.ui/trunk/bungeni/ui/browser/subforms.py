# utf-8
from zope.viewlet import viewlet, interfaces
from zope.app.pagetemplate import ViewPageTemplateFile
import bungeni.core.domain as domain
from bungeni.core.interfaces import IMemberOfParliament
from ore.alchemist import Session
from ore.alchemist.model import queryModelDescriptor
from bungeni.core.i18n import _
import bungeni.core.domain as domain
from forms import BungeniAttributeDisplay
from container import ContainerListing

from alchemist.ui.viewlet import EditFormViewlet, AttributesViewViewlet, DisplayFormViewlet
#from alchemist.ui.core import DynamicFields

from zope.formlib import form

from bungeni.ui.viewlets.sittingcalendar import SittingCalendarViewlet

class SubformViewlet ( ContainerListing ):

    render = ViewPageTemplateFile ('templates/generic-sub-container.pt')  


        

class SessionViewlet( SubformViewlet ):


    def __init__( self,  context, request, view, manager ):        

        self.context = context.sessions
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None


class GovernmentViewlet( SubformViewlet ):


    def __init__( self,  context, request, view, manager ):        

        self.context = context.governments                  
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None

class MemberOfParliamentViewlet( SubformViewlet ):


    def __init__( self,  context, request, view, manager ):        

        self.context = context.parliamentmembers                  
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None



class CommitteeSittingsViewlet( SittingCalendarViewlet ):

    def __init__( self,  context, request, view, manager ):        

        self.context = context.sittings                  
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None
#        self.Date=datetime.date.today()
#        self.Data = []
#        session = Session()
#        self.type_query = session.query(domain.SittingType)
        super( CommitteeSittingsViewlet, self).__init__(self.context, request, view, manager)

class MinistersViewlet( ContainerListing ):


    def __init__( self,  context, request, view, manager ):        

        self.context = context.ministers                  
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None


    render = ViewPageTemplateFile ('templates/generic-sub-container.pt')  

class MinistriesViewlet( ContainerListing ):


    def __init__( self,  context, request, view, manager ):        

        self.context = context.ministries                   
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None


    render = ViewPageTemplateFile ('templates/generic-sub-container.pt')  


class CommitteesViewlet( ContainerListing ):

    def __init__( self,  context, request, view, manager ):        

        self.context = context.committees                   
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None


    render = ViewPageTemplateFile ('templates/generic-sub-container.pt')  

class CommitteeStaffViewlet( ContainerListing ):

    def __init__( self,  context, request, view, manager ):        

        self.context = context.committeestaff                    
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None


    render = ViewPageTemplateFile ('templates/generic-sub-container.pt')  


class CommitteeMemberViewlet( ContainerListing ):

    def __init__( self,  context, request, view, manager ):        

        self.context = context.committeemembers                     
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None


    render = ViewPageTemplateFile ('templates/generic-sub-container.pt')                
    
class TitleViewlet ( ContainerListing ):

    def __init__( self,  context, request, view, manager ):        

        self.context = context.titles                     
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None

    render = ViewPageTemplateFile ('templates/generic-sub-container.pt')                


    
class PersonInfo( BungeniAttributeDisplay ):
    """
    Bio Info / personal data about the MP
    """
    mode = "view"
    template = ViewPageTemplateFile('templates/display_subform.pt')        
    form_name = _(u"Personal Info")   
    
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.query = None
        md = queryModelDescriptor(domain.ParliamentMember)          
        self.form_fields=md.fields #.select('user_id', 'start_date', 'end_date')
        
    def update(self):
        """
        refresh the query
        """       
        session = Session()
        user_id = self.context.user_id
        self.query = session.query(domain.ParliamentMember).filter(domain.ParliamentMember.c.user_id == user_id) 
        self.context = self.query.all()[0]
        self.context.__parent__=None
        super( PersonInfo, self).update()



    
            
    
