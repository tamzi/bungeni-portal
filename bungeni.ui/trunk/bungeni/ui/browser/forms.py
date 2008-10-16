
# encoding: utf-8

import pdb

from zope import component

from ore.alchemist.vocabulary import DatabaseSource
from ore.alchemist.model import queryModelDescriptor
from ore.alchemist import Session
from ore.workflow import interfaces

from alchemist.ui.content import ContentAddForm, ContentDisplayForm
from alchemist.ui.viewlet import EditFormViewlet, AttributesViewViewlet, DisplayFormViewlet
from alchemist.ui.core import DynamicFields, null_validator, handle_edit_action

from zope.formlib import form, namedtemplate
from zope import schema, interface
from zope.formlib.namedtemplate import NamedTemplate
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.traversing.browser import absoluteURL 
from zope.security.proxy import removeSecurityProxy
from zope.security.permission import checkPermission
import zope.security.management

import bungeni.core.vocabulary as vocabulary
import bungeni.core.domain as domain
from bungeni.core.i18n import _
from bungeni.core.interfaces import IGroupSitting, IParliamentSession, IMemberOfParliament, \
    ICommittee, ICommitteeMember, IGovernment, IMinistry, IExtensionGroup, IMinister, \
    IExtensionMember, IParliament, IGroupSittingAttendance, ICommitteeStaff, IMemberRoleTitle, \
    IMemberOfParty, IPoliticalParty, IQuestion, IResponse

import bungeni.core.workflows.utils
from bungeni.core.workflows.question import states as question_states
import bungeni.core.globalsettings as prefs

from bungeni.ui.datetimewidget import  SelectDateTimeWidget, SelectDateWidget
from bungeni.ui import widget
#from bungeni.ui.workflow import bindTransitions


from ore.yuiwidget import calendar

import validations

from bungeni.core.interfaces import IVersioned 

def createVersion(context, comment = ''):
    """Create a new version of an object and return it."""
    instance = removeSecurityProxy(context)
    versions = IVersioned(instance)
    if not comment:
        comment =''
    versions.create(u'New version created upon edit.' + comment)


#################################
# workflow transition 2 formlib action bindings
class TransitionHandler( object ):

    def __init__( self, transition_id, wf_name=None):
        self.transition_id = transition_id
        self.wf_name = wf_name


    def __call__( self, form, action, data ):
        """
        save data make version and fire transition
        """
        context = getattr( form.context, '_object', form.context )
        notes = None
        if self.wf_name:
            info = component.getAdapter( context, interfaces.IWorkflowInfo, self.wf_name )            
        else:
            info = interfaces.IWorkflowInfo( context ) 
        if data.has_key('note'):
            notes = data['note']     
        else:
            notes=''            
        result = handle_edit_action( form, action, data )
        if form.errors: 
            return result
        else:         
            createVersion(form.context, notes)                                                        
            info.fireTransition( self.transition_id, notes )       
            url = absoluteURL( form.context, form.request )  
            return form.request.response.redirect( url )             
        #form.setupActions()

def bindTransitions( form_instance, transitions, wf_name=None, wf=None):
    """ bind workflow transitions into formlib actions 
    """

    if wf_name:
        success_factory = lambda tid: TransitionHandler( tid, wf_name )
    else:
        success_factory = TransitionHandler

    actions = []
    for tid in transitions:
        d = {}
        if success_factory:
            d['success'] = success_factory( tid )
        if wf is not None:
            action = form.Action( _(unicode(wf.getTransitionById( tid ).title)), **d )
        else:
            action = form.Action( tid, **d )
        action.form = form_instance
        action.__name__ = "%s.%s"%(form_instance.prefix, action.__name__)
        
        actions.append( action )  
    return actions





#############
## VIEW


#############
# Generic Custom View form


        
class BungeniAttributeDisplay( DynamicFields, DisplayFormViewlet ):
    
    mode = "view"
    template = ViewPageTemplateFile('templates/display_form.pt')        
    form_name = _(u"General")    
    has_data = True


    def setupActions( self ):
        try:
            self.wf = interfaces.IWorkflowInfo( self.context )
            transitions = self.wf.getManualTransitionIds()
            self.actions = tuple(bindTransitions( self, transitions, None, interfaces.IWorkflow( self.context ) ) )  
        except:
            pass
            
    def update( self ):
        self.form_name = self.getform_name()
        self.setupActions() 
        super( BungeniAttributeDisplay, self).update() 
        self.setupActions()  # after we transition we have different actions  
        try:
            wf_state =interfaces.IWorkflowState( removeSecurityProxy(self.context) ).getState()
            self.wf_status = wf_state  
        except:
            pass
               
    def getform_name( self ):
        try:
            if self.context.__parent__:
                descriptor = queryModelDescriptor( self.context.__parent__.domain_model )
            else:
                return self.form_name
        except:
            return self.form_name                        
        if descriptor:
            name = getattr( descriptor, 'display_name', None)
        if not name:
            name = getattr( self.context.__parent__.domain_model, '__name__', None)                
        return name #"%s %s"%(name, self.mode.title())



#questions
#class QuestionDisplay( BungeniAttributeDisplay ):
    
#    respond_action = form.Actions( form.Action( _(u"Respond"), success='handle_respond_action'), )
    
#    def handle_respond_action( self, action, data ):
#        """ the respond action will create a response to the question"""
#        url = absoluteURL( self.context, self.request )  + '/responses/add'
#        return self.request.response.redirect( url )
    
#    def update( self ):
#        """
#        if the question is in the state 'Question pending response' 
#        display a create answer button
#        """
#        if self.context.status == question_states.response_pending :
#            self.actions = self.respond_action
#        super(QuestionDisplay, self).update()

#    def update( self ):
#        self.setupActions()  
#        super( QuestionDisplay, self).update()
#        self.setupActions()  # after we transition we have different actions      
#        wf_state =interfaces.IWorkflowState( removeSecurityProxy(self.context) ).getState()
#        self.wf_status = wf_state            
        

        
#############
## ADD 

##################


   


#####################
# Generic Custom Add Form

class CustomAddForm( ContentAddForm ):
    """
    Override the autogenerated Add form for custom behaviour
    """
    Adapts = {} 
    CustomValidation = None

    def update( self ):
         self.status = self.request.get('portal_status_message','')
         form.AddForm.update( self )
         set_widget_errors(self.widgets, self.errors)
         

    def finishConstruction( self, ob ):
        """
        adapt the custom fields to the object
        """
        self.adapters = { self.Adapts : ob }    
         
             
    def validate(self, action, data):    
        """
        validation that require context must be called here,
        invariants may be defined in the descriptor
        """                                          
        return (form.getWidgetsData(self.widgets, self.prefix, data) +
                 form.checkInvariants(self.form_fields, data) +
                 self.CustomValidation( self.context, data ) )  
    
    
    @form.action(_(u"Save"), condition=form.haveInputWidgets)
    def handle_add_save(self, action, data ):
        """
        After succesfull creation of the content we are back at the listing
        """
        self.createAndAdd( data )
        name = self.context.domain_model.__name__
        self._next_url = absoluteURL( self.context, self.request ) + '?portal_status_message=%s Added'%name    
        
    @form.action(_(u"Cancel"), validator=null_validator )
    def handle_cancel( self, action, data ):
        """
        takes us back to the listing
        """
        url = self.nextURL()
        return self.request.response.redirect( url )
        
    @form.action(_(u"Save and continue editing"), condition=form.haveInputWidgets, validator='validateAdd')
    def handle_add_edit( self, action, data ):
        ob = self.createAndAdd( data )
        name = self.context.domain_model.__name__
        self._next_url = absoluteURL( ob, self.request ) + "/@@edit?portal_status_message=%s Added"%name
        
    @form.action(_(u"Save and add another"), condition=form.haveInputWidgets)
    def handle_add_and_another(self, action, data ):
        self.createAndAdd( data )
        name = self.context.domain_model.__name__
        self._next_url = absoluteURL( self.context, self.request ) + '/@@add?portal_status_message=%s Added'%name        



#parliament        
class ParliamentAdd( CustomAddForm ):
    """
    custom Add form for parliaments
    """
    form_fields = form.Fields( IParliament )
    form_fields["start_date"].custom_widget = calendar.CalendarWidget
    #form_fields["end_date"].custom_widget = SelectDateWidget  
    form_fields["election_date"].custom_widget = calendar.CalendarWidget
    form_fields["description"].custom_widget=widget.RichTextEditor
    Adapts = IParliament
    CustomValidation = validations.CheckParliamentDatesAdd  
    
class PoliticalPartyAdd( CustomAddForm ):
    """
    custom Add form for parliaments
    """
    form_fields = form.Fields( IPoliticalParty )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget  
    form_fields["description"].custom_widget=widget.RichTextEditor
    Adapts = IPoliticalParty
    CustomValidation = validations.checkPartyDates

# party membership



class PartyMemberAdd( CustomAddForm ):
    """
    add a person to a party
    """
    #XXX

class MemberOfPartyAdd( CustomAddForm ):
    """
    add a partymembership to a person
    """
    #XXX
    form_fields = form.Fields( IMemberOfParty )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget
    form_fields["notes"].custom_widget=widget.RichTextEditor
    Adapts = IMemberOfParty    
    CustomValidation = validations.checkPartyMembershipDates


# ministries
class MinistryAdd( CustomAddForm ):
    """
    custom Add form for ministries
    """
    form_fields = form.Fields( IMinistry )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget
    Adapts = IMinistry
    CustomValidation =  validations.CheckMinistryDatesInsideGovernmentDatesAdd     
                      

                 
#ministers


sql_addMinister = """
                SELECT DISTINCT "users"."titles" || ' ' || "users"."first_name" || ' ' || "users"."middle_name" || ' ' || "users"."last_name" as fullname, 
                        "users"."user_id", "users"."last_name" 
                FROM "public"."ministries", "public"."government", "public"."parliaments", 
                    "public"."user_group_memberships", "public"."users" 
                WHERE ( "ministries"."government_id" = "government"."government_id" 
                    AND "government"."parliament_id" = "parliaments"."parliament_id" 
                    AND "user_group_memberships"."group_id" = "parliaments"."parliament_id" 
                    AND "user_group_memberships"."user_id" = "users"."user_id" ) 
                    AND ( "user_group_memberships"."active_p" = True AND "ministries"."ministry_id" = %(primary_key)s )
                    AND ( "users"."user_id" NOT IN ( SELECT "user_id" 
                                                                FROM "public"."user_group_memberships" 
                                                                WHERE ( "group_id"  = %(primary_key)s 
                                                                        AND "active_p" = True) 
                                                                )                                           
                                    ) 
                UNION
                SELECT DISTINCT "users"."titles" || ' ' || "users"."first_name" || ' ' || "users"."middle_name" || ' ' || "users"."last_name" as fullname, 
                        "users"."user_id", "users"."last_name" 
                FROM "public"."ministries", "public"."government", "public"."groups", 
                    "public"."extension_groups", "public"."user_group_memberships", "public"."users" 
                WHERE ( "ministries"."government_id" = "government"."government_id" 
                    AND "ministries"."ministry_id" = "groups"."group_id" 
                    AND "extension_groups"."group_type" = "groups"."type" 
                    AND "extension_groups"."extension_type_id" = "user_group_memberships"."group_id" 
                    AND "user_group_memberships"."user_id" = "users"."user_id" 
                    AND "extension_groups"."parliament_id" = "government"."parliament_id" ) 
                    AND ( "user_group_memberships"."active_p" = True AND "ministries"."ministry_id" = %(primary_key)s )
                    AND ( "users"."user_id" NOT IN ( SELECT "user_id" 
                                                                FROM "public"."user_group_memberships" 
                                                                WHERE ( "group_id"  = %(primary_key)s 
                                                                        AND "active_p" = True) 
                                                                )                                           
                                    )                                     
                ORDER BY "last_name"
                """

qryAddMinisterVocab = vocabulary.SQLQuerySource(sql_addMinister, 'fullname', 'user_id')

class IMinisterAdd( IMinister ):
    """
    override some fields with custom schema
    """
    user_id = schema.Choice(title=_(u"Minister"),  
                                source=qryAddMinisterVocab, 
                                required=True,
                                )
    
    
class MinistersAdd( CustomAddForm ):
    """
    custom Add form for ministries
    """
    form_fields = form.Fields( IMinisterAdd ).select(
                    'user_id', 
                    'start_date', 'end_date',
                    'notes')
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget
    form_fields["notes"].custom_widget=widget.RichTextEditor
    Adapts = IMinisterAdd
    CustomValidation =   validations.CheckMinisterDatesInsideMinistryDatesAdd    
                       
    
# government

class GovernmentAdd ( CustomAddForm ):
    """
    custom Add form for government
    """
    form_fields = form.Fields( IGovernment )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget 
    Adapts = IGovernment
    CustomValidation =  validations.CheckGovernmentsDateInsideParliamentsDatesAdd    
                      
   

# Extension groups

class ExtensionGroupAdd( CustomAddForm ):
    """
    override the AddForm for GroupSittingAttendance
    """
    form_fields = form.Fields( IExtensionGroup )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget 
    Adapts = IExtensionGroup
    CustomValidation =   validations.CheckExtensionGroupDatesInsideParentDatesAdd   
 



#XXX currently filters by "type" = 'memberofparliament' -> has to be replaced with all electable usertypes
sql_addExtensionMember = """
                        SELECT DISTINCT "users"."titles" || ' ' || "users"."first_name" || ' ' || "users"."middle_name" || ' ' || "users"."last_name" as fullname, 
                        "users"."user_id", "users"."last_name" 
                        FROM "public"."users" 
                        WHERE ( ( "active_p" = 'A' AND "type" = 'memberofparliament' )
                                AND ( "users"."user_id" NOT IN ( SELECT "user_id" 
                                                                FROM "public"."user_group_memberships" 
                                                                WHERE ( "group_id"  = %(primary_key)s 
                                                                        AND "active_p" = True) 
                                                                )                                           
                                    )
                                AND ( "users"."user_id" NOT IN (SELECT "user_group_memberships"."user_id" 
                                                                FROM "public"."user_group_memberships", "public"."extension_groups" 
                                                                WHERE ( "user_group_memberships"."group_id" = "extension_groups"."parliament_id" ) 
                                                                AND ( "extension_groups"."extension_type_id" = %(primary_key)s  
                                                                        AND "active_p" = True) 
                                                                )
                                    )         
                               )                    
                        ORDER BY "last_name"
                        """
qryAddExtensionMemberVocab = vocabulary.SQLQuerySource(sql_addExtensionMember, 'fullname', 'user_id')

class IExtensionMemberAdd( IExtensionMember ):
    """
    override some fields for extension group members
    """
    user_id = schema.Choice(title=_(u"Person"),  
                                source=qryAddExtensionMemberVocab, 
                                required=True,
                                )
                                
                                
# Members of extension Groups
class ExtensionMemberAdd( CustomAddForm ):
    """
    override the AddForm for GroupSittingAttendance
    """
    form_fields = form.Fields( IExtensionMemberAdd ).omit( "replaced_id", "substitution_type" )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget 
    form_fields["notes"].custom_widget=widget.RichTextEditor
    Adapts = IExtensionMemberAdd
    CustomValidation =  validations.CheckExtensionMemberDatesInsideParentDatesAdd    
                      

# CommitteeMemberAdd



sql_AddCommitteeMember = """
                        SELECT DISTINCT "users"."titles" || ' ' || "users"."first_name" || ' ' || "users"."middle_name" || ' ' || "users"."last_name" as fullname, 
                        "users"."user_id", "users"."last_name" 
                        FROM "public"."user_group_memberships", "public"."users", 
                             "public"."extension_groups", "public"."groups", 
                             "public"."committees", "public"."parliaments" 
                        WHERE ( "user_group_memberships"."user_id" = "users"."user_id" 
                                AND "extension_groups"."extension_type_id" = "user_group_memberships"."group_id" 
                                AND "extension_groups"."group_type" = "groups"."type" 
                                AND "committees"."committee_id" = "groups"."group_id" 
                                AND "committees"."parliament_id" = "parliaments"."parliament_id" 
                                AND "extension_groups"."parliament_id" = "parliaments"."parliament_id" ) 
                                AND ( "committees"."committee_id" = %(primary_key)s  AND "user_group_memberships"."active_p" = True )
                                AND ( "users"."user_id" NOT IN ( SELECT "user_id" 
                                                                FROM "public"."user_group_memberships" 
                                                                WHERE ( "group_id"  = %(primary_key)s 
                                                                        AND "active_p" = True) 
                                                                )                                           
                                    ) 
                        UNION
                        SELECT DISTINCT "users"."titles" || ' ' || "users"."first_name" || ' ' || "users"."middle_name" || ' ' || "users"."last_name" as fullname,  
                        "users"."user_id", "users"."last_name" 
                        FROM "public"."committees", "public"."parliaments", "public"."groups", 
                            "public"."user_group_memberships", "public"."users" 
                        WHERE ( "committees"."parliament_id" = "parliaments"."parliament_id" 
                                AND "parliaments"."parliament_id" = "groups"."group_id" 
                                AND "user_group_memberships"."group_id" = "groups"."group_id" 
                                AND "user_group_memberships"."user_id" = "users"."user_id" ) 
                                AND ( "user_group_memberships"."active_p" = True AND "committees"."committee_id" = %(primary_key)s )
                                AND ( "users"."user_id" NOT IN ( SELECT "user_id" 
                                                                FROM "public"."user_group_memberships" 
                                                                WHERE ( "group_id"  = %(primary_key)s 
                                                                        AND "active_p" = True) 
                                                                )                                           
                                    )
                        ORDER BY "last_name"
                        """

qryAddCommitteeMemberVocab = vocabulary.SQLQuerySource(sql_AddCommitteeMember, 'fullname', 'user_id')

class ICommitteeMemberAdd ( ICommitteeMember ):
    """
    override some fields with custom schema
    """
    user_id = schema.Choice(title=_(u"Member of Parliament"),  
                                source=qryAddCommitteeMemberVocab, 
                                required=True,
                                )
class CommitteeMemberAdd( CustomAddForm ):
    """
    override the AddForm for GroupSittingAttendance
    """
    form_fields = form.Fields( ICommitteeMemberAdd ).select(
                    'user_id', 
                    'start_date', 'end_date',
                    'notes')
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget
    form_fields["notes"].custom_widget=widget.RichTextEditor
    Adapts = ICommitteeMemberAdd
    CustomValidation =  validations.CheckCommitteeMembersDatesInsideParentDatesAdd     
                      
# committee staff

sql_AddCommitteeStaff = """                        
                        SELECT DISTINCT "users"."titles" || ' ' || "users"."first_name" || ' ' || "users"."middle_name" || ' ' || "users"."last_name" as fullname, 
                        "users"."user_id", "users"."last_name" 
                        FROM "public"."users" 
                        WHERE ( ( "active_p" = 'A' AND "type" = 'staff' )
                                AND ( "users"."user_id" NOT IN ( SELECT "user_id" 
                                                                FROM "public"."user_group_memberships" 
                                                                WHERE ( "group_id"  = %(primary_key)s 
                                                                        AND "active_p" = True) 
                                                                )                                           
                                    )                                   
                               )                    
                        ORDER BY "last_name"                       
                        """
                        
qryAddCommitteeStaffVocab = vocabulary.SQLQuerySource(sql_AddCommitteeStaff, 'fullname', 'user_id')

class ICommitteeStaffAdd ( ICommitteeStaff ):
    """
    override some fields with custom schema
    """
    user_id = schema.Choice(title=_(u"Staff Member"),  
                                source=qryAddCommitteeStaffVocab, 
                                required=True,
                                )
                                
class CommitteeStaffAdd( CustomAddForm ):
    """
    override the AddForm 
    """
    form_fields = form.Fields( ICommitteeStaffAdd ).select(
                    'user_id', 
                    'start_date', 'end_date',
                    'notes')
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget
    form_fields["notes"].custom_widget=widget.RichTextEditor
    Adapts = ICommitteeStaffAdd
    CustomValidation =  validations.CheckCommitteeMembersDatesInsideParentDatesAdd   


# Committees


class CommitteeAdd( CustomAddForm ):
    """
    override the AddForm for GroupSittingAttendance
    """
    form_fields = form.Fields( ICommittee )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget    
    form_fields["reinstatement_date"].custom_widget = SelectDateWidget 
    Adapts = ICommittee
    CustomValidation = validations.CheckCommitteesDatesInsideParentDatesAdd     
                      

# Members of Parliament



sql_AddMemberOfParliament = """
                            SELECT "titles" ||' ' || "first_name" || ' ' || "middle_name" || ' ' || "last_name" as fullname, "user_id" 
                            FROM "public"."users" 
                            WHERE ( ( "active_p" = 'A' ) 
                                AND ( "users"."user_id" NOT IN ( SELECT "user_id" 
                                                                FROM "public"."user_group_memberships" 
                                                                WHERE ( "group_id"  = %(primary_key)s 
                                                                        AND "active_p" = True) 
                                                                )                                           
                                    )
                                )
                            ORDER BY "users"."last_name"  
                            """
qryAddMemberOfParliamentVocab = vocabulary.SQLQuerySource(sql_AddMemberOfParliament, 'fullname', 'user_id')  

class IMemberOfParliamentAdd ( IMemberOfParliament ):
    """ Custom schema to override some autogenerated fields"""
    user_id = schema.Choice(title=_(u"Member of Parliament"),  
                                source=qryAddMemberOfParliamentVocab, 
                                required=True,
                                )


class MemberOfParliamentAdd( CustomAddForm ):
    """
    override the AddForm for GroupSittingAttendance
    """
    #form_fields = form.Fields( IMemberOfParliamentAdd ).omit( "replaced_id", "substitution_type" )
    form_fields = form.Fields( IMemberOfParliamentAdd ).select(
                    'user_id', 'start_date', 
                    'election_nomination_date', 'elected_nominated',  'constituency_id',
                    'end_date', 'leave_reason',
                    'notes')
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget 
    form_fields["start_date"].field.description = _(u"Begin of the parliamentary mandate")
    #form_fields["start_date"].field.title = _(u"Beginn of the parliamentary mandate")    
    form_fields["election_nomination_date"].custom_widget = SelectDateWidget   
    form_fields["notes"].custom_widget=widget.RichTextEditor 
    Adapts = IMemberOfParliamentAdd
    CustomValidation = validations.CheckMPsDatesInsideParentDatesAdd  
    
    def update( self ):      
        edate = getattr(self.context.__parent__, 'election_date', None)       
        if edate:
            self.form_fields["election_nomination_date"].field.default = edate                    
        sdate = getattr(self.context.__parent__, 'start_date', None)     
        if sdate:
            self.form_fields["start_date"].field.default = sdate                 
        super( MemberOfParliamentAdd, self ).update()  
    

# Sessions

    
class SessionAdd( CustomAddForm ):
    """
    override the AddForm for GroupSittingAttendance
    """
    form_fields = form.Fields( IParliamentSession )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget 
    Adapts = IParliamentSession
    CustomValidation =  validations.CheckSessionDatesInsideParentDatesAdd    
                      
 

# Sittings



class GroupSittingAdd( CustomAddForm ):
    """
    override the AddForm for GroupSittingAttendance
    """
    form_fields = form.Fields( IGroupSitting )
    form_fields["start_date"].custom_widget = SelectDateTimeWidget
    form_fields["end_date"].custom_widget = SelectDateTimeWidget
    Adapts = IGroupSitting
    CustomValidation =  validations.CheckSittingDatesInsideParentDatesAdd 
                      
        
     

sql_add_members ='''SELECT "users"."titles" || ' ' || "users"."first_name" || ' ' || "users"."middle_name" || ' ' || "users"."last_name" as user_name, 
                    "users"."user_id", "group_sittings"."sitting_id" 
                    FROM "public"."group_sittings", "public"."sessions", 
                    "public"."user_group_memberships", "public"."users" 
                    WHERE ( "group_sittings"."session_id" = "sessions"."session_id" 
                        AND "user_group_memberships"."group_id" = "sessions"."parliament_id" 
                        AND "user_group_memberships"."user_id" = "users"."user_id" )
                        AND ( "user_group_memberships"."active_p" = True )
                        AND ("group_sittings"."sitting_id" = %(primary_key)s)
                        AND ( "users"."user_id" NOT IN (SELECT member_id 
                                                        FROM sitting_attendance 
                                                        WHERE sitting_id = %(primary_key)s )                                           
                            )
                    ORDER BY "users"."last_name"                    
                    '''
membersAddVocab = vocabulary.SQLQuerySource(sql_add_members, 'user_name', 'user_id')      
attendanceVocab = DatabaseSource(domain.AttendanceType, 'attendance_type', 'attendance_id' )

# Sitting Attendance

class IGroupSittingAttendanceAdd( interface.Interface ):
    """ """
    member_id = schema.Choice(title=_(u"Member of Parliament"),  
                                source=membersAddVocab, 
                                required=True,
                                )
    attendance_id = schema.Choice( title=_(u"Attendance"),  
                                    source=attendanceVocab, 
                                    required=True,
                                    )  



class GroupSittingAttendanceAdd( ContentAddForm ):
    """
    override the AddForm for GroupSittingAttendance
    """
    form_fields = form.Fields( IGroupSittingAttendanceAdd )
                      
    def update(self):
        """
        Called by formlib after __init__ for every page update. This is
        the method you can use to update form fields from your class
        """        
        self.status = self.request.get('portal_status_message','')        
        form.AddForm.update( self )
        set_widget_errors(self.widgets, self.errors)
         
    def finishConstruction( self, ob ):
        """
        adapt the custom fields to the object
        """
        self.adapters = { IGroupSittingAttendanceAdd : ob }

sql_addMemberTitle = '''
                        SELECT "user_role_types"."sort_order" || ' - ' || "user_role_types"."user_role_name" AS "ordered_title", 
                        "user_role_types"."user_role_type_id"
                        FROM "public"."user_role_types", "public"."user_group_memberships" 
                        WHERE ( "user_role_types"."user_type" = "user_group_memberships"."membership_type" ) 
                            AND ( ( "user_group_memberships"."membership_id" = %(primary_key)s ) ) 
                        ORDER BY "user_role_types"."sort_order" ASC
                       '''
                                  
titleAddVocab =  vocabulary.SQLQuerySource(sql_addMemberTitle, 'ordered_title', 'user_role_type_id')

# Titles / Roles

     
class IMemberRoleTitleAdd( IMemberRoleTitle ):
    title_name_id = schema.Choice( title=_(u"Title"),  
                                    source=titleAddVocab, 
                                    required=True,
                                    )  
     
class MemberTitleAdd( CustomAddForm ):
    form_fields = form.Fields( IMemberRoleTitleAdd ).select('title_name_id', 'start_date', 'end_date')
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget
    Adapts = IMemberRoleTitleAdd
    CustomValidation =  validations.CheckMemberTitleDateAdd 


#def getMinistryDateFilter(Date):
#    return sql.or_(
#        sql.between(Date, domain.ministry.c.start_date, domain.ministry.c.end_date),
#        sql.and_( domain.ministry.c.start_date <= Date, domain.ministry.c.end_date == None)
#        )


sql_select_question_ministry_add = """
            SELECT "groups"."short_name", "groups"."full_name", "groups"."group_id"  
            FROM "public"."ministries" AS "ministries", "public"."groups" AS "groups" 
            WHERE "ministries"."ministry_id" = "groups"."group_id"
            AND ( (current_date between "groups"."start_date" and  "groups"."end_date")
                 OR ( ("groups"."start_date" < current_date) AND ("groups"."end_date" IS NULL))
                 )
            ORDER BY short_name
        """
        
qryAddQuestionMinistryVocab = vocabulary.SQLQuerySource(sql_select_question_ministry_add, 'full_name', 'group_id')
        
class IQuestionAdd ( IQuestion ):
    """ Custom schema to override some autogenerated fields"""
    ministry_id = schema.Choice(title=_(u"Ministry"),  
                                source=qryAddQuestionMinistryVocab, 
                                required=False,
                                )        

class QuestionAdd( CustomAddForm ):
    form_fields = form.Fields( IQuestionAdd ).select('question_type', 'response_type', 'owner_id', 'ministry_id',
                                                    'subject', 'question_text',                                                                  
                                                    'note', 'receive_notification' )

    Adapts = IQuestionAdd
    CustomValidation =  validations.QuestionAdd 
    form_fields["note"].custom_widget = widget.OneTimeEditor
    form_fields["question_text"].custom_widget = widget.RichTextEditor 

    def update( self ):      
        ministry_id = getattr(self.context.__parent__, 'ministry_id', None)   
        if self.context.__parent__.__class__  == domain.Question:    
        #if ministry_id:
            #self.form_fields["ministry_id"].field.default = ministry_id
            #self.form_fields["ministry_id"].for_display = True
            self.form_fields = self.form_fields.omit("ministry_id")
        super( QuestionAdd, self ).update()  

    def can_submit( self, action):
        result = form.haveInputWidgets( self, action)
        result = result and prefs.getQuestionSubmissionAllowed()
        return result

    @form.action(_(u"Save"), condition=form.haveInputWidgets)
    def handle_add_save(self, action, data ):
        """
        After succesfull creation of the content we are back at the listing
        """
        self.createAndAdd( data )
        name = self.context.domain_model.__name__
        self._next_url = absoluteURL( self.context, self.request ) + '?portal_status_message=%s Added'%name    
        
    @form.action(_(u"Cancel"), validator=null_validator )
    def handle_cancel( self, action, data ):
        """
        takes us back to the listing
        """
        url = self.nextURL()
        return self.request.response.redirect( url )
        
    @form.action(_(u"Save and continue editing"), condition=form.haveInputWidgets, validator='validateAdd')
    def handle_add_edit( self, action, data ):
        ob = self.createAndAdd( data )
        name = self.context.domain_model.__name__
        self._next_url = absoluteURL( ob, self.request ) + "/@@edit?portal_status_message=%s Added"%name
        
    @form.action(_(u"Save and add another"), condition=form.haveInputWidgets)
    def handle_add_and_another(self, action, data ):
        self.createAndAdd( data )
        name = self.context.domain_model.__name__
        self._next_url = absoluteURL( self.context, self.request ) + '/@@add?portal_status_message=%s Added'%name    
        
    @form.action(_(u"Save and submit to clerk"), condition=can_submit, validator='validateAdd')
    def handle_add_submit( self, action, data ):
        ob = self.createAndAdd( data )
        info = component.getAdapter( ob,  interfaces.IWorkflowInfo)
        if data.has_key('note'):
            notes = data['note']     
        else:
            notes=''                   
        createVersion(ob, notes)                                                                    
        info.fireTransition( 'submit-to-clerk', notes )                          
        name = self.context.domain_model.__name__
        self._next_url = absoluteURL( ob, self.request ) + "/?portal_status_message=%s Added"%name        
        
class ResponseAdd( CustomAddForm ):
    """
    Answer a Question
    UI for ministry to input response
    Display the question when adding the answer.
    """
    form_fields = form.Fields( IResponse ).select('response_text', 'sitting_time') 
    Adapts = IResponse
    form_fields["response_text"].custom_widget=widget.RichTextEditor 
    #form_fields["response_type"].custom_widget=widget.CustomRadioWidget
    CustomValidation =  validations.ResponseAdd
    template = ViewPageTemplateFile('templates/response-add.pt')     
        
##############
# Edit forms      
##############

##############
#Generic Custom Edit form   

####
# Display invariant errors /  custom validation errors in the context of the field
# that raised the error.

def set_widget_errors(widgets, errors):
    for widget in widgets:
        name = widget.context.getName()
        for error in errors:
            if isinstance(error, interface.Invalid) and name in error.args[1:]:
                if widget._error is None:
                    widget._error = error




def flag_changed_widgets( widgets, context, data):
    for widget in widgets:
        name = widget.context.getName()
        # If the field is not in the data, then go on to the next one
        if name not in data:
            widget.changed = False
            continue
        if data[name] == getattr(context, name):
            widget.changed = False
        else:
            widget.changed = True  
    return []                  

class CustomEditForm ( EditFormViewlet ):
    """
    Override the autogenerated Edit form for specific behaviour
    """  
    Adapts = None
    CustomValidations = None
    template = NamedTemplate('alchemist.subform')       
    
          
    def update( self ):
        """
        adapt the custom fields to our object
        """
        self.adapters = {self.Adapts  : self.context }    
        super( CustomEditForm, self).update()        
        set_widget_errors(self.widgets, self.errors)   
       
        
    def validate(self, action, data):    
        """
        validation that require context must be called here,
        invariants may be defined in the descriptor
        """                                          
        return (form.getWidgetsData(self.widgets, self.prefix, data) +
                 form.checkInvariants(self.form_fields, data) +
                 flag_changed_widgets( self.widgets, self.context, data) +     
                 self.CustomValidations( self.context, data) )  

    def invariantErrors( self ):        
        """ All invariant errors should be handled by the fields that raised them """
        return []    
    
    
    @form.action(_(u"Cancel"), condition=form.haveInputWidgets, validator=null_validator)
    def handle_cancel_action( self, action, data ):
        """ the cancel action will take us back to the display view"""
        #return handle_edit_action( self, action, data )                    
        url = absoluteURL( self.context, self.request )  + '?portal_status_message=No Changes'
        return self.request.response.redirect( url )
        
                
        
    @form.action(_(u"Save"), condition=form.haveInputWidgets)
    def handle_edit_action( self, action, data ):
        """ Save action will take us: 
        If there were no errors to the display view
        If there were Errors to the edit view
        """
        result = handle_edit_action( self, action, data )                                 
        if self.errors: 
            return result
        else:            
            url = absoluteURL( self.context, self.request )  
            return self.request.response.redirect( url )                    
                      
#################
# return only current member
# Members should not be editable (exchanged) once they were added

sql_edit_members = '''SELECT "users"."titles" || ' ' || "users"."first_name" || ' ' || "users"."middle_name" || ' ' || "users"."last_name" as user_name, 
                      "users"."user_id" 
                       FROM  "public"."users" 
                       WHERE  "users"."user_id" = %(member_id)s                                                                  
                    '''            
membersEditVocab = vocabulary.SQLQuerySource(sql_edit_members, 'user_name', 'user_id', {'member_id':'$member_id'} )      
  
# Parliament
class ParliamentEdit( CustomEditForm ):
    """
    Edit a parliament
    """
    form_fields = form.Fields( IParliament )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget  
    form_fields["election_date"].custom_widget = SelectDateWidget  
    form_fields["description"].custom_widget=widget.RichTextEditor   
    Adapts = IParliament
    CustomValidations = validations.CheckParliamentDatesEdit
   
       

                              

class GovernmentEdit( CustomEditForm ): 
    """
    Edit a government
    """
    form_fields = form.Fields( IGovernment )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget
    form_fields["description"].custom_widget=widget.RichTextEditor      
    Adapts = IGovernment
    CustomValidations = validations.CheckGovernmentsDateInsideParliamentsDatesEdit
    
# Sitting Attendance
             
  

class IGroupSittingAttendanceEdit( interface.Interface ):
    """ """
    member_id = schema.Choice(title=_(u"Member of Parliament"),  
                                source=membersEditVocab, 
                                required=True,
                                )
    attendance_id = schema.Choice( title=_(u"Attendance"),  
                                    source=attendanceVocab, 
                                    required=True,
                                    )  
   
class GroupSittingAttendanceEdit( EditFormViewlet ):
    """
    override the Edit Form for GroupSittingAttendance
    """
    form_fields = form.Fields( IGroupSittingAttendanceEdit )
    template = NamedTemplate('alchemist.subform')   
    def update( self ):
        """
        adapt the custom fields to our object
        """
        self.adapters = { IGroupSittingAttendanceEdit : self.context }        
        super( GroupSittingAttendanceEdit, self).update()
        set_widget_errors(self.widgets, self.errors)

# Sittings                    


class GroupSittingEdit( CustomEditForm ):
    """
    override the Edit Form for GroupSitting
    """
    form_fields = form.Fields( IGroupSitting )
    form_fields["start_date"].custom_widget = SelectDateTimeWidget
    form_fields["end_date"].custom_widget = SelectDateTimeWidget
    Adapts = IGroupSitting
    CustomValidations = validations.CheckSittingDatesInsideParentDatesEdit 

                 

class SessionsEdit ( CustomEditForm ):
    form_fields = form.Fields( IParliamentSession )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget 
    form_fields["notes"].custom_widget=widget.RichTextEditor      
    Adapts = IParliamentSession
    CustomValidations = validations.CheckSessionDatesEdit    

membersEditVocab = vocabulary.SQLQuerySource(sql_edit_members, 'user_name', 'user_id', {'member_id':'$user_id'} )  

sql_editSubstitution = """
                        SELECT "users"."titles" || ' ' || "users"."first_name" || ' ' || "users"."middle_name" || ' ' || "users"."last_name" as user_name,        
                                "users"."user_id" , "users"."last_name"
                        FROM "public"."user_group_memberships", "public"."users" 
                        WHERE ( "user_group_memberships"."user_id" = "users"."user_id" ) 
                            AND ( ( "user_group_memberships"."group_id" = %(group_id)s 
                                AND "user_group_memberships"."user_id" != %(user_id)s 
                                AND "user_group_memberships"."active_p" = True ) ) 
                        UNION
                        SELECT "users"."titles" || ' ' || "users"."first_name" || ' ' || "users"."middle_name" || ' ' || "users"."last_name" as user_name,        
                                "users"."user_id" , "users"."last_name"
                        FROM  "public"."user_group_memberships", "public"."users"
                        WHERE (( "user_group_memberships"."replaced_id" = "users"."user_id" ) 
                            AND "user_group_memberships"."user_id" = %(user_id)s )                             
                        ORDER BY "last_name" ASC
                        """

substitutionsEditVocab = vocabulary.SQLQuerySource(sql_editSubstitution, 'user_name', 'user_id', 
                                                    {'user_id':'$user_id', 'group_id' : '$group_id'} )  
    
class IMemberOfParliamentEdit( IMemberOfParliament ):
    """ Custom schema to override some autogenerated fields"""
    user_id = schema.Choice(title=_(u"Member of Parliament"),  
                                source=membersEditVocab, 
                                required=True,
                                )
    replaced_id = schema.Choice(title=_(u"substituted by"),  
                                source=substitutionsEditVocab, 
                                required=False,
                                )
    
class MemberOfParliamenEdit( CustomEditForm ):     
    Adapts = IMemberOfParliamentEdit          
    form_fields = form.Fields( IMemberOfParliamentEdit ).select(
                    'user_id', 'start_date', 
                    'election_nomination_date', 'elected_nominated',  'constituency_id',
                    'end_date', 'leave_reason',
                    'notes')
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget
    form_fields["election_nomination_date"].custom_widget = SelectDateWidget
    form_fields["notes"].custom_widget=widget.RichTextEditor          
    CustomValidations = validations.CheckMemberDatesEdit         

class CommitteeEdit ( CustomEditForm ):
    Adapts = ICommittee          
    form_fields = form.Fields( ICommittee )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget     
    form_fields["reinstatement_date"].custom_widget = SelectDateWidget  
    form_fields["description"].custom_widget=widget.RichTextEditor            
    CustomValidations = validations.CheckCommitteeDatesEdit 

class ICommitteeMemberEdit( ICommitteeMember ):
    """ Custom schema to override some autogenerated fields"""
    user_id = schema.Choice(title=_(u"Comittee Member"),  
                                source=membersEditVocab, 
                                required=True,
                                )
    replaced_id = schema.Choice(title=_(u"substituted by"),  
                                source=substitutionsEditVocab, 
                                required=False,
                                )
    
        
class CommitteeMemberEdit( CustomEditForm ):
    Adapts = ICommitteeMemberEdit          
    form_fields = form.Fields( ICommitteeMemberEdit ).select(
                    'user_id', 
                    'start_date', 'end_date',
                    'notes')
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget 
    form_fields["notes"].custom_widget=widget.RichTextEditor         
    CustomValidations = validations.CommitteeMemberDatesEdit

class ICommitteeStaffEdit ( ICommitteeStaff ):
    """
    override some fields with custom schema
    """
    user_id = schema.Choice(title=_(u"Staff Member"),  
                                source=membersEditVocab, 
                                required=True,
                                )
    replaced_id = schema.Choice(title=_(u"substituted by"),  
                                source=substitutionsEditVocab, 
                                required=False,
                                )
                                
class CommitteeStaffEdit( CustomEditForm ):
    """
    override the AddForm 
    """
    form_fields = form.Fields( ICommitteeStaffEdit ).select(
                    'user_id', 
                    'start_date', 'end_date',
                    'notes')
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget
    form_fields["notes"].custom_widget=widget.RichTextEditor 
    Adapts = ICommitteeStaffEdit
    CustomValidation =  validations.CommitteeMemberDatesEdit   

   
class MinistryEdit( CustomEditForm ):
    Adapts = IMinistry   
    form_fields = form.Fields( IMinistry )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget 
    form_fields["description"].custom_widget=widget.RichTextEditor         
    CustomValidations = validations.MinistryDatesEdit

class IMinisterEdit( IMinister ):
    """ Custom schema to override some autogenerated fields"""
    user_id = schema.Choice(title=_(u"Minister"),  
                                source=membersEditVocab, 
                                required=True,
                                )
    replaced_id = schema.Choice(title=_(u"substituted by"),  
                                source=substitutionsEditVocab, 
                                required=False,
                                )

class MinisterEdit( CustomEditForm ):
    Adapts = IMinisterEdit   
    form_fields = form.Fields( IMinisterEdit ).select(
                    'user_id', 
                    'start_date', 'end_date',
                    'notes')
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget 
    form_fields["notes"].custom_widget=widget.RichTextEditor         
    CustomValidations = validations.MinisterDatesEdit
    
class ExtensionGroupEdit( CustomEditForm ):
    Adapts = IExtensionGroup   
    form_fields = form.Fields( IExtensionGroup )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget 
    form_fields["description"].custom_widget=widget.RichTextEditor         
    CustomValidations = validations.ExtensionGroupDatesEdit    
        
class IExtensionMemberEdit( IExtensionMember ):
    """ Custom schema to override some autogenerated fields"""
    user_id = schema.Choice(title=_(u"Member"),  
                                source=membersEditVocab, 
                                required=True,
                                )
    replaced_id = schema.Choice(title=_(u"substituted by"),  
                                source=substitutionsEditVocab, 
                                required=False,
                                )
       
class ExtensionMemberEdit( CustomEditForm ):
    Adapts = IExtensionMemberEdit   
    form_fields = form.Fields( IExtensionMemberEdit ).select(
                    'user_id', 
                    'start_date', 'end_date',
                    'notes')
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget         
    form_fields["notes"].custom_widget=widget.RichTextEditor 
    CustomValidations = validations.ExtensionMemberDatesEdit    
 
sql_EditMemberTitle = '''
                        SELECT "user_role_types"."sort_order" || ' - ' || "user_role_types"."user_role_name" AS "ordered_title", 
                        "user_role_types"."user_role_type_id"
                        FROM "public"."user_role_types", "public"."user_group_memberships" 
                        WHERE ( "user_role_types"."user_type" = "user_group_memberships"."membership_type" ) 
                            AND ( ( "user_group_memberships"."membership_id" = %(primary_key)s ) ) 
                        ORDER BY "user_role_types"."sort_order" ASC
                       '''
                                  
titleEditVocab =  vocabulary.SQLQuerySource(sql_EditMemberTitle, 'ordered_title', 'user_role_type_id')
     
class IMemberRoleTitleEdit( IMemberRoleTitle ):
    title_name_id = schema.Choice( title=_(u"Title"),  
                                    source=titleEditVocab, 
                                    required=True,
                                    )  
     
class MemberTitleEdit( CustomEditForm ):
    form_fields = form.Fields( IMemberRoleTitleEdit ).select('title_name_id', 'start_date', 'end_date')
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget
    Adapts = IMemberRoleTitleEdit
    CustomValidations =  validations.CheckMemberTitleDateEdit





sql_select_question_ministry_edit = """
        SELECT "groups"."short_name", "groups"."full_name", "groups"."group_id"
        FROM "public"."ministries" AS "ministries", "public"."groups" AS "groups", "public"."government" AS "government" 
        WHERE "ministries"."ministry_id" = "groups"."group_id" 
            AND "ministries"."government_id" = "government"."government_id" 
            AND "government"."parliament_id" = 9
            AND ( (current_date between "groups"."start_date" and  "groups"."end_date")
                 OR ( ("groups"."start_date" < current_date) AND ("groups"."end_date" IS NULL))
                 )
        ORDER BY short_name
        """
        
qryEditQuestionMinistryVocab = vocabulary.SQLQuerySource(sql_select_question_ministry_edit, 'full_name', 'group_id', 
                                                            {'parliament_id':'$parliament_id',})
        
class IQuestionEdit ( IQuestion ):
    """ Custom schema to override some autogenerated fields"""
    ministry_id = schema.Choice(title=_(u"Ministry"),  
                                source=qryEditQuestionMinistryVocab, 
                                required=False,
                                )        
        
class QuestionEdit( CustomEditForm ):
    """
    Edit a question.
    the workflow transitions are available as actions as well as the 
    default save and cancel buttons
    """
    form_fields = form.Fields( IQuestionEdit ).select('question_type', 'response_type', 'owner_id', 'ministry_id',
                                                    'subject', 'question_text', 
                                                    'clerk_submission_date', 'approval_date',                                                    
                                                    'note', 'receive_notification' )
                    
                                                    
                                                    
    Adapts = IQuestionEdit
    form_fields["note"].custom_widget = widget.OneTimeEditor
    form_fields["question_text"].custom_widget = widget.RichTextEditor 
    form_fields['clerk_submission_date'].for_display = True
    form_fields['approval_date'].for_display = True    
    #form_fields['supplement_parent_id'].custom_widget = widget.SupplementaryQuestionDisplay
#    form_fields['notes_display'].for_display = True  
#    form_fields['notes_display'].custom_widget = widget.HTMLDisplay  
    CustomValidations =  validations.QuestionEdit
    
#    default_actions = form.Actions(
#             form.Action(_(u'Save'), success='handle_edit_action'),
#             form.Action(_(u'Cancel'), success= 'handle_cancel_action'), #, condition='can_delete'),
#             form.Action(_(u'Delete'), success= 'handle_delete_action')
#             )
    
    

    
    def _can_delete(self):
        interaction = zope.security.management.getInteraction()
        return interaction.checkPermission('bungeni.question.delete', self.context)
        
    def _can_edit(self):
        interaction = zope.security.management.getInteraction()
        return interaction.checkPermission('bungeni.question.edit', self.context)    
    
    def _can_view(self):    
        interaction = zope.security.management.getInteraction()
        return interaction.checkPermission('bungeni.question.view', self.context)
    
    def _getDefaultActions(self):
        actions = []
        if self._can_edit():
            action = form.Action(_(u'Save'), success='handle_edit_action')
            action.form = self
            actions.append(action)
        #cancel is allways available... 
        action = form.Action(_(u'Cancel'), success= 'handle_cancel_action')
        action.form = self   
        actions.append(action)

        if self._can_delete():                  
            action = form.Action(_(u'Delete'), success= 'handle_delete_action')
            action.form = self
            actions.append(action)   
        return actions
    
    def handle_delete_action( self, action, data):
        """ 
        delete this object and return to container view
        """
        # we need a check here that the user has the rights to delete
        # the content, otherwise it it should fail!
        if self._can_delete():
            context = removeSecurityProxy(self.context)
            session = Session()
            session.delete(context)
            url = absoluteURL( self.context.__parent__, self.request )  + '?portal_status_message=Object deleted'
            return self.request.response.redirect( url )
        
    def handle_cancel_action( self, action, data ):
        """ the cancel action will take us back to the display view"""
        url = absoluteURL( self.context, self.request )  + '?portal_status_message=No Changes'
        return self.request.response.redirect( url )
            
    def handle_edit_action( self, action, data ):
        """ Save action will take us: 
        If there were no errors to the display view
        If there were Errors to the edit view
        """
        result = handle_edit_action( self, action, data )                                 
        if self.errors: 
            return result
        else:            
            url = absoluteURL( self.context, self.request ) 
            #create a version on every edit ...
            if data.has_key('note'):
                notes = data['note']     
            else:
                notes= ''                
            createVersion(self.context, notes)
            return self.request.response.redirect( url )        
    
    def setupActions( self ):
        self.wf = interfaces.IWorkflowInfo( self.context )
        transitions = self.wf.getManualTransitionIds()
        self.actions = self._getDefaultActions() + bindTransitions( self, transitions, None, interfaces.IWorkflow( self.context ) ) 
       

    def update( self ):
        self.setupActions()  
        super( QuestionEdit, self).update()
        self.setupActions()  # after we transition we have different actions      
        wf_state =interfaces.IWorkflowState( removeSecurityProxy(self.context) ).getState()
        self.wf_status = wf_state            
        

class ResponseEdit ( CustomEditForm ):
    """
    Answer a Question
    UI for ministry to input response
    Display the question when adding the answer.
    """
    form_fields = form.Fields( IResponse ).select('response_text', 'sitting_time') 
    Adapts = IResponse
    form_fields["response_text"].custom_widget=widget.RichTextEditor 
    #form_fields["response_type"].custom_widget=widget.CustomRadioWidget
    CustomValidations =  validations.ResponseEdit
    template = ViewPageTemplateFile('templates/response-edit.pt')        

        
