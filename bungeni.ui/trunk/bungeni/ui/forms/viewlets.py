# encoding: utf-8

from dateutil import relativedelta
import datetime, calendar

from zope.viewlet import viewlet
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.formlib.namedtemplate import NamedTemplate
from zope.traversing.browser import absoluteURL 
from zope.formlib import form
from zope.security.proxy import removeSecurityProxy

import sqlalchemy.sql.expression as sql

from alchemist import ui
from ore.alchemist import Session
from ore.alchemist.model import queryModelDescriptor

from bungeni.models import domain
from bungeni.models.utils import get_offices_held_for_user_in_parliament
from bungeni.ui.i18n import _
import bungeni.core.globalsettings as prefs
from bungeni.core.workflows.question import states as qw_state
from bungeni.ui.table import AjaxContainerListing
from bungeni.ui.queries import statements, utils
from bungeni.ui.utils import getDisplayDate

from fields import BungeniAttributeDisplay

class GroupIdViewlet(viewlet.ViewletBase):
    """ display the group and parent group
    principal id """
    parent_group_principal_id = None
    my_group_principal_id = None
    
    def __init__( self,  context, request, view, manager ):        

        self.context = context
        self.request = request
        self.__parent__= context
        self.manager = manager
        
    def update(self):
        session = Session()
        trusted = removeSecurityProxy(self.context)    
        self.parent_group_principal_id = ("group.parliament.%i" %              
                trusted.parent_group_id)
        self.my_group_principal_id = trusted.group_principal_id        
        
    render = ViewPageTemplateFile ('templates/group_id.pt')  


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
        md = queryModelDescriptor(domain.User)          
        self.form_fields=md.fields #.select('user_id', 'start_date', 'end_date')
        
    def update(self):
        """
        refresh the query
        """       
        session = Session()
        user_id = self.context.user_id
        parent = self.context.__parent__
        self.query = session.query(domain.User).filter(domain.User.user_id == user_id) 
        self.context = self.query.all()[0]
        self.context.__parent__= parent
        super( PersonInfo, self).update()

class SupplementaryQuestionsViewlet( SubformViewlet ):
    form_name = (u"Supplementary Questions")    
    
    @property
    def for_display(self):
        return self.context.__parent__.status == qw_state[u"answered"].id   
    
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

class OfficesHeldViewlet( viewlet.ViewletBase ):
    for_display = True                    
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.query = None            
     
    
    def update(self):
        """
        refresh the query
        """       
        trusted = removeSecurityProxy(self.context)        
        user_id = trusted.user_id                
        parliament_id = trusted.group_id
        self.offices_held = get_offices_held_for_user_in_parliament(
                user_id, parliament_id)
                        
         
    
    
    render = ViewPageTemplateFile ('templates/offices_held_viewlet.pt')    

        
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
        bill_id = self.context.bill_id
        self.results = utils.execute_sql(statements.sql_bill_timeline, item_id=bill_id)
        path = absoluteURL( self.context, self.request ) 
        self.addurl = '%s/event/add' %( path )
         
    
    
    render = ViewPageTemplateFile ('templates/bill_timeline_viewlet.pt')    


class DisplayViewlet(BungeniAttributeDisplay):
    """Display a target object; if the object is `None`, the user is
    prompted to add it."""

    render = ViewPageTemplateFile ('templates/display_form.pt')
    mode = 'view'
    for_display = True
    query = None
    factory = None
    has_data = False
    form_fields = form.Fields()

    add_action = form.Actions(
        form.Action(_(u"Add"), success='handle_add'),
        )

    def __init__( self,  context, request, view, manager):
        super(DisplayViewlet, self).__init__(
            context, request, view, manager)

        # set add url before we change context
        self.add_url = self.get_add_url()

        target = self.get_target()
        if target is None:
            self.status = _(u"No item has been set.")
        else:
            self.context = target
            self.has_data = True

            assert self.factory is not None
            descriptor = queryModelDescriptor(self.factory)
            self.form_fields = descriptor.fields

    def update(self):
        # only if there's data to display do we update using our
        # immediate superclass
        if self.has_data:
            super(DisplayViewlet, self).update()
        else:
            self.setupActions()
            super(form.SubPageDisplayForm, self).update()

    def handle_add(self, action, data):
        self.request.response.redirect(self.add_url)

    def get_add_url(self):
        raise NotImplementedError("Must be implemented by subclass.")

    def get_target(self):
        raise NotImplementedError("Must be implemented by subclass.")

    def set_target(self, target):
        raise NotImplementedError("Must be implemented by subclass.")

    def setupActions(self):
        if self.has_data:
            super(DisplayViewlet, self).setupActions()
        else:
            self.actions = self.add_action.actions

    @property
    def form_name(self):
        descriptor = queryModelDescriptor(self.factory)
        return descriptor.display_name

class SchedulingMinutesViewlet(DisplayViewlet):
    factory = domain.ScheduledItemDiscussion

    def get_target(self):
        return self.context.discussion

    def set_target(self, target):
        self.context.discussion = target

    def get_add_url(self):
        return '%s/discussions/add' % absoluteURL(
            self.context, self.request)
            
            
class SessionCalendarViewlet( viewlet.ViewletBase ):
    """
    display a monthly calendar with all sittings for a session
    """
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.query = None
        self.Date=datetime.date.today()
        self.Data = []
        session = Session()
        self.type_query = session.query(domain.SittingType)        

    def _getDisplayDate(self, request):
        display_date = getDisplayDate(self.request)                    
        session = self.context
        if display_date:
            if session.end_date:
                if display_date > session.end_date:
                    display_date = session.end_date
            if session.start_date > display_date:
                display_date = session.start_date
        else:
            display_date = session.end_date                            
        return display_date                            
        
    def current_sittings_query(self, date):
        session = removeSecurityProxy(self.context)
        group_id = session.parliament_id
        start_date = session.start_date
        if start_date.month < date.month:
            start_date = datetime.date(date.year, date.month, 1)
        end_date = session.end_date
        if end_date:
            if end_date.month > date.month:
                end_date = date + relativedelta.relativedelta(day=31)
        else:
            end_date = date + relativedelta.relativedelta(day=31)                                                   
        session = Session()

        s_filter = sql.and_(
                domain.GroupSitting.group_id == group_id,
                sql.between(                        
                    domain.GroupSitting.start_date,
                    start_date, end_date)
                    )            
        return session.query(domain.GroupSitting).filter(s_filter).order_by(
                domain.GroupSitting.start_date)
        

    def previous(self):
        """
        return link to the previous month 
        if the session start date is prior to the current month
        """                   
        session = self.context
        if self.Date.month == 1:
            month = 12
            year = self.Date.year - 1
        else:
            month = self.Date.month -1
            year = self.Date.year  
        try:
            prevdate = datetime.date(year,month,self.Date.day)
        except:
            # in case we try to move to Feb 31st (or so)                      
            prevdate = datetime.date(year,month,15)                   
        if session.start_date < datetime.date( 
                self.Date.year, self.Date.month, 1):            
            return ('<a href="?date=' 
                + datetime.date.strftime(prevdate,'%Y-%m-%d') 
                + '"> &lt;&lt; </a>' )
        else:
            return ""
        
    def next(self):
        """
        return link to the next month if the end date
        of the session is after the 1st of the next month
        """        
        session = self.context
        if self.Date.month == 12:
            month = 1
            year = self.Date.year + 1
        else:
            month = self.Date.month + 1
            year = self.Date.year        
        try:
            nextdate = datetime.date(year,month,self.Date.day)
        except:
            # if we try to move from 31 of jan to 31 of feb or so
            nextdate = datetime.date(year,month,15)    
        if session:
            if session.end_date:
                if session.end_date < datetime.date(year,month,1):
                    return ""                                                
        return ('<a href="?date=' 
                + datetime.date.strftime(nextdate,'%Y-%m-%d' )
                + '"> &gt;&gt; </a>' )


    def getData(self):
        """
        return the data of the query
        """
        sit_types ={}
        type_results = self.type_query.all()
        for sit_type in type_results:
            sit_types[sit_type.sitting_type_id] = sit_type.sitting_type
        data_list=[]      
        path = '/calendar/group/sittings/'       
        results = self.query.all()
        for result in results:            
            data ={}
            data['sittingid']= ('sid_' + str(result.sitting_id) )     
            data['sid'] =  result.sitting_id                   
            data['short_name'] = ( datetime.datetime.strftime(result.start_date,'%H:%M')
                                    + ' - ' + datetime.datetime.strftime(result.end_date,'%H:%M')
                                    + ' (' + sit_types[result.sitting_type_id] + ')')
            data['start_date'] = result.start_date
            data['end_date'] = result.end_date
            data['start_time'] = result.start_date.time()
            data['end_time'] = result.end_date.time()            
            data['day'] = result.start_date.date()
            data['url']= ( path + 'obj-' + str(result.sitting_id) )   
            data['did'] = ('dlid_' +  datetime.datetime.strftime(result.start_date,'%Y-%m-%d') +
                           '_stid_' + str( result.sitting_type))                                                
            data_list.append(data)            
        return data_list

    def getTdId(self, Date):
        """
        return an Id for that td element:
        consiting of tdid- + date
        like tdid-2008-01-17
        """
        return 'tdid-' + datetime.date.strftime(Date,'%Y-%m-%d') 

    def getDayClass(self, Date):
        """
        return the class settings for that calendar day
        """
        css_class = ""
        if self.Date.month != Date.month:
            css_class = css_class + "other-month "           
        if Date < datetime.date.today():
            css_class = css_class + "past-date "    
        if Date == datetime.date.today():
            css_class = css_class + "current-date "  
        if Date.weekday() in prefs.getWeekendDays():
            css_class = css_class + "weekend-date "             
        session = Session()    
        query = session.query(domain.HoliDay).filter(domain.HoliDay.holiday_date == Date)
        results = query.all()
        if results:        
            css_class = css_class + "holyday-date "          
        return css_class.strip()
            
    def getWeekNo(self, Date):
        """
        return the weeknumber for a given date
        """
        return Date.isocalendar()[1]


    def getSittings4Day(self, Date):
        """
        return the sittings for that day
        """
        day_data=[]      
        for data in self.Data:
            if data['day'] == Date:
                day_data.append(data)
        return day_data                
        

    def update(self):
        """
        refresh the query
        """                
        self.Date = self._getDisplayDate(self.request)
        if not self.Date:
            self.Date=datetime.date.today()                            
        self.query = self.current_sittings_query(self.Date)               
        self.monthcalendar = calendar.Calendar(prefs.getFirstDayOfWeek()).monthdatescalendar(self.Date.year,self.Date.month)         
        self.monthname = datetime.date.strftime(self.Date,'%B %Y')
        self.Data = self.getData()
    
    render = ViewPageTemplateFile ('templates/session_calendar_viewlet.pt')            
