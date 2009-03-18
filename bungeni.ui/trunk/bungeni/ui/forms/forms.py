# encoding: utf-8

from zope import component
from zope.formlib import form, namedtemplate
from zope import schema, interface
from zope.formlib.namedtemplate import NamedTemplate
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.traversing.browser import absoluteURL 
from zope.security.proxy import removeSecurityProxy
from zope.publisher.browser import BrowserView

import zope.security.management

from ore.alchemist.vocabulary import DatabaseSource
from ore.alchemist import Session
from ore.workflow import interfaces
from ore.yuiwidget import calendar
from ore.alchemist.model import queryModelDescriptor

from alchemist.ui.viewlet import EditFormViewlet
from alchemist.ui.core import null_validator
from alchemist.ui.core import handle_edit_action

from alchemist.catalyst.ui import EditForm

import bungeni.ui.queries.utils as sqlutils 
import bungeni.models.domain as domain

from bungeni.ui.queries import sqlstatements

from bungeni.ui.forms.workflow import bindTransitions
from bungeni.ui.forms.workflow import createVersion

from bungeni.models.interfaces import \
     IGroupSitting, \
     IParliamentSession, \
     IMemberOfParliament, \
     ICommittee, \
     ICommitteeMember, \
     IGovernment, \
     IMinistry, \
     IExtensionGroup, \
     IMinister, \
     IExtensionMember, \
     IParliament, \
     IGroupSittingAttendance, \
     ICommitteeStaff, \
     IMemberRoleTitle, \
     IMemberOfParty, \
     IPoliticalParty, \
     IQuestion, \
     IResponse

from bungeni.core.i18n import _

import bungeni.core.globalsettings as prefs
from bungeni.models.interfaces import IFileAttachments 
from bungeni.ui.widgets import  SelectDateTimeWidget, SelectDateWidget
from bungeni.ui import widgets

from bungeni.ui.forms.common import AddForm
BungeniAddForm = AddForm

import validations

FormTemplate = namedtemplate.NamedTemplateImplementation(
    ViewPageTemplateFile('templates/form.pt')
    )

###################### Specialized Add Forms per content Type ################################   

    


# party membership

# ministries
                                      
#ministers
               
# CommitteeMemberAdd
                      
# committee staff
                                         
# Members of Parliament
   

# Sessions

    
class SessionAdd( BungeniAddForm ):
    """
    override the AddForm for GroupSittingAttendance
    """
    form_fields = form.Fields( IParliamentSession )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget 
    Adapts = IParliamentSession
    CustomValidation =  validations.CheckSessionDatesInsideParentDatesAdd    
                      
 

# Sittings



class GroupSittingAdd( BungeniAddForm ):
    """
    override the AddForm for GroupSittingAttendance
    """
    form_fields = form.Fields( IGroupSitting )
    form_fields["start_date"].custom_widget = SelectDateTimeWidget
    form_fields["end_date"].custom_widget = SelectDateTimeWidget
    Adapts = IGroupSitting
    CustomValidation =  validations.CheckSittingDatesInsideParentDatesAdd 
                      
        
     


membersAddVocab = sqlutils.SQLQuerySource(sqlstatements.sql_add_members, 'user_name', 'user_id')      
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



class GroupSittingAttendanceAdd( BungeniAddForm ):
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


                                  
titleAddVocab =  sqlutils.SQLQuerySource(sqlstatements.sql_addMemberTitle, 'ordered_title', 'user_role_type_id')

# Titles / Roles

     
class IMemberRoleTitleAdd( IMemberRoleTitle ):
    title_name_id = schema.Choice( title=_(u"Title"),  
                                    source=titleAddVocab, 
                                    required=True,
                                    )  
     
class MemberTitleAdd( BungeniAddForm ):
    form_fields = form.Fields( IMemberRoleTitleAdd ).select('title_name_id', 'start_date', 'end_date')
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget
    Adapts = IMemberRoleTitleAdd
    CustomValidation =  validations.CheckMemberTitleDateAdd 



##############
#Generic Custom Edit form   


def hasDeletePermission(context):
    """Generic check if the user has rights to delete the object 
    The permission must follow the convention: bungeni.classname.Delete
    where classname is the lowercase of the name of the python class
    """
    
    interaction = zope.security.management.getInteraction()
    class_name = context.__class__.__name__ 
    permission_name = 'bungeni.' + class_name.lower() +'.Delete'
    return interaction.checkPermission(permission_name, context)



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
    
    def _can_edit(self):
        """
        check for edit permissions
        """
        #TODO
        return True
    
    
    def _can_delete( self ):
        return hasDeletePermission(self.context)

    def _can_attach( self ):
        #result = form.haveInputWidgets( self, action)
        result =  IFileAttachments.providedBy( self.context )    
        return result      
    
    def _getDefaultActions(self):
        actions = []
        if self._can_edit():
            action = form.Action(_(u'Save'), success='handle_edit_action')
            action.form = self
            actions.append(action)
        if self._can_attach():
            action = form.Action(_(u'Attach a file'), success='handle_save_attach')
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
     

    def setupActions( self ):
        self.actions = self._getDefaultActions()    
          
          
    def update( self ):
        """
        adapt the custom fields to our object
        """
        self.setupActions()  
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
        
    
    #form.action(_(u"delete"), condition=can_delete, validator=null_validator)
    def handle_delete_action( self, action, data):    
        """
        deletes the current content and takes you to the listing
        """        
        if self.can_delete(action):
            context = removeSecurityProxy(self.context)
            session = Session()
            session.delete(context)
            url = absoluteURL( self.context.__parent__, self.request )  + '?portal_status_message=Object deleted'
            return self.request.response.redirect( url )
    
    #form.action(_(u"Cancel"), condition=form.haveInputWidgets, validator=null_validator)
    def handle_cancel_action( self, action, data ):
        """ the cancel action will take us back to the display view"""
        #return handle_edit_action( self, action, data )                    
        url = absoluteURL( self.context, self.request )  + '?portal_status_message=No Changes'
        return self.request.response.redirect( url )
        
                
        
    #form.action(_(u"Save"), condition=form.haveInputWidgets)
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

    #form.action(_(u"Save and attach files"), condition=can_attach )
    def handle_save_attach( self, action, data ):        
        result = handle_edit_action( self, action, data )                                 
        if self.errors: 
            return result
        else:            
            url = absoluteURL( self.context, self.request )   + '/files'
            return self.request.response.redirect( url  )    
                        
                      

  


    
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
    form_fields["notes"].custom_widget=widgets.RichTextEditor      
    Adapts = IParliamentSession
    CustomValidations = validations.CheckSessionDatesEdit    


    
class ResponseEdit ( CustomEditForm ):
    """ Answer a Question
    UI for ministry to input response
    Display the question when adding the answer.
    """
    form_fields = form.Fields( IResponse ).select('response_text', 'sitting_time') 
    Adapts = IResponse
    form_fields["response_text"].custom_widget=widgets.RichTextEditor 
    #form_fields["response_type"].custom_widget=widgets.CustomRadioWidget
    CustomValidations =  validations.ResponseEdit
    
class ResponseAdd( BungeniAddForm ):
    """
    Answer a Question
    UI for ministry to input response
    Display the question when adding the answer.
    """
    form_fields = form.Fields( IResponse ).select('response_text', 'sitting_time') 
    Adapts = IResponse
    form_fields["response_text"].custom_widget=widgets.RichTextEditor 
    #form_fields["response_type"].custom_widget=widget.CustomRadioWidget
    CustomValidation =  validations.ResponseAdd
    

   
    
 
################################################## NEW #######################################################

########## Groups ########################
       
class GroupEditForm (EditForm):
    """ generic form for all groups """

class ExtensionGroupEditForm( GroupEditForm ):
     
    CustomValidations = validations.ExtensionGroupDatesEdit    

class MinistryEditForm( GroupEditForm ):
        
    CustomValidations = validations.MinistryDatesEdit     

class CommitteeEditForm ( GroupEditForm ):
          
    CustomValidations = validations.CheckCommitteeDatesEdit   


class ParliamentEditForm( GroupEditForm ):

    CustomValidations = validations.CheckParliamentDatesEdit

class GovernmentEdit( GroupEditForm ): 

    CustomValidations = validations.CheckGovernmentsDateInsideParliamentsDatesEdit


class GroupAddForm(AddForm):

    def get_form_fields(self):
        form_fields = super(
            GroupAddForm, self).get_form_fields().omit("end_date")
        return form_fields

class ParliamentAddForm( GroupAddForm ):

    CustomValidation = validations.CheckParliamentDatesAdd  


class GovernmentAdd ( BungeniAddForm ):

    CustomValidation =  validations.CheckGovernmentsDateInsideParliamentsDatesAdd    

                      
class MinistryAdd( GroupAddForm ):

    CustomValidation =  validations.CheckMinistryDatesInsideGovernmentDatesAdd     


class CommitteeAdd( GroupAddForm ):

    CustomValidation = validations.CheckCommitteesDatesInsideParentDatesAdd     

class ExtensionGroupAdd( GroupAddForm ):

    CustomValidation =   validations.CheckExtensionGroupDatesInsideParentDatesAdd   


class PoliticalPartyAdd( BungeniAddForm ):

    CustomValidation = validations.checkPartyDates

############# User Group Memberships ########################

class GroupMemberEditForm ( EditForm ):
    """ generic form for all groupmemberships"""
    
    _membersEditVocab = sqlutils.SQLQuerySource(
        sqlstatements.sql_edit_members, 'user_name', 'user_id', 
            {'member_id':'$user_id'} )  

    _substitutionsEditVocab = sqlutils.SQLQuerySource(
        sqlstatements.sql_editSubstitution, 
        'user_name', 'user_id',                                                     
        {'user_id':'$user_id', 'group_id' : '$group_id'} )  
    
     def get_form_fields(self):
        base_fields = super(MemberTitleEditForm, self).get_form_fields()
            
        return base_fields.omit("user_id", "replaced_id") + form.Fields(
            schema.Choice(
                __name__="user_id",
                title=_(u"Name"),  
                source=self._membersEditVocab, 
                required=True,
                ),                
            schema.Choice(
                __name__="replaced_id",
                title=_(u"Substituted by"),  
                source=self._substitutionsEditVocab, 
                required=False,
                )                                
            )


class MinisterEditForm( GroupMemberEditForm ):

    CustomValidations = validations.MinisterDatesEdit

class ExtensionMemberEditForm( CustomEditForm ):

    CustomValidations = validations.ExtensionMemberDatesEdit  


class CommitteeStaffEditForm( GroupMemberEditForm ):

    CustomValidation =  validations.CommitteeMemberDatesEdit   

class CommitteeMemberEditForm( GroupMemberEditForm ):
        
    CustomValidations = validations.CommitteeMemberDatesEdit

class MemberOfParliamenEditForm( GroupMemberEditForm ):     
         
    CustomValidations = validations.CheckMemberDatesEdit         

class GroupMemberAddForm ( AddForm ):
    """ Generic Add Form for all user group memberships
    """
    def get_form_fields(self):
        base_fields = super(GroupMemberAddForm, self).get_form_fields()
            
        return base_fields.omit("user_id", 
                                "replaced_id", 
                                "substitution_type", 
                                "end_date" )
            
    @property
    def defaults(self):
        defaults = {}        
        sdate = getattr(self.context.__parent__, 'start_date', None)
        if sdate:
            defaults['start_date'] = sdate
        return defaults    
    

class MemberOfParliamentAddForm( GroupMemberAddForm ):
    _qryAddMemberOfParliamentVocab = sqlutils.SQLQuerySource(
        sqlstatements.sql_AddMemberOfParliament, 
        'fullname', 
        'user_id')  
    CustomValidation = validations.CheckMPsDatesInsideParentDatesAdd  

    @property
    def defaults(self):
        defaults = super(MemberOfParliamentAddForm, self).defaults()        
        edate = getattr(self.context.__parent__, 'election_date', None)       
        if edate:
            defaults['election_nomination_date'] = edate
        return defaults
        

    def get_form_fields(self):
        base_fields = super(QuestionEditForm, self).get_form_fields()
            
        return base_fields + form.Fields(
            schema.Choice(
                __name__="user_id",
                title=_(u"Member of Parliament"),  
                source=self._qryAddMemberOfParliamentVocab, 
                required=True,
                )
            )

    
class MinistersAddForm( GroupMemberAddForm ):
    _qryAddMinisterVocab = sqlutils.SQLQuerySource(
        sqlstatements.sql_addMinister, 'fullname', 'user_id')
    CustomValidation =   validations.CheckMinisterDatesInsideMinistryDatesAdd    

   def get_form_fields(self):
        base_fields = super(MinistersAddForm, self).get_form_fields()
            
        return base_fields + form.Fields(
            schema.Choice(
                __name__="user_id",
                title=_(u"Minister"),  
                source=self._qryAddMinisterVocab, 
                required=True,
                ))

                                
                                
class ExtensionMemberAddForm( GroupMemberAddForm ):
    _qryAddExtensionMemberVocab = sqlutils.SQLQuerySource(
        sqlstatements. sql_addExtensionMember, 'fullname', 'user_id')
    CustomValidation =  validations.CheckExtensionMemberDatesInsideParentDatesAdd       
    
    def get_form_fields(self):
        base_fields = super(ExtensionMemberAddForm, self).get_form_fields()            
        return base_fields + form.Fields(
            schema.Choice(
                __name__="user_id",
                title=_(u"Person"),  
                source=qryAddExtensionMemberVocab, 
                required=True,
                ))    
    

class CommitteeMemberAddForm( GroupMemberAddForm ):
    _qryAddCommitteeMemberVocab = sqlutils.SQLQuerySource(
        sqlstatements. sql_AddCommitteeMember, 'fullname', 'user_id')
    CustomValidation =  validations.CheckCommitteeMembersDatesInsideParentDatesAdd   

    def get_form_fields(self):
        base_fields = super(CommitteeMemberAddForm, self).get_form_fields()            
        return base_fields + form.Fields(
            schema.Choice(
                __name__="user_id",
                title=_(u"Committee member"),  
                source=self._qryAddCommitteeMemberVocab, 
                required=True,
                ))  



class ICommitteeStaffAdd ( ICommitteeStaff ):
    """
    override some fields with custom schema
    """
    user_id = schema.Choice(
                                )
                                
class CommitteeStaffAddForm( GroupMemberAddForm ):
    _qryAddCommitteeStaffVocab = sqlutils.SQLQuerySource(
        sqlstatements.sql_AddCommitteeStaff, 'fullname', 'user_id')
    CustomValidation =  validations.CheckCommitteeMembersDatesInsideParentDatesAdd  
    
    def get_form_fields(self):
        base_fields = super(CommitteeStaffAddForm, self).get_form_fields()            
        return base_fields + form.Fields(
            schema.Choice(
                __name__="user_id",
                title=_(u"Staff Member"),  
                source=self._qryAddCommitteeStaffVocab, 
                required=True,
                ))  

class PartyMemberAdd( GroupMemberAddForm ):
    """add a person to a party"""
    #XXX
    pass

class MemberOfPartyAdd( GroupMemberAddForm ):
    """ add a partymembership to a person """
    #XXX
    #Adapts = IMemberOfParty    
    CustomValidation = validations.checkPartyMembershipDates






############ Titles for Users and Group members ############


class MemberTitleEditForm( EditForm ):
    _titleEditVocab =  sqlutils.SQLQuerySource(
        sqlstatements.sql_EditMemberTitle, 'ordered_title', 'user_role_type_id')
    
     def get_form_fields(self):
        base_fields = super(MemberTitleEditForm, self).get_form_fields()
            
        return base_fields.omit("title_name_id") + form.Fields(
            schema.Choice(
                __name__="title_name_id",
                title=_(u"Title"),  
                source=self._titleEditVocab, 
                required=True,
                ))
    
    CustomValidations =  validations.CheckMemberTitleDateEdit

################# Paliamentary Items ########################

class QuestionAdd(AddForm):
    _qryAddQuestionMinistryVocab = sqlutils.SQLQuerySource(
        sqlstatements.sql_select_question_ministry_add, 'full_name', 'group_id')

    def get_form_fields(self):
        form_fields = super(
            QuestionAdd, self).get_form_fields().omit("ministry_id")

        if self.context.__parent__.__class__ != domain.Question:
            form_fields += form.Fields(
                schema.Choice(
                    __name__="ministry_id",
                    title=_(u"Ministry"),  
                    source=self._qryAddQuestionMinistryVocab, 
                    required=False,
                    ))
            
        return form_fields
    
    def _can_submit( self, action):
        result = form.haveInputWidgets( self, action)
        result = result and prefs.getQuestionSubmissionAllowed()
        return result

    @form.action(_(u"Save and submit to clerk"),
                 condition=_can_submit, validator='validateAdd')
    def handle_add_submit(self, action, data):
        ob = self.createAndAdd(data)
        info = component.getAdapter(ob,  interfaces.IWorkflowInfo)
        
        if data.has_key('note'):
            notes = data['note']
        else:
            notes = ""
            
        createVersion(ob, notes)                                                                    
        info.fireTransition('submit-to-clerk', notes)

        # set status message and next URL
        name = self.context.domain_model.__name__
        self._next_url = absoluteURL(ob, self.request) + \
                         "/?portal_status_message=%s Added" % name
                         

class QuestionEditForm(EditForm):
    """Edit a question.
    
    Todo: The workflow transitions are available as actions as well as
    the default save and cancel buttons
    """

    _qryEditQuestionMinistryVocab = sqlutils.SQLQuerySource(
        sqlstatements.sql_select_question_ministry_edit, 'full_name', 'group_id', 
        {'parliament_id':'$parliament_id',})
    CustomValidations = validations.QuestionEdit
    
    def get_form_fields(self):
        base_fields = super(QuestionEditForm, self).get_form_fields()
            
        return base_fields.omit("ministry_id") + form.Fields(
            schema.Choice(
                __name__="ministry_id",
                title=_(u"Ministry"),  
                source=self._qryEditQuestionMinistryVocab, 
                required=False,
                ))
                                                    



        



        
