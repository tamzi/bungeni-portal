# encoding: utf-8

import zope.security.management

from zope import component
from zope.formlib import form, namedtemplate
from zope import schema, interface
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.traversing.browser import absoluteURL 

from ore.workflow import interfaces

from bungeni.models import domain
from bungeni.core import globalsettings as prefs
from bungeni.core.i18n import _
from bungeni.ui.queries import statements as sqlstatements
from bungeni.ui.queries import utils as sqlutils
from bungeni.ui.forms.workflow import createVersion
from bungeni.ui.forms import validations
from bungeni.ui.forms.common import ReorderForm
from bungeni.ui.forms.common import AddForm
from bungeni.ui.forms.common import EditForm

FormTemplate = namedtemplate.NamedTemplateImplementation(
    ViewPageTemplateFile('templates/form.pt')
    )

def hasDeletePermission(context):
    """Generic check if the user has rights to delete the object. The
    permission must follow the convention:
    ``bungeni.<classname>.Delete`` where 'classname' is the lowercase
    of the name of the python class.
    """
    
    interaction = zope.security.management.getInteraction()
    class_name = context.__class__.__name__ 
    permission_name = 'bungeni.' + class_name.lower() +'.Delete'
    return interaction.checkPermission(permission_name, context)

def set_widget_errors(widgets, errors):
    """Display invariant errors / custom validation errors in the
    context of the field."""

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

membersEditVocab = sqlutils.SQLQuerySource(
        sqlstatements.sql_edit_members, 
        'user_name', 'user_id', 
        {'member_id':'$user_id'} )


########## Groups ########################
       
class GroupEditForm (EditForm):
    """ generic form for all groups """


class ExtensionGroupEditForm( GroupEditForm ):
     
    CustomValidations = validations.validate_date_range_within_parent    

class MinistryEditForm( GroupEditForm ):
        
    CustomValidations = validations.validate_date_range_within_parent     

class CommitteeEditForm ( GroupEditForm ):
          
    CustomValidations = validations.validate_date_range_within_parent   


class ParliamentEditForm( GroupEditForm ):

    CustomValidations = validations.CheckParliamentDatesEdit


class GovernmentEditForm( GroupEditForm ): 

    CustomValidations = validations.CheckGovernmentsDateInsideParliamentsDatesEdit


class GroupAddForm(AddForm):

    def get_form_fields(self):
        form_fields = super(
            GroupAddForm, self).get_form_fields().omit("end_date")
        return form_fields

class GovernmentAddForm ( AddForm ):

    CustomValidation =  validations.CheckGovernmentsDateInsideParliamentsDatesAdd    



class CommitteeAddForm( GroupAddForm ):

    CustomValidation = validations.validate_date_range_within_parent     

class ExtensionGroupAddForm( GroupAddForm ):

    CustomValidation =   validations.validate_date_range_within_parent   


class PoliticalPartyAddForm( AddForm ):

    CustomValidation = validations.validate_date_range_within_parent

############# User Group Memberships ########################

class GroupMemberEditForm ( EditForm ):
    """ generic form for all groupmemberships"""
    
    _membersEditVocab = membersEditVocab

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

    CustomValidations = validations.validate_date_range_within_parent
    
class ExtensionMemberEditForm( EditForm ):

    CustomValidations = validations.validate_date_range_within_parent  


class CommitteeStaffEditForm( GroupMemberEditForm ):

    CustomValidation =  validations.validate_date_range_within_parent   

class CommitteeMemberEditForm( GroupMemberEditForm ):
        
    CustomValidations = validations.validate_date_range_within_parent

class MemberOfParliamenEditForm( GroupMemberEditForm ):     
         
    CustomValidations = validations.validate_date_range_within_parent         

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
    CustomValidation = validations.validate_date_range_within_parent  

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
    CustomValidation =   validations.validate_date_range_within_parent    

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
    CustomValidation =  validations.validate_date_range_within_parent       
    
    def get_form_fields(self):
        base_fields = super(ExtensionMemberAddForm, self).get_form_fields()            
        return base_fields + form.Fields(
            schema.Choice(
                __name__="user_id",
                title=_(u"Person"),  
                source=self._qryAddExtensionMemberVocab, 
                required=True,
                ))    
    

class CommitteeMemberAddForm( GroupMemberAddForm ):
    _qryAddCommitteeMemberVocab = sqlutils.SQLQuerySource(
        sqlstatements. sql_AddCommitteeMember, 'fullname', 'user_id')
    CustomValidation =  validations.validate_date_range_within_parent   

    def get_form_fields(self):
        base_fields = super(CommitteeMemberAddForm, self).get_form_fields()            
        return base_fields + form.Fields(
            schema.Choice(
                __name__="user_id",
                title=_(u"Committee member"),  
                source=self._qryAddCommitteeMemberVocab, 
                required=True,
                ))  


                                
class CommitteeStaffAddForm( GroupMemberAddForm ):
    _qryAddCommitteeStaffVocab = sqlutils.SQLQuerySource(
        sqlstatements.sql_AddCommitteeStaff, 'fullname', 'user_id')
    CustomValidation =  validations.validate_date_range_within_parent  
    
    def get_form_fields(self):
        base_fields = super(CommitteeStaffAddForm, self).get_form_fields()            
        return base_fields + form.Fields(
            schema.Choice(
                __name__="user_id",
                title=_(u"Staff Member"),  
                source=self._qryAddCommitteeStaffVocab, 
                required=True,
                ))  

class PartyMemberAddForm( GroupMemberAddForm ):
    """add a person to a party
    used in the political party container
    """
    #XXX
    

class MemberOfPartyAddForm( GroupMemberAddForm ):
    """ add a partymembership to a person 
    used in the parliament members container
    """
    #XXX
    #Adapts = IMemberOfParty    
    #CustomValidation = validations.checkPartyMembershipDates




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
    

class MemberTitleAddForm( AddForm ):
    _titleAddVocab =  sqlutils.SQLQuerySource(
        sqlstatements.sql_addMemberTitle, 
        'ordered_title', 
        'user_role_type_id')
    CustomValidation =  validations.CheckMemberTitleDateAdd 
    
    def get_form_fields(self):
        base_fields = super(MemberTitleEditForm, self).get_form_fields()
            
        return base_fields.omit("title_name_id") + form.Fields(
            schema.Choice(
                __name__="title_name_id",
                title=_(u"Title"),  
                source=self._titleAddVocab, 
                required=True,
                ))
    

################# Sessions and sittings #####################

class SessionAddForm( AddForm ):

    CustomValidation =  validations.CheckSessionDatesInsideParentDatesAdd    

class SessionsEditForm ( EditForm ):

    CustomValidations = validations.CheckSessionDatesEdit    

class GroupSittingAddForm( AddForm ):
    CustomValidation =  validations.CheckSittingDatesInsideParentDatesAdd 

class GroupSittingEditForm( EditForm ):

    CustomValidations = validations.CheckSittingDatesInsideParentDatesEdit 
      

class GroupSittingAttendanceAddForm( AddForm ):
    _qryMembersAddVocab = sqlutils.SQLQuerySource(sqlstatements.sql_add_members, 'user_name', 'user_id')      
    
    def get_form_fields(self):
        base_fields = super(GroupSittingAttendanceAddForm, self).get_form_fields()
            
        return base_fields.omit("member_id", "" ) + form.Fields(
            schema.Choice(
                __name__="member_id",
                title=_(u"Member of Parliament"),  
                source=self._qryMembersAddVocab, 
                required=True,                                
                ))    

    
class GroupSittingAttendanceEditForm( EditForm ):

    _membersEditVocab = membersEditVocab
    
    def get_form_fields(self):
        base_fields = super(GroupSittingAttendanceAddForm, self).get_form_fields()
            
        return base_fields.omit("member_id", "" ) + form.Fields(
            schema.Choice(
                __name__="member_id",
                title=_(u"Member"),  
                source=self._membersEditVocab, 
                required=True,                          
                ))    


    
                
################# Paliamentary Items ########################

class QuestionAddForm(AddForm):
    _qryAddQuestionMinistryVocab = sqlutils.SQLQuerySource(
        sqlstatements.sql_select_question_ministry_add, 'full_name', 'group_id')
    CustomValidations = validations.null_validator
    actions = AddForm.actions.copy()

    def get_form_fields(self):
        form_fields = super(
            QuestionAddForm, self).get_form_fields().omit("ministry_id")

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
    The workflow transitions are available as actions as well as
    the default save and cancel buttons
    """

    _qryEditQuestionMinistryVocab = sqlutils.SQLQuerySource(
        sqlstatements.sql_select_question_ministry_edit, 'full_name', 'group_id', 
        {'parliament_id':'$parliament_id',})
    CustomValidations = validations.null_validator

    
    def get_form_fields(self):
        base_fields = super(QuestionEditForm, self).get_form_fields()
            
        return base_fields.omit("ministry_id") + form.Fields(
            schema.Choice(
                __name__="ministry_id",
                title=_(u"Ministry"),  
                source=self._qryEditQuestionMinistryVocab, 
                required=False,
                ))
                                                    
class ResponseEditForm( EditForm ):
    """ Answer a Question
    UI for ministry to input response
    Display the question when adding the answer.
    """
    CustomValidations =  validations.null_validator

    
class ResponseAddForm( AddForm ):
    """
    Answer a Question
    UI for ministry to input response
    Display the question when adding the answer.
    """
    CustomValidation =  validations.null_validator

    
class ItemScheduleContainerReorderForm(ReorderForm):
    def save_ordering(self, ordering):
        for name, scheduling in self.context.items():
            scheduling.planned_order = ordering.index(name)
    
