# encoding: utf-8
from zope.viewlet import viewlet
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.formlib.namedtemplate import NamedTemplate
from zope.traversing.browser import absoluteURL 
from zope.formlib import form

import sqlalchemy.sql.expression as sql

from alchemist import ui
from ore.alchemist import Session
from ore.alchemist.model import queryModelDescriptor

from bungeni.models import domain, interfaces, venue, schema
from bungeni.ui.i18n import _
from bungeni.core.workflows.question import states as qw_state
from bungeni.ui.table import AjaxContainerListing
from bungeni.ui.queries import statements, utils
from bungeni.ui.utils import makeList
import datetime
import bungeni.ui.recurring as recurring

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

class RecurringEventsViewlet(DisplayViewlet):
    render = ViewPageTemplateFile ('templates/recurrence.pt')
    date = None
    time = None
    errors= {}
    def get_add_url(self):
        return ''          
    def get_target(self):
        pass

    def set_target(self, target):
        pass
               
    def get_errors(self):
        errors = []
        for k in self.errors.keys():
            errors.append({'field': k, 'msg': self.errors[k] })
        return errors            
        
    def get_field_error(self, field):
        return errors.get(field, None)

    def get_overlapping_sittings(self, group_id, start, end, sitting=None):
        session = Session()
        b_filter = sql.and_(
                    sql.or_( 
                        sql.between(schema.sittings.c.start_date, start, end), 
                        sql.between(schema.sittings.c.end_date, start, end),
                        sql.between(start, schema.sittings.c.start_date, 
                                    schema.sittings.c.end_date),
                        sql.between(end, schema.sittings.c.start_date, 
                                    schema.sittings.c.end_date)                    
                        ),
                        schema.sittings.c.group_id == group_id)                        
        if sitting:
            if sitting.sitting_id:
                b_filter = sql.and_(b_filter,
                        schema.sittings.c.sitting_id != sitting.sitting_id)
        query = session.query(domain.GroupSitting).filter(b_filter)
        return query.all()
                
    def validate_sitting_dates(self, group_id, start, end, sitting=None):
        """ Sittings cannot overlap for one group    
        and must be inside the groups start end dates"""
        session = Session()
        group = session.query(domain.Group).get(group_id)
        if start.date() < group.start_date:
            self.errors['sitting_date'] = _(
                u"A sitting canno be scheduled before the groups start date")
        if group.end_date:                
            if end.date() > group.end_date:
                self.errors['sitting_date'] = _(
                    u"A sitting canno be scheduled after the groups end date")
        results = self.get_overlapping_sittings(group_id, start, end, sitting)
        for result in results:
            self.errors['start_time'] = _(
                u"Another sitting is already scheduled for this time")                    
            
    def get_groups(self):
        if interfaces.IGroupSitting.providedBy(self.context):
            group_id = self.context.group_id
        else:
            group_id = getattr(self.context.__parent__, 'group_id', None)
        session = Session()
        query = session.query(domain.Group).filter(
                sql.or_(
                    sql.between(self.date, domain.Group.start_date, 
                            domain.Group.end_date),
                    sql.and_(domain.Group.start_date < self.date,
                            domain.Group.end_date == None)
                            )                                                   
                        )
                            
        results = query.all()
        groups = []
        for result in results:                             
            groups.append({'name' : result.short_name,
                            'id' : result.group_id,
                            "selected" : None})
            if result.group_id == group_id:
                 groups[-1]["selected"] = u"selected"                                            
        return groups                            
            
    def get_start_time(self):
        if interfaces.IGroupSitting.providedBy(self.context):
            time = self.context.start_date.time()
        else:            
            time = self.time
        return datetime.time.strftime(time, "%H:%M")
        
    def get_end_time(self):
        if interfaces.IGroupSitting.providedBy(self.context):
            time = self.context.end_date.time()
        else:            
            time = self.time 
        return datetime.time.strftime(time, "%H:%M")
        
    def get_date(self):
        if interfaces.IGroupSitting.providedBy(self.context):
            date = self.context.start_date.date()
        else:            
            date = self.date
        return date

    def get_sitting_types(self):
        if interfaces.IGroupSitting.providedBy(self.context):
            stid = self.context.sitting_type_id    
        session=Session()
        query = session.query(domain.SittingType)
        results=query.all()
        sitting_types = []
        for result in results:
            sitting_types.append({"id": result.sitting_type_id,
                    "name" :  "%s (%s-%s)" % (
                    result.sitting_type.capitalize(), 
                    result.start_time, result.end_time),
                    "selected" : None})
            if result.sitting_type_id == stid:
                sitting_types[-1]["selected"] = u"selected"                                
        return sitting_types
        
    def get_venues(self):
        if interfaces.IGroupSitting.providedBy(self.context):
            vid = self.context.venue_id
        else:
            vid = None                
        session = Session()
        query= session.query(domain.Venue)
        results = query.all()
        if vid:
            venues = [{'id' : None, 'name': _(u"(no value)"), 'selected' : None}]        
        else:
            venues = [{'id' : None, 'name': _(u"(no value)"), 'selected' : u'selected'}]        
        for result in results:            
            venues.append({"id" : result.venue_id,
                        "name": result.short_name, 
                        'selected' : None})
            if vid == result.venue_id:
                venues[-1]['selected'] = u"selected"                        
        return venues            

    def get_weekdays(self):
        if interfaces.IGroupSitting.providedBy(self.context):
            cwd = self.context.start_date.weekday()
        else:
            cwd = self.date.weekday()
                        
        weekdays =[{'daynum' : 0, 'name' : u"Mon", 'checked' : None, 'disabled' : None},
            {'daynum' : 1, 'name' : u"Tue", 'checked' : None, 'disabled' : None},
            {'daynum' : 2, 'name' : u"Wed", 'checked' : None, 'disabled' : None},
            {'daynum' : 3, 'name' : u"Thu", 'checked' : None, 'disabled' : None},
            {'daynum' : 4, 'name' : u"Fri", 'checked' : None, 'disabled' : None},
            {'daynum' : 5, 'name' : u"Sat", 'checked' : None, 'disabled' : None},
            {'daynum' : 6, 'name' : u"Sun", 'checked' : None, 'disabled' : None}]
        weekdays[cwd]['checked'] = u"checked"
        weekdays[cwd]['disabled'] = u"disabled"
        return weekdays
        
    def get_monthday(self):
        """ Day 3 of every month """        
        return u"Day %i of every month" % self.context.start_date.day        

    def get_nth_monthday(self):
        """ 1st Friday of every month """
        dayname = self.context.start_date.strftime('%A')        
        daylist = []
        for day in recurring.nth_weekday_in_month(self.context.start_date):
            legend = u"%s %s of every month" % ( day['name'], dayname )
            daylist.append({'daynum': day['daynum'], 'name' : legend  })
        return daylist
   
    def update(self):
        self.errors = {}
        if self.request.form:
            timestamp = self.request.form.get('timestamp', None)
            if timestamp:
                dt = datetime.datetime.fromtimestamp(float(timestamp))
                self.date = dt.date()
                self.time = dt.time()
            else:
                self.date = datetime.datetime.today()
                self.time = datetime.datetime.now().time()         
            if interfaces.IGroupSitting.providedBy(self.context):                
                sitting = self.context
                self.date = sitting.start_date.date()
                self.time = sitting.start_date.time()
            else:
                sitting = None
            if self.request.form.has_key('save'):     
                session = Session()                                     
                sitting_type_id = self.request.form.get('sitting_type_id', None)
                try:
                    sitting_type_id = long(sitting_type_id)
                except:
                    self.errors['sitting_type_id'] = _(u"sitting_type must be set")
                sitting_date = self.request.form.get('sitting_date', None)
                sitting_start_time = self.request.form.get('sitting_start_time', None)
                sitting_end_time = self.request.form.get('sitting_end_time', None)
                group_id = self.request.form.get('group_id', None)
                exceptions = self.request.form.get('exceptions', None)
                if group_id:
                    group_id = long(group_id) 
                else:    
                    if interfaces.IGroupSitting.providedBy(self.context):
                        group_id = self.context.group_id
                    else:
                        group_id = getattr(self.context.__parent__, 'group_id', None)                                                   
                venue_id = self.request.form.get('venue_id', None)
                if venue_id:
                    try:
                        venue_id = long(venue_id)
                    except:
                        venue_id = None                           
                try:
                    sitting_date = datetime.datetime.strptime(sitting_date,"%Y-%m-%d")
                except:
                    self.errors['sitting_date'] = _(u"Invalid value for date")
                try:                
                    sitting_start_time = datetime.datetime.strptime(sitting_start_time, "%H:%M")
                except:
                    self.errors['sitting_start_time'] = _(u"Invalid value for time")
                try:                  
                    sitting_end_time = datetime.datetime.strptime(sitting_end_time, "%H:%M")
                except:
                    self.errors['sitting_end_time'] = _(u"Invalid value for time")
                try:                  
                    start_date = datetime.datetime(sitting_date.year, 
                                                    sitting_date.month, 
                                                    sitting_date.day,
                                                    sitting_start_time.hour,
                                                    sitting_start_time.minute)
                                                    
                    end_date = datetime.datetime(sitting_date.year, 
                                                    sitting_date.month, 
                                                    sitting_date.day,
                                                    sitting_end_time.hour,
                                                    sitting_end_time.minute)
                except:
                    pass                                                            
                recurrence =  self.request.form.get('recurrence', None)
                rrange =  self.request.form.get('range', None)
                count =  self.request.form.get('count', None)
                until =  self.request.form.get('until', None)
                if recurrence:
                    if rrange == 'count':
                        try:
                            count = int(count)
                            until = None
                        except:
                            self.errors['count'] = _(u"must be a number")                                                                           
                    elif rrange == 'until':
                        try:
                            until = datetime.datetime.strptime(until,"%Y-%m-%d")
                            count = None
                        except:
                            self.errors['until'] = _(u"Invalid value for date")   
                    if exceptions:
                        pass
                                                             
                if recurrence == "weekly":
                    days = makeList(self.request.form.get('weekdays',[]))
                    weekdays = []
                    for day in days:
                        weekdays.append(int(day))
                    try:                        
                        weekdays.append(sitting_date.weekday())                                                                 
                    except:
                        pass
                                                
                elif recurrence == "monthly":
                    monthly = self.request.form.get('monthly', None)
                    if monthly == "monthday":
                        try:
                            daynum = sitting_date.day
                            weekday = None
                        except:
                            pass                        
                    else:
                        monthly = int(monthly)
                        try:
                            weekday = sitting_date.weekday()                                        
                            daynum = None
                        except:
                            pass                                            
                if self.errors == {}:
                    if start_date > end_date:
                        self.errors['sitting_start_time'] = _(u"Sitting start must be before end")
                        self.errors['sitting_end_time'] = _(u"Sitting end must be after start")                            
                    if venue_id:                        
                        sitting_venue=session.query(domain.Venue).get(venue_id)
                        if not venue.check_availability( start_date, end_date, sitting_venue, sitting):
                            self.errors['venue_id'] = _(u"This venue is already booked")    
                    self.validate_sitting_dates(group_id, start_date, end_date, sitting)                                                                         
                if self.errors == {}:
                    if sitting is None:                                                
                        sitting = domain.GroupSitting()
                        sitting.start_date =  start_date
                        sitting.end_date = end_date
                        sitting.venue_id = venue_id
                        sitting.sitting_type_id = sitting_type_id
                        sitting.group_id = group_id 
                        session.add(sitting)
                    else:
                        sitting.start_date =  start_date
                        sitting.end_date = end_date
                        sitting.venue_id = venue_id
                        sitting.sitting_type_id = sitting_type_id
                        sitting.group_id = group_id 
                    session.flush()
                    dates = None
                    if recurrence == "weekly":  
                        dates = recurring.getWeeklyScheduleDates(
                            sitting_date, 
                            weekdays,  
                            end=until, 
                            times=count, 
                            edates=[])['valid']
                    elif recurrence == "monthly":
                        dates = getMonthlyScheduleDates(sitting_date, 
                            monthday=daynum, 
                            nth=monthly, 
                            weekday=weekday,  
                            end=until, 
                            times=count, 
                            edates=[])['valid']
                    if dates:    
                        recurring.create_recurrent_sittings( dates, sitting)
                    session.flush()                                                                                                                
            
        else:
            self.date = datetime.datetime.today()
            self.time = datetime.datetime.now().time()               
