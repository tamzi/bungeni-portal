# utf-8
import datetime
import base64

from zope.viewlet import viewlet, interfaces
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.traversing.browser import absoluteURL 
from zope.security.proxy import removeSecurityProxy
from zope.formlib import form

import sqlalchemy.orm

from ore.alchemist import Session
from ore.alchemist.model import queryModelDescriptor
from ore.alchemist.container import stringKey

from alchemist.ui.viewlet import EditFormViewlet, AttributesViewViewlet, DisplayFormViewlet

import bungeni.core.domain as domain
from bungeni.core.interfaces import IMemberOfParliament
from bungeni.core.i18n import _
import bungeni.core.domain as domain
from bungeni.core.workflows.question import states as qw_state

from bungeni.ui.viewlets.sittingcalendar import SittingCalendarViewlet

from forms import BungeniAttributeDisplay
from container import ContainerListing, AtomContainerListing
from table import AjaxContainerListing

class SubformViewlet ( AjaxContainerListing ):
    """
    
    """
    render = ViewPageTemplateFile ('templates/generic-sub-container.pt')  
    for_display = True

class AtomSubformViewlet( AtomContainerListing ):
    """
    """
    for_display = True        


class SessionViewlet( SubformViewlet ):


    def __init__( self,  context, request, view, manager ):        

        self.context = context.sessions
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None


class ConsignatoryViewlet( SubformViewlet ):


    def __init__( self,  context, request, view, manager ):        

        self.context = context.consignatory
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


class SittingsCalendarViewlet( SittingCalendarViewlet ):
    """
    sittingcalendar displayed for a sitting
    """
    for_display = True    
    
    def __init__( self,  context, request, view, manager ):        

        self.context = context.__parent__                  
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None
        super( SittingsCalendarViewlet, self).__init__(self.context, request, view, manager)

class SittingsViewlet( SittingCalendarViewlet ):
    """
    sittingcalendar for a session or group
    """
    for_display = True
        
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
        super( SittingsViewlet, self).__init__(self.context, request, view, manager)


class SittingAttendanceViewlet( SubformViewlet ):


    def __init__( self,  context, request, view, manager ):        

        self.context = context.attendance                  
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None


class MinistersViewlet( SubformViewlet ):


    def __init__( self,  context, request, view, manager ):        

        self.context = context.ministers                  
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None




class MinistriesViewlet( SubformViewlet ):


    def __init__( self,  context, request, view, manager ):        

        self.context = context.ministries                   
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None





class CommitteesViewlet( SubformViewlet ):

    def __init__( self,  context, request, view, manager ):        

        self.context = context.committees                   
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None



class CommitteeStaffViewlet( SubformViewlet ):

    def __init__( self,  context, request, view, manager ):        

        self.context = context.committeestaff                    
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None




class CommitteeMemberViewlet( SubformViewlet ):

    def __init__( self,  context, request, view, manager ):        

        self.context = context.committeemembers                     
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None


class CommitteeMemberAtomViewlet( AtomSubformViewlet ):

    def __init__( self,  context, request, view, manager ):        

        self.context = context.committeemembers                     
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None

    
class TitleViewlet ( SubformViewlet ):

    def __init__( self,  context, request, view, manager ):        

        self.context = context.titles                     
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None

class AddressesViewlet( SubformViewlet ):

    def __init__( self,  context, request, view, manager ):        

        self.context = context.addresses
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None

class PoliticalPartyViewlet( SubformViewlet ):
    def __init__( self,  context, request, view, manager ):        

        self.context = context.politicalparties
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None

class PartyMemberViewlet( SubformViewlet ):
    def __init__( self,  context, request, view, manager ):        

        self.context = context.partymembers
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None
        
class PartyMemberAtomViewlet( AtomSubformViewlet ):
    """
    """        
    def __init__( self,  context, request, view, manager ):        

        self.context = context.partymembers
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None
            
        
    
class PartyMembershipViewlet( SubformViewlet ):
    def __init__( self,  context, request, view, manager ):        

        self.context = context.party
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None
            
#class ResponseViewlet( SubformViewlet ):
#    def __init__( self,  context, request, view, manager ):        
#
#        self.context = context.responses
#        self.request = request
#        self.__parent__= context
#        self.manager = manager
#        self.query = None

    
class PersonInfo( BungeniAttributeDisplay ):
    """
    Bio Info / personal data about the MP
    """
    for_display = True    
    mode = "view"
    template = ViewPageTemplateFile('templates/display_subform.pt')        
    form_name = _(u"Personal Info")   
    
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= context.__parent__
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
        parent = self.context.__parent__
        self.query = session.query(domain.ParliamentMember).filter(domain.ParliamentMember.c.user_id == user_id) 
        self.context = self.query.all()[0]
        self.context.__parent__= parent
        super( PersonInfo, self).update()

class AtomPersonInfo( PersonInfo ):
    template = ViewPageTemplateFile('templates/generic-atom-container.pt')
    
    def name(self):
        return self.form_name
        
    def listing(self):
        return  ViewPageTemplateFile('templates/display_atom_form.pt').__call__(self)
        
    def uid(self):     
        #XXX       
        return "urn:uuid:" + base64.urlsafe_b64encode(self.context.__class__.__name__ + ':' + stringKey(removeSecurityProxy(self.context)))
        
    def url(self):    
        return absoluteURL( self.context, self.request )       
        
    def updated(self):
        return datetime.datetime.now().isoformat()          
                       
    def update(self):    
        super( AtomPersonInfo, self).update()
        self.form_name = _(u"Bio Info")

class SupplementaryQuestionsViewlet( SubformViewlet ):
    form_name = (u"Supplementary Questions")    
    
    @property
    def for_display(self):
        return self.context.__parent__.status == qw_state.answered   
    
    def __init__( self,  context, request, view, manager ):        

        self.context = context.supplementaryquestions
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None
        #self.form_name = (u"Supplementary Questions")    


class InitialQuestionsViewlet( BungeniAttributeDisplay ):
    form_name = (u"Initial Questions")
    template = ViewPageTemplateFile('templates/display_subform.pt')    
    
    @property
    def for_display(self):
        return self.context.supplement_parent_id is not None            
        
    def update(self):
        """
        refresh the query
        """    
        if self.context.supplement_parent_id is None:
            self.context = self.__parent__
            #self.for_display = False
            return
               
        session = Session()
        results = session.query(domain.Question).get(self.context.supplement_parent_id) 

        if results:
            #parent = self.context.__parent__
            self.context = results
            #self.context.__parent__ = parent
            self.form_name = (u"Initial Questions")
            self.has_data = True
            #self.for_display =True
        else:
            self.has_data = False
            self.context = None
            
        super( InitialQuestionsViewlet, self).update()



class ResponseViewlet( BungeniAttributeDisplay ):
    """
    Response to Question
    """
    mode = "view"
    template = ViewPageTemplateFile('templates/display_subform.pt')        
    form_name = _(u"Response")   
    addurl = 'add'
    add_action = form.Actions( form.Action(_(u'add response'), success='handle_response_add_action'), )
    for_display = True
    
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.query = None
        md = queryModelDescriptor(domain.Response)          
        self.form_fields=md.fields

    def handle_response_add_action( self, action, data ):
        self.request.response.redirect(self.addurl)

 
        
    def update(self):
        """
        refresh the query
        """       
        session = Session()
        question_id = self.context.question_id
        self.query = session.query(domain.Response).filter(domain.Response.c.response_id == question_id) 
        results = self.query.all() 
        #self.context = self.query.all()[0]
        path = absoluteURL( self.context, self.request ) 
        self.addurl = '%s/responses/add' %( path )
        if results:
            self.context = results[0]
            self.context.__parent__=None
            self.has_data = True
        else:
            self.context =  domain.Response()
            self.has_data = False             
            self.actions = self.add_action.actions
        super( ResponseViewlet, self).update()





            
class BillTimeLineViewlet( viewlet.ViewletBase ):
    """
    tracker/timeline view:
    Chronological changes are aggregated from : bill workflow, bill
    audit, bill scheduling and bill event records. 
    """
    add_action = form.Actions( form.Action(_(u'add event'), success='handle_event_add_action'), )
    for_display = True    
    # sqlalchemy give me a rough time sorting a union, with hand coded sql it is much easier.
    _sql_timeline = """
            SELECT 'schedule' AS "atype",  "items_schedule"."item_id" AS "item_id", "items_schedule"."status" AS "title", "group_sittings"."start_date" AS "adate" 
            FROM "public"."items_schedule" AS "items_schedule", "public"."group_sittings" AS "group_sittings" 
            WHERE "items_schedule"."sitting_id" = "group_sittings"."sitting_id" 
            AND "items_schedule"."active" = True
            AND "items_schedule"."item_id" = %(item_id)s
         UNION
            SELECT 'event' AS "atype", "item_id", "title", "event_date" AS "adate" 
            FROM "public"."event_items" AS "event_items"
            WHERE "item_id" = %(item_id)s
         UNION
            SELECT "action" as "atype", "content_id" AS "item_id", "description" AS "title", "date" AS "adate" 
            FROM "public"."bill_changes" AS "bill_changes" 
            WHERE "action" = 'workflow'
            AND "content_id" = %(item_id)s
         ORDER BY adate
                """
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.query = None            
    
    def handle_event_add_action( self, action, data ):
        self.request.response.redirect(self.addurl)    
    
    def update(self):
        """
        refresh the query
        """       
        session = Session()
        bill_id = self.context.bill_id
        connection = session.connection(domain.Bill)
        self.results = connection.execute( self._sql_timeline % {'item_id' : bill_id} )       
        path = absoluteURL( self.context, self.request ) 
        self.addurl = '%s/event/add' %( path )
         
    
    
    render = ViewPageTemplateFile ('templates/bill_timeline_viewlet.pt')    
