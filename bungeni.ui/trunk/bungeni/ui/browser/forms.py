
# encoding: utf-8

from ore.alchemist.vocabulary import DatabaseSource

from alchemist.ui.content import ContentAddForm
from alchemist.ui.viewlet import EditFormViewlet

from zope.formlib import form
from zope import schema, interface
from zope.formlib.namedtemplate import NamedTemplate

import bungeni.core.vocabulary as vocabulary
import bungeni.core.domain as domain
from bungeni.core.i18n import _
from bungeni.core.interfaces import IGroupSitting, IParliamentSession, IMemberOfParliament, \
    ICommittee, ICommitteeMember, IGovernment, IMinistry, IExtensionGroup, IMinister, \
    IExtensionMember, IParliament


from bungeni.ui.datetimewidget import  SelectDateTimeWidget, SelectDateWidget

import validations



###########
# Add forms


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


#parliaments




class ParliamentAdd( ContentAddForm ):
    """
    custom Add form for ministries
    """
    form_fields = form.Fields( IParliament )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget  
    form_fields["election_date"].custom_widget = SelectDateWidget    
                      
    def update(self):
        """
        Called by formlib after __init__ for every page update. This is
        the method you can use to update form fields from your class
        """        
        self.status = self.request.get('portal_status_message','')        
        # to display errors from invariants, pass the field names when raising Invalid
        #super(ParliamentAdd, self).update()
        form.AddForm.update( self )
        set_widget_errors(self.widgets, self.errors) 
 
    def finishConstruction( self, ob ):
        """
        adapt the custom fields to the object
        """
        self.adapters = { IParliament : ob }
        
    def validate(self, action, data):    
        """
        validation that require context must be called here,
        invariants may be defined in the descriptor
        """                                       
        return (form.getWidgetsData(self.widgets, self.prefix, data) +
                 form.checkInvariants(self.form_fields, data) +
                 validations.CheckParliamentDatesAdd( self.context, data))  

    def invariantErrors( self ):        
        errors = []       
        return errors
                         




# ministries
class MinistryAdd( ContentAddForm ):
    """
    custom Add form for ministries
    """
    form_fields = form.Fields( IMinistry )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget    
                      
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
        self.adapters = { IMinistry : ob }
        
    def validate(self, action, data):    
        """
        validation that require context must be called here,
        invariants may be defined in the descriptor
        """                                       
        return (form.getWidgetsData(self.widgets, self.prefix, data) +
                 form.checkInvariants(self.form_fields, data) +
                 validations.CheckMinistryDatesInsideGovernmentDatesAdd( self.context, data))  
                 
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
    
    
class MinistersAdd( ContentAddForm ):
    """
    custom Add form for ministries
    """
    form_fields = form.Fields( IMinisterAdd ).omit( "replaced_id", "substitution_type" )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget    
                      
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
        self.adapters = { IMinisterAdd : ob }
        
    def validate(self, action, data):    
        """
        validation that require context must be called here,
        invariants may be defined in the descriptor
        """                                       
        return (form.getWidgetsData(self.widgets, self.prefix, data) +
                 form.checkInvariants(self.form_fields, data) +
                 validations.CheckMinisterDatesInsideMinistryDatesAdd( self.context, data))  
    
# government

class GovernmentAdd ( ContentAddForm ):
    """
    custom Add form for government
    """
    form_fields = form.Fields( IGovernment )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget    
                      
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
        self.adapters = { IGovernment : ob }
        
    def validate(self, action, data):    
        """
        validation that require context must be called here,
        invariants may be defined in the descriptor
        """                                       
        return (form.getWidgetsData(self.widgets, self.prefix, data) +
                 form.checkInvariants(self.form_fields, data) +
                 validations.CheckGovernmentsDateInsideParliamentsDatesAdd( self.context, data))  




# Extension groups

class ExtensionGroupAdd( ContentAddForm ):
    """
    override the AddForm for GroupSittingAttendance
    """
    form_fields = form.Fields( IExtensionGroup )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget    
                      
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
        self.adapters = { IExtensionGroup : ob }
        
    def validate(self, action, data):    
        """
        validation that require context must be called here,
        invariants may be defined in the descriptor
        """                                       
        return (form.getWidgetsData(self.widgets, self.prefix, data) +
                 form.checkInvariants(self.form_fields, data) +
                 validations.CheckExtensionGroupDatesInsideParentDatesAdd( self.context, data))



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
class ExtensionMemberAdd( ContentAddForm ):
    """
    override the AddForm for GroupSittingAttendance
    """
    form_fields = form.Fields( IExtensionMemberAdd ).omit( "replaced_id", "substitution_type" )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget    
                      
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
        self.adapters = { IExtensionMemberAdd : ob }
        
    def validate(self, action, data):    
        """
        validation that require context must be called here,
        invariants may be defined in the descriptor
        """                                       
        return (form.getWidgetsData(self.widgets, self.prefix, data) +
                 form.checkInvariants(self.form_fields, data) +
                 validations.CheckExtensionMemberDatesInsideParentDatesAdd( self.context, data))


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
class CommitteeMemberAdd( ContentAddForm ):
    """
    override the AddForm for GroupSittingAttendance
    """
    form_fields = form.Fields( ICommitteeMemberAdd ).omit( "replaced_id", "substitution_type" )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget    
                      
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
        self.adapters = { ICommitteeMember : ob }
        
    def validate(self, action, data):    
        """
        validation that require context must be called here,
        invariants may be defined in the descriptor
        """                                       
        return (form.getWidgetsData(self.widgets, self.prefix, data) +
                 form.checkInvariants(self.form_fields, data) +
                 validations.CheckCommitteeMembersDatesInsideParentDatesAdd( self.context, data))  

# Committees


class CommitteeAdd( ContentAddForm ):
    """
    override the AddForm for GroupSittingAttendance
    """
    form_fields = form.Fields( ICommittee )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget    
    form_fields["dissolution_date"].custom_widget = SelectDateWidget
    form_fields["reinstatement_date"].custom_widget = SelectDateWidget    
                      
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
        self.adapters = { ICommittee : ob }
        
    def validate(self, action, data):    
        """
        validation that require context must be called here,
        invariants may be defined in the descriptor
        """                                       
        return (form.getWidgetsData(self.widgets, self.prefix, data) +
                 form.checkInvariants(self.form_fields, data) +
                 validations.CheckCommitteesDatesInsideParentDatesAdd( self.context, data))    

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


class MemberOfParliamentAdd( ContentAddForm ):
    """
    override the AddForm for GroupSittingAttendance
    """
    form_fields = form.Fields( IMemberOfParliamentAdd ).omit( "replaced_id", "substitution_type" )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget 
    
    
    #pdb.set_trace()
                      
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
        self.adapters = { IMemberOfParliamentAdd : ob }
        
    def validate(self, action, data):    
        """
        validation that require context must be called here,
        invariants may be defined in the descriptor
        """                                       
        return (form.getWidgetsData(self.widgets, self.prefix, data) +
                 form.checkInvariants(self.form_fields, data) +
                 validations.CheckMPsDatesInsideParentDatesAdd( self.context, data))


# Sessions

    
class SessionAdd( ContentAddForm ):
    """
    override the AddForm for GroupSittingAttendance
    """
    form_fields = form.Fields( IParliamentSession )
    form_fields["start_date"].custom_widget = SelectDateWidget
    form_fields["end_date"].custom_widget = SelectDateWidget    
                      
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
        self.adapters = { IParliamentSession : ob }
        
    def validate(self, action, data):    
        """
        validation that require context must be called here,
        invariants may be defined in the descriptor
        """                                       
        return (form.getWidgetsData(self.widgets, self.prefix, data) +
                 form.checkInvariants(self.form_fields, data) +
                 validations.CheckSessionDatesInsideParentDatesAdd( self.context, data))   
                 

# Sittings



class GroupSittingAdd( ContentAddForm ):
    """
    override the AddForm for GroupSittingAttendance
    """
    form_fields = form.Fields( IGroupSitting )
    form_fields["start_date"].custom_widget = SelectDateTimeWidget
    form_fields["end_date"].custom_widget = SelectDateTimeWidget
                      
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
        self.adapters = { IGroupSitting : ob }
        
    def validate(self, action, data):    
        """
        validation that require context must be called here,
        invariants may be defined in the descriptor
        """                                       
        return (form.getWidgetsData(self.widgets, self.prefix, data) +
                 form.checkInvariants(self.form_fields, data) +
                 validations.CheckSittingDatesInsideParentDatesAdd( self.context, data))         
     

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
        
        
##############
# Edit forms      
             

# Sitting Attendance
             
sql_edit_members = '''SELECT "users"."titles" || ' ' || "users"."first_name" || ' ' || "users"."middle_name" || ' ' || "users"."last_name" as user_name, 
                      "users"."user_id" 
                       FROM  "public"."users" 
                       WHERE  "users"."user_id" = %(member_id)s                                                                  
                    '''            
membersEditVocab = vocabulary.SQLQuerySource(sql_edit_members, 'user_name', 'user_id', {'member_id':'$member_id'} )      

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


class GroupSittingEdit( EditFormViewlet ):
    """
    override the Edit Form for GroupSitting
    """
    form_fields = form.Fields( IGroupSitting )
    form_fields["start_date"].custom_widget = SelectDateTimeWidget
    form_fields["end_date"].custom_widget = SelectDateTimeWidget
    template = NamedTemplate('alchemist.subform')   

    def update( self ):
        """
        adapt the custom fields to our object
        """
        self.adapters = { IGroupSitting : self.context }        
        super( GroupSittingEdit, self).update()
        set_widget_errors(self.widgets, self.errors)
        
        
    def validate(self, action, data):    
        """
        validation that require context must be called here,
        invariants may be defined in the descriptor
        """                                       
        return (form.getWidgetsData(self.widgets, self.prefix, data) +
                 form.checkInvariants(self.form_fields, data) +
                 validations.CheckSittingDatesInsideParentDatesEdit( self.context, data))  
                 
        
        

    
