# encoding: utf-8
from zope.viewlet import viewlet
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.formlib.namedtemplate import NamedTemplate
from zope.traversing.browser import absoluteURL 
from zope.formlib import form

from alchemist import ui

from ore.alchemist import Session
from ore.alchemist.model import queryModelDescriptor

import bungeni.models.domain as domain

from bungeni.ui.i18n import _
from bungeni.core.workflows.question import states as qw_state
from bungeni.ui.table import AjaxContainerListing
from bungeni.ui.queries import sqlstatements


from fields import BungeniAttributeDisplay

class ResponseQuestionViewlet(viewlet.ViewletBase):    
    """
    Display the question when adding/editing a response
    """
    def __init__( self,  context, request, view, manager ):        

        self.context = context
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None
        self.subject = ''
        self.question_text = ''
    
    def update(self):
        if self.context.__class__ == domain.Response:
            #edit response
            question_id = self.context.response_id
            session = Session()
            return session.query(domain.Question).get(question_id)
            self.subject = self.context.__parent__.__parent__.subject
            self.question_text = self.context.__parent__.__parent__.question_text
        else:
            # add a response
            if self.context.__parent__.__class__ == domain.Question:
                self.subject = self.context.__parent__.subject
                self.question_text = self.context.__parent__.question_text

    render = ViewPageTemplateFile ('templates/question.pt')  
    
    
class AttributesEditViewlet(ui.core.DynamicFields, ui.viewlet.EditFormViewlet):
    mode = "edit"
    template = NamedTemplate('alchemist.subform')
    form_name = _(u"General")

class SubformViewlet ( AjaxContainerListing ):
    """
    
    """
    render = ViewPageTemplateFile ('templates/generic-sub-container.pt')  
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

class SupplementaryQuestionsViewlet( SubformViewlet ):
    form_name = (u"Supplementary Questions")    
    
    @property
    def for_display(self):
        return self.context.__parent__.status == qw_state[u"questionstates.answered"].id   
    
    def __init__( self,  context, request, view, manager ):        

        self.context = context.supplementaryquestions
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None
        #self.form_name = (u"Supplementary Questions")    


class InitialQuestionsViewlet( BungeniAttributeDisplay ):
    form_name = (u"Initial Questions")

    
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
    """Response to question."""

    mode = "view"
    for_display = True
    
    form_name = _(u"Response")   
    
    add_action = form.Actions(
        form.Action(_(u'Add response'), success='handle_response_add_action'),
        )
    
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.query = None
        md = queryModelDescriptor(domain.Response)          
        self.form_fields=md.fields
        self.add_url = '%s/responses/add' % absoluteURL(
            self.context, self.request)
        
    def handle_response_add_action(self, action, data):
        self.request.response.redirect(self.add_url)
        
    def update(self):
        context = self.context
        responses = context.responses        
        if len(responses):
            self.context = tuple(responses.values())[0]
            self.has_data = True
        else:
            self.context =  domain.Response()
            self.has_data = False
            
        super(ResponseViewlet, self).update()
        
    def setupActions(self):
        if self.has_data:
            super(ResponseViewlet, self).setupActions()
        else:
            self.actions = self.add_action.actions
        
class BillTimeLineViewlet( viewlet.ViewletBase ):
    """
    tracker/timeline view:

    Chronological changes are aggregated from : bill workflow, bill
    audit, bill scheduling and bill event records. 
    """
    add_action = form.Actions( form.Action(_(u'add event'), success='handle_event_add_action'), )
    for_display = True    
    # sqlalchemy give me a rough time sorting a union, with hand coded sql it is much easier.
 
                
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
        self.results = connection.execute( sqlstatements.sql_bill_timeline % {'item_id' : bill_id} )       
        path = absoluteURL( self.context, self.request ) 
        self.addurl = '%s/event/add' %( path )
         
    
    
    render = ViewPageTemplateFile ('templates/bill_timeline_viewlet.pt')    
