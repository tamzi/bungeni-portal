
from ore.alchemist import Session
from ore.alchemist.model import ModelDescriptor
from ore.alchemist.vocabulary import DatabaseSource
from copy import deepcopy
from zope import schema, interface
from zope.schema.vocabulary import SimpleVocabulary

from zc.table import column
import zope.app.form.browser
#from z3c.form.browser import image

from bungeni.ui.widgets import SelectDateWidget, SelectDateTimeWidget
from bungeni.ui.widgets import CustomRadioWidget
from bungeni.ui.widgets import HTMLDisplay
from bungeni.ui.widgets import RichTextEditor
from bungeni.ui.widgets import ImageDisplayWidget
from bungeni.ui.widgets import ImageInputWidget
from bungeni.ui.widgets import SupplementaryQuestionDisplay

from ore.yuiwidget import calendar


from alchemist.ui import widgets
from bungeni.ui.constraints import check_email

from bungeni.models import domain
from bungeni.models import vocabulary
from bungeni.ui.forms import validations
from bungeni.core.translation import get_default_language
from bungeni.core.translation import available_languages
from bungeni.ui.i18n import _


###
# Listing Columns 
# 
def _column( name, title, renderer, default="" ):
    def getter( item, formatter ):
        value = getattr( item, name )
        if value:
            return renderer( value )
        return default
    return column.GetterColumn( title, getter )
    
def day_column( name, title, default="" ):
    renderer = lambda x: x.strftime('%Y-%m-%d')
    return _column( name, title, renderer, default)
    
def name_column( name, title, default=""):
    def renderer( value, size=50 ):
        if len(value) > size:
            return "%s..."%value[:size]
        return value
    return _column( name, title, renderer, default)
    
def vocab_column( name, title, vocabulary_source ):
    def getter( item, formatter ):
        value = getattr( item, name)
        if not value:
            return ''
        formatter_key = "vocabulary_%s"%name
        vocabulary = getattr( formatter, formatter_key, None)
        if vocabulary is None:
            vocabulary = vocabulary_source()
            setattr( formatter, formatter_key, vocabulary)
        term = vocabulary.getTerm( value )
        return term.title or term.token
    return column.GetterColumn( title, getter )
        
def member_fk_column( name, title, default=""):
    def getter( item, formatter ):
        value = getattr( item, name)
        if not value:
            return default
        session = Session()
        member = session.query( domain.Person ).get( value )
        return u"%s %s"%(member.first_name, member.last_name)
    return column.GetterColumn( title, getter )

def lookup_fk_column(name, title, domain_model, field, default=""):
    def getter( item, formatter ):
        value = getattr( item, name)
        if not value:
            return default
        session = Session()
        member = session.query( domain_model ).get( value )
        return member.__dict__[field]
    return column.GetterColumn( title, getter )
     
     
def inActiveDead_Column( name, title, default):
    #[(_(u"active"),'A'),(_(u"inactive"), 'I'),(_(u"deceased"), 'D')]
    aid = { 'A': _(u"active"),
        'I': _(u"inactive"),
        'D': _(u"deceased")}    
    renderer = lambda x: aid[x]
    return _column( name, title, renderer, default)  
     
####
#  Constraints / Invariants
#  

def ElectionAfterStart(obj):
    """ Start Date must be after Election Date"""        
    if obj.election_date >= obj.start_date:
        raise interface.Invalid(
            _("A parliament has to be elected before it can be sworn in"), 
            "election_date", 
            "start_date")
   
def EndAfterStart(obj):
    """ End Date must be after Start Date"""    
    if obj.end_date is None: return
    if obj.end_date <= obj.start_date:
        raise interface.Invalid(
            _("End Date must be after Start Date"), 
            "start_date", 
            "end_date")

def DissolutionAfterReinstatement( obj ):       
    """ A committee must be disolved before it can be reinstated """   
    if (obj.dissolution_date is None) or (obj.reinstatement_date is None): 
        return
    if obj.dissolution_date > obj.reinstatement_date:
        raise interface.Invalid(
            _("A committee must be disolved before it can be reinstated"), 
            "dissolution_date", 
            "reinstatement_date" )

def ActiveAndSubstituted( obj ):
    """ A person cannot be active and substituted at the same time"""
    if obj.active_p and obj.replaced_id:
        raise interface.Invalid(
            _("A person cannot be active and substituted at the same time"), 
            "active_p", 
            "replaced_id")

def SubstitudedEndDate( obj ):
    """ If a person is substituted he must have an end date"""
    if not (obj.end_date) and obj.replaced_id:    
        raise interface.Invalid(
            _("If a person is substituted End Date must be set"), 
            "replaced_id", 
            "end_date")
        
def InactiveNoEndDate( obj ):
    """ If you set a person inactive you must provide an end date """
    if not obj.active_p:
        if not (obj.end_date):
            raise interface.Invalid(
                _("If a person is inactive End Date must be set"), 
                "end_date", 
                "active_p")
        
def MpStartBeforeElection( obj ):
    """ For members of parliament start date must be after election """                
    if obj.election_nomination_date > obj.start_date:
        raise interface.Invalid(
            _("A parliament member has to be elected/nominated before she/he can be sworn in"), 
            "election_nomination_date", 
            "start_date")    
            

def DeathBeforeLife(User):
    """Check if date of death is after date of birth"""
    if User.date_of_death is None: return
    if User.date_of_death < User.date_of_birth:       
        raise interface.Invalid(
            _(u"One cannot die before being born"),     
            "date_of_death", 
            "date_of_birth")
    
def IsDeceased(User):
    """If a user is deceased a date of death must be given"""
    if User.active_p is None: 
        if User.date_of_death is None: 
            return
        else: 
            raise interface.Invalid(
                _(u"If a user is deceased he must have the status 'D'"), 
                "date_of_death", 
                "active_p" )
    if User.active_p == 'D':
        if User.date_of_death is None:
            raise interface.Invalid(
                _(u"A Date of Death must be given if a user is deceased"), 
                "date_of_death", 
                "active_p" )
    else:
        if User.date_of_death is not None:
            raise interface.Invalid(
                _(u"If a user is deceased he must have the status 'D'"), 
                "date_of_death", 
                "active_p" )
    
def POBoxOrAddress( obj ):
    """
    An Address must have either an entry for a physical address or a P.O. Box    
    """
    if obj.po_box is None and  obj.address is None:
        raise interface.Invalid(
            _(u"You have to enter either a P.O. Box or a Street Address"), 
            "po_box", 
            "address" )
        
            
####
# Descriptors

class UserDescriptor( ModelDescriptor ):
    fields = [
        dict( name="user_id", 
                listing_column=member_fk_column("user_id", _(u'Name')), 
                listing=True, 
                edit=False, 
                add=False, 
                view=False),
        dict( name="titles", 
              label=_(u"Salutation"), 
                description=_(u"e.g. Mr. Mrs, Prof. etc.")),
        dict( name="first_name", label=_(u"First Name")),
        dict( name="middle_name", label=_(u"Middle Name")),        
        dict( name="last_name", label=_(u"Last Name")), 
        dict( name="email",
              property = schema.TextLine( title =_(u"Email"), 
                          description=_(u"Email address"),
                          constraint=check_email,
                          required=True
                          ),
             ),                                                                                
        dict( name="login", label=_(u"Login Name")),
        dict( name="national_id", label=_(u"National Id")),
        dict( name="gender", 
              property = schema.Choice( 
              title=_(u"Gender"), 
              source=vocabulary.Gender ),
              edit_widget=CustomRadioWidget ),
        dict( name="date_of_birth", 
              label=_(u"Date of Birth"), 
              edit_widget=calendar.CalendarWidget, 
              add_widget=calendar.CalendarWidget),
        dict( name="birth_country", 
              property = schema.Choice( 
              title=_(u"Country of Birth"), 
            source=DatabaseSource(domain.Country, 
                    token_field='country_id', 
                    title_field='country_name',
                    value_field='country_id' ),                                        
                    required=True ),             
            ),
        dict( name="birth_nationality", 
              property = schema.Choice( 
                title=_(u"Nationality at Birth"), 
                source=DatabaseSource(domain.Country, 
                    token_field='country_id', 
                    title_field='country_name',
                    value_field='country_id' ),                                        
                required=True ),             
            ),
        dict( name="current_nationality", 
              property = schema.Choice( 
                title=_(u"Current Nationality"), 
                source=DatabaseSource(domain.Country, 
                token_field='country_id', 
                title_field='country_name',
                value_field='country_id' ),                                        
            required=True ),             
            ),
        dict( name="date_of_death", label=_(u"Date of Death"),
              #view_permission="bungeni.user.AdminRecord",
              edit_permission="bungeni.user.AdminRecord",
              edit_widget=calendar.CalendarWidget, 
              add_widget=calendar.CalendarWidget),
        dict( name="password", omit=True ),
        dict( name="active_p", label=_(u"Status"), 
              property = schema.Choice( 
                title=_(u"Status"), 
                source=vocabulary.InActiveDead, default='A' ),
              listing_column=inActiveDead_Column("active_p", _(u'Status'), ''),
              #view_permission="bungeni.user.AdminRecord",
              edit_permission="bungeni.user.AdminRecord",  
              listing=True,
              edit_widget=CustomRadioWidget),
        dict( name="description", 
              property=schema.Text(title=_(u"Notes"), required=False),
              view_widget=HTMLDisplay,
              edit_widget=RichTextEditor, 
              add_widget=RichTextEditor 
               ),
        dict( name ="image", 
                label=_(u"Image"), 
                description=_(u"Picture of the person"),
                view_widget=ImageDisplayWidget,
                edit_widget = ImageInputWidget,
                listing=False),       
        dict( name="salt", omit=True),
        dict( name="type", omit=True ),
        ]
        
    schema_invariants = [DeathBeforeLife, IsDeceased]


class MemberDescriptor( UserDescriptor ):

    fields = deepcopy( UserDescriptor.fields )

class StaffMemberDescriptor( UserDescriptor ):
    display_name = _(u"Staff member")
    container_name = _(u"Staff members")
    
    fields = deepcopy( UserDescriptor.fields )	        
        
class HansardReporterDescriptor( UserDescriptor ):
	
    fields = deepcopy( UserDescriptor.fields )	        

class GroupMembershipDescriptor( ModelDescriptor ):

   SubstitutionSource = DatabaseSource(domain.ParliamentMember,  
                    token_field='user_id', 
                    title_field='fullname', 
                    value_field='user_id')                                          
   fields = [
        dict( name="user_id",
              property=schema.Choice( 
                title=_(u"Member of Parliament"), 
                source=DatabaseSource(domain.Person,  
                    token_field='user_id', 
                    title_field='fullname', 
                    value_field='user_id')),
                listing_column=member_fk_column("user_id", 
                    _(u'Member of Parliament')), 
              listing=True,
            ),                 
        dict( name="start_date", label=_(u"Start Date"), 
            listing_column=day_column("start_date", 
                _(u'Start Date') ), 
                listing=True,
            edit_widget=SelectDateWidget, add_widget=SelectDateWidget ),
        dict( name="end_date", 
                label=_(u"End Date"), 
                listing=True,
                listing_column=day_column("end_date", 
                _(u'End Date')), 
                edit_widget=SelectDateWidget, 
                add_widget=SelectDateWidget ),
        dict( name="active_p", label=_(u"Active"), view=False),
        dict( name="notes", 
                label=_(u"Notes"), 
                view_widget=HTMLDisplay,
                edit_widget=RichTextEditor,
                add_widget=RichTextEditor
             ),
        dict( name="substitution_type", 
                label=_(u"Type of Substitution"), 
                add = False ),
        dict( name="replaced_id", 
                property=schema.Choice( 
                    title=_(u"Substituted by"), 
                    source=SubstitutionSource, 
                    required=False),
                add = False
                ), 
        dict( name="group_id", omit=True),
        dict( name="membership_id", omit=True),
        dict( name="status", omit=True ),
        dict( name="membership_type", omit=True )
        ]
        
   schema_invariants = [EndAfterStart, ActiveAndSubstituted,
        SubstitudedEndDate, InactiveNoEndDate]


class MpDescriptor ( ModelDescriptor ):
    display_name = _(u"Member of parliament")
    container_name = _(u"Members of parliament")
    
    fields = deepcopy(GroupMembershipDescriptor.fields)    
    constituencySource=DatabaseSource(domain.Constituency,  
                    token_field='constituency_id', 
                    title_field='name', 
                    value_field='constituencye_id')
    #mpTypeSource= ['E', 'N', 'O']
    fields.extend([
        dict( name="constituency_id",
            property=schema.Choice( 
                title=_(u"Constituency"), 
                source=constituencySource,),
            listing_column=vocab_column( 
                "constituency_id" , 
                _(u'Constituency'), 
                constituencySource, ),
            listing=True),   
        dict( name="elected_nominated", 
            property=schema.Choice( 
                title=_(u"elected/nominated"), 
                source=vocabulary.ElectedNominated), 
                listing=True,            
            ),
        dict( name="election_nomination_date", 
            label=_("Election/Nomination Date"), 
            required=True, 
            edit_widget=SelectDateWidget, 
            add_widget=SelectDateWidget ),
        dict( name="leave_reason", label=_("Leave Reason")),     
    ])
    schema_invariants = [EndAfterStart, ActiveAndSubstituted, 
            SubstitudedEndDate, InactiveNoEndDate, MpStartBeforeElection]
    
class PartyMemberDescriptor( ModelDescriptor ):
    display_name=_(u"Party member")
    container_name=_(u"Party members")
    
    fields = deepcopy(GroupMembershipDescriptor.fields)
    
class MemberOfPartyDescriptor( ModelDescriptor ):
    """Describes the partymembership of a user rather then the
    membership of a user in a party."""
    
    display_name = _(u"Party membership")
    container_name = _(u"Party memberships")
    
    partySource=DatabaseSource(domain.PoliticalParty,  
                    token_field='party_id', 
                    title_field='short_name', 
                    value_field='party_id')
    fields = [
        dict( name="user_id", omit=True),                 
        dict( name='short_name', 
            label=_(u"Political Party"), 
            listing=True),
        dict( name="start_date", 
            label=_(u"Start Date"), 
            listing_column=day_column("start_date", 
                _(u'Start Date') ), 
                listing=True,
            edit_widget=SelectDateWidget, 
            add_widget=SelectDateWidget ),
        dict( name="end_date", 
            label=_(u"End Date"), 
            listing=True,
            listing_column=day_column("end_date", 
                _(u'End Date')), 
            edit_widget=SelectDateWidget, 
            add_widget=SelectDateWidget ),
        dict( name="active_p", 
            label=_(u"Active"), 
            view=False),
        dict( name="notes", 
                label=_(u"Notes"), 
                view_widget=HTMLDisplay,
                edit_widget=RichTextEditor,
                add_widget=RichTextEditor
             ),
        dict( name="substitution_type", omit=True),
        dict( name="replaced_id", omit=True),
        dict( name="membership_id", omit=True),
        dict( name="status", omit=True ),
        dict( name="membership_type", omit=True )
        ]
        
    schema_invariants = [EndAfterStart]

class ExtensionMemberDescriptor( ModelDescriptor ):
    display_name =_(u"Additional member")
    container_name =_(u"Additional members")
    custom_validators = validations.check_valid_date_range,
    
    fields = deepcopy(GroupMembershipDescriptor.fields)


class GroupDescriptor( ModelDescriptor ):

    fields = [
        dict( name="group_id", omit=True ),
        dict( name="type", omit=True ),
        dict( name="short_name", 
                label=_(U"Name"), 
                listing=True,
                listing_column=name_column("short_name", 
                    _(u'Name'))),
        dict( name="full_name", 
                label=_(u"Full Name"), 
                listing=True,
                listing_column=name_column("full_name", 
                    _(u'Full Name'))),
        dict( name="description", 
                property=schema.Text(title=_(u"Description") , 
                    required=False ),
              view_widget=HTMLDisplay,
              edit_widget=RichTextEditor,
              add_widget=RichTextEditor),
        dict( name="start_date", 
                label=_(u"Start Date"), 
                listing=True, 
                listing_column=day_column("start_date", 
                    _(u'Start Date')), 
                edit_widget=calendar.CalendarWidget, 
                add_widget=calendar.CalendarWidget),
        dict( name="end_date", 
                label=_(u"End Date"), 
                listing=True, 
                listing_column=day_column('end_date', 
                    _(u'End Date')), 
                    edit_widget=SelectDateWidget, 
                    add_widget=SelectDateWidget),        
        dict( name="status", omit=True),
        ]

    schema_invariants = [EndAfterStart]

class ParliamentDescriptor( GroupDescriptor ):
    display_name = _(u"Parliament")
    container_name = _(u"Parliaments")
    custom_validators = validations.check_parliament_date_no_overlap,
    
    fields = [
        dict( name="group_id", omit=True ),
        dict( name="parliament_id", omit=True ),
        dict( name="short_name", 
                label=_(u"Parliament Identifier"), 
                description=_(u"Unique identifier of each Parliament (e.g. nth Parliament)"), 
                listing=True ),
        dict( name="full_name", 
                label=_(u"Name"), 
                description=_(u"Parliament name"), 
                listing=True,
                listing_column=name_column("full_name", "Name") ),
        dict( name="description", 
              property=schema.Text(title=_(u"Description"), required=False),
              view_widget=HTMLDisplay,
              edit_widget=RichTextEditor, 
              add_widget=RichTextEditor 
               ),
        dict( name="election_date",
              label=_(u"Election Date"), 
              description=_(u"Date the of the election"),
              edit_widget=calendar.CalendarWidget, 
              add_widget=calendar.CalendarWidget
              ),        
        dict( name="start_date",
              label=_(u"In power from"), 
              description=_(u"Date the of the swearing in"),
              listing_column=day_column("start_date", _(u"In power from") ), 
              listing=True, 
              edit_widget=SelectDateWidget,
              add_widget=SelectDateWidget 
              ),
        dict( name="end_date", 
              label=_(u"In power till"),
              description=_(u"Date the of the dissolution"), 
              listing_column=day_column("end_date", _(u"In power till")),
              listing=True,
              edit_widget=SelectDateWidget,
              add_widget=SelectDateWidget 
              ),
        dict( name="status", omit=True),
        dict( name="type", omit=True),
        ]
    schema_invariants = [EndAfterStart, ElectionAfterStart]
            
class CommitteeDescriptor( GroupDescriptor ):
    display_name = _(u"Committee")
    container_name = _(u"Committees")
    custom_validators = validations.check_valid_date_range,
    
    fields = deepcopy( GroupDescriptor.fields )
    typeSource = DatabaseSource(domain.CommitteeType, 
                    token_field='committee_type_id', 
                    title_field='committee_type', 
                    value_field='committee_type_id')
    fields.extend([
        dict( name='parliament_id', omit=True ),
        dict( name='committee_id', omit=True ),
        dict( name = 'committee_type_id',
                property=schema.Choice( title=_(u"Type of committee"), 
                    source=typeSource),
                listing_column=vocab_column( "committee_type_id" , 
                    _(u"Type"), 
                    typeSource, ), 
                    listing=True,
            
            ),
        dict( name='no_members', 
            label=_(u"Number of members"), 
            description=_(u"") ),
        dict( name='min_no_members', 
            label =_(u"Minimum Number of Members")),
        dict( name='quorum', 
            label=_(u"Quorum")),
        dict( name='no_clerks', 
            label=_(u"Number of clerks")),
        dict( name='no_researchers', 
            label=_(u"Number of researchers")),
        dict( name='proportional_representation', 
            label=_(u"Proportional representation")),       
        dict( name='default_chairperson', 
            label=_(u"Default chairperson")),
        dict( name='dissolution_date', 
            label=_(u"Dissolution date"), 
            edit_widget=SelectDateWidget, 
            add_widget=SelectDateWidget ),
        dict( name='reinstatement_date', 
            label=_(u"Reinstatement Date"), 
            edit_widget=SelectDateWidget, 
            add_widget=SelectDateWidget ),              
    ])
    schema_invariants = [EndAfterStart,] # DissolutionAfterReinstatement]
    
class CommitteeMemberDescriptor( ModelDescriptor ):
    display_name = _(u"Committee member")
    container_name = _(u"Committee members")
    
    fields = deepcopy(GroupMembershipDescriptor.fields)    
    schema_invariants = [EndAfterStart, ActiveAndSubstituted, 
            SubstitudedEndDate, InactiveNoEndDate]
    
class MemberRoleTitleDescriptor( ModelDescriptor ):
    display_name= _(u"Title")
    container_name= _(u"Titles")
    
    fields = [
        dict( name='role_title_id', omit=True),
        dict( name='membership_id', omit=True),
        dict( name='title_name_id', label=_(u"Title"),
                property=schema.Choice( title=_(u"Title"), 
                  source=DatabaseSource(domain.MemberTitle,  
                    token_field='user_role_type_id', 
                    title_field='user_role_name', 
                    value_field='user_role_type_id')
                  ),
                  listing_column = lookup_fk_column( 
                    "title_name_id", 
                    _(u'Title'), 
                    domain.MemberTitle, 
                    'user_role_name' ),
                  listing=True,
              ),
        dict( name="start_date", 
                label=_(u"Start Date"), 
                listing=True, 
                listing_column=day_column("start_date",
                     _(u'Start Date')), 
                edit_widget=calendar.CalendarWidget, 
                add_widget=calendar.CalendarWidget),
        dict( name="end_date", 
                label=_(u"End Date"), 
                listing=True, 
                listing_column=day_column('end_date', 
                    _(u'End Date')), 
                    edit_widget=SelectDateWidget, 
                    add_widget=SelectDateWidget), 
    ]
       
    schema_invariants = [EndAfterStart]     
    
class CommitteeStaffDescriptor( ModelDescriptor ):
    display_name = _(u"Committee staff")
    container_name = _(u"Committee staff members")
    
    fields = deepcopy(GroupMembershipDescriptor.fields)     
    
    schema_invariants = [EndAfterStart, ActiveAndSubstituted, 
            SubstitudedEndDate, InactiveNoEndDate]     
        
class PoliticalPartyDescriptor( GroupDescriptor ):
    display_name = _(u"Political party")
    container_name = _(u"Political parties")
    custom_validators = validations.check_valid_date_range,
    
    fields = deepcopy( GroupDescriptor.fields )    
    fields.extend([
        dict( name='logo_data', 
                label=_(u"Logo"), 
                edit=True, 
                add=True, 
                view=True, 
                listing=False,
                view_widget=ImageDisplayWidget,
                edit_widget = ImageInputWidget),
        dict(name="parliament_id", omit=True),   
        dict(name="party_id", omit=True),                           
     ])
          
    schema_invariants = [EndAfterStart]
    
class ExtensionGroupDescriptor( GroupDescriptor ):
    display_name = _(u"Group extension")
    container_name = _(u"Group extensions")
    custom_validators = validations.check_valid_date_range,
    
    fields = deepcopy( GroupDescriptor.fields )    
    fields.extend([
        dict(name="group_type", listing=True,
            property = schema.Choice(
                title=_(u"Extension for"), 
                values=['ministry', 'committee',])
            ),
        dict(name="extension_type_id", omit=True),  
        dict(name="parliament_id", omit=True),           
    ])   
     
class MinistryDescriptor( GroupDescriptor ):
    display_name = _(u"Ministry")
    container_name = _(u"Ministries")
    custom_validators = validations.check_valid_date_range,
    
    fields = deepcopy( GroupDescriptor.fields )       
    fields.extend([
        dict( name='ministry_id', omit=True ),
        dict( name='government_id', omit=True ),
                   
    ])
    
    schema_invariants = [EndAfterStart]
    
class MinisterDescriptor( ModelDescriptor ):    
    display_name = _(u"Minister")
    container_name = _(u"Ministers")
    
    fields = deepcopy(GroupMembershipDescriptor.fields)

    schema_invariants = [ActiveAndSubstituted, SubstitudedEndDate,
            InactiveNoEndDate]
    
class ParliamentSession( ModelDescriptor ):
    display_name = _(u"Parliamentary session")
    container_name = _(u"Parliamentary sessions")
    
    fields = deepcopy( GroupDescriptor.fields )
    fields.extend([
        dict( name="session_id", omit=True ),
        dict( name="start_date", 
                label=_(u"Start Date"), 
                listing_column=day_column("start_date", 
                    _(u'Start Date')), 
            edit_widget=SelectDateWidget, 
            add_widget=SelectDateWidget),
        dict( name="end_date", 
            label=_(u"End Date"), 
            listing_column=day_column('end_date', 
                _(u'End Date')),
            edit_widget=SelectDateWidget, 
            add_widget=SelectDateWidget),                
        dict( name="notes", 
              property=schema.Text(title=_(u"Notes"), 
                required=False ),
              view_widget=HTMLDisplay,
              edit_widget=RichTextEditor,
              add_widget=RichTextEditor )
        ])
        
    schema_invariants = [EndAfterStart]        
        
class GovernmentDescriptor( ModelDescriptor ):
    display_name = _(u"Government")
    container_name = _(u"Governments")
    
    fields = [
        dict( name="group_id", omit=True ),
        dict( name="short_name", 
                label=_(u"Name"), 
                description=_(u"Name of the Head of Government"), 
                listing=True),
        dict( name="full_name", 
                label=_(u"Number")),       
        dict( name="start_date", 
                label=_(u"In power from"), 
                listing=True, 
                listing_column=day_column("start_date", 
                    _(u"In power from")), 
                edit_widget=SelectDateWidget, 
                add_widget=SelectDateWidget ),
        dict( name="end_date", 
                label=_(u"In power till"), 
                listing=True,
                listing_column=day_column("end_date", _(u"In power till")), 
                edit_widget=SelectDateWidget, 
                add_widget=SelectDateWidget ),
        dict( name="description", 
                property=schema.Text(title=_(u"Notes") , required=False),
                view_widget=HTMLDisplay,
                edit_widget=RichTextEditor,
                add_widget=RichTextEditor
            ),
        dict( name="status", omit=True),
        dict( name="government_id", omit=True), 
        dict( name="parliament_id", omit=True),   
        dict( name="type", omit=True ),  
        ]
    
    schema_invariants = [EndAfterStart]    

class ParliamentaryItemDescriptor( ModelDescriptor ):
    fields= [
        dict(name="parliamentary_item_id", omit=True),
        dict(name="parliament_id", omit=True),
        dict( name="owner_id", 
              property = schema.Choice( title=_(u"Owner"), 
                source=DatabaseSource(domain.ParliamentMember, 
                title_field='fullname', 
                token_field='user_id', 
                value_field = 'user_id' )), 
              listing_column=vocab_column( "owner_id" , _(u'Owner'),
               DatabaseSource(domain.ParliamentMember, 
                title_field='fullname', 
                token_field='user_id', 
                value_field = 'user_id' ), ),              
              listing = True 
            ),
        dict(name="short_name", 
            label=_(u"Title"), 
            listing=True, 
            add=True, 
            edit=True, 
            omit=False),
        dict(name="full_name", 
            label=_(u"Summary"), 
            listing=False, 
            add=True, 
            edit=True, 
            omit=False),
        dict(name="language", 
             label=_(u"Language"), 
             listing=True, 
             add=True, 
             edit=False, 
             omit=False,
             required=True,
             property=schema.Choice(
                 title=u"Language",
                 default=get_default_language(),
                 vocabulary=SimpleVocabulary.fromItems(
                     [(title, name) for (name, title) in available_languages()]),
                 ),
             ),
        dict( name="body_text", label=_(u"Text"),
              property = schema.Text( title=u"Text" ),
              view_widget=HTMLDisplay,
              edit_widget=RichTextEditor, 
              add_widget=RichTextEditor
              ),
        dict( name="submission_date", 
            label=_(u"Submission Date"), 
            add=False, 
            edit=False, 
            listing=True ,  
            edit_widget=SelectDateWidget, 
            add_widget=SelectDateWidget, 
            omit=False),        
        dict( name="status", 
            label=_(u"Status"), 
            edit=False, 
            add=False, 
            listing=True, 
            omit=False ),            
        dict( name="note", 
            label=_(u"Notes"), 
            description="Recommendation note", 
              property=schema.Text(title=_(u"Notes"),  
                description=_(u"Recommendation note"), required=False ),              
              edit = True, 
              add = True, 
              view = False, 
              view_widget=HTMLDisplay,
              edit_widget=RichTextEditor, ),    
        dict( name="receive_notification", 
              label=_(u"Receive notification"), 
              description=_(u"Select this option to receive notifications for this motion."), 
              listing=False, 
              omit=False ),  
        dict( name="type", 
              omit=False,
              edit = False, 
              add = False, 
              view = False, ),
        ]                   

class AgendaItemDescriptor( ParliamentaryItemDescriptor): 
    display_name =_(u"Agenda item")
    container_name =_(u"Agenda items")
    fields = deepcopy( ParliamentaryItemDescriptor.fields )    
    fields.extend([
        dict( name="agenda_item_id", omit=True ), 
    ])
        
class MotionDescriptor( ParliamentaryItemDescriptor ):
    display_name = _(u"Motion")
    container_name = _(u"Motions")
    fields = deepcopy( ParliamentaryItemDescriptor.fields )    
    fields.extend([                
        dict( name="approval_date", 
            label=_(u"Approval Date"), 
            add=False, 
            edit=False, 
            edit_widget=SelectDateWidget, 
            add_widget=SelectDateWidget),
        dict( name="notice_date", 
            label=_(u"Notice Date"), 
            add=False, 
            edit= False, 
            listing=True, 
            edit_widget=SelectDateWidget, 
            add_widget=SelectDateWidget),        
        dict( name="motion_number", 
            label=_(u"Identifier"), 
            add=False, 
            edit = False),


        # TODO omit for now
        dict( name="entered_by", label=_(u"Entered By"), omit=True ), 
        dict( name="party_id",
            property = schema.Choice( title=_(u"Political Party"), 
              source=DatabaseSource(domain.PoliticalParty, 
                title_field='short_name', 
                token_field='party_id', 
                value_field = 'party_id' ), 
              required=False) ),                
        ])

class BillDescriptor( ParliamentaryItemDescriptor ):
    display_name = _(u"Bill")
    container_name = _(u"Bills")
    fields = deepcopy( ParliamentaryItemDescriptor.fields )    
    fields.extend([
        dict( name="bill_id", omit=True ),
        dict( name="bill_type_id", property = schema.Choice(
                title =_(u"Bill Type"),
                source=DatabaseSource(domain.BillType, 
                    title_field='bill_type_name',
                    token_field='bill_type_id',
                    value_field='bill_type_id'),
                ),
             ),                                                                
        dict( name="ministry_id", 
              property = schema.Choice( title=_(u"Ministry"), 
                        source=DatabaseSource(domain.Ministry, 
                            title_field='short_name', 
                            token_field='ministry_id', 
                            value_field = 'ministry_id' ),
                    required=False,
                    ), 
             listing = False,),

        dict( name="summary", 
                label=_(u"Summary"), 
                view_widget=HTMLDisplay,
                edit_widget=RichTextEditor, 
                add_widget=RichTextEditor),
        dict( name="identifier", label=_(u"Identifer") ),
        dict( name="publication_date", 
                label=_(u"Publication Date"), 
                listing=True,  
                edit_widget=SelectDateWidget, 
                add_widget=SelectDateWidget ,
                listing_column=day_column("publication_date", 
                    _(u"Publication Date")), ),        

        ])
        
class QuestionDescriptor( ParliamentaryItemDescriptor ):
    display_name = _(u"Question")
    container_name = _(u"Questions")
    custom_validators = ()
    
    fields = deepcopy( ParliamentaryItemDescriptor.fields )    
    fields.extend([
        dict( name="question_id", omit=True),
        dict( name="supplement_parent_id",
            label=_(u"Initial/supplementary question"), 
            view_widget=SupplementaryQuestionDisplay),
        dict( name="ministry_id", 
                property = schema.Choice(title=_(u"Ministry"), 
                source=DatabaseSource(domain.Ministry,
                    title_field='short_name', 
                    token_field='ministry_id', 
                    value_field = 'ministry_id' ),
                 required=False),
                listing_column=vocab_column( "ministry_id" , _(u'Ministry'),
                DatabaseSource(domain.Ministry,
                                title_field='short_name', 
                                token_field='ministry_id', 
                                value_field = 'ministry_id' )),
                listing=True,                 
            ),
        dict( name="approval_date", 
            label=_(u"Date approved"),  
            listing=True, 
            add=False ),     
        dict( name="ministry_submit_date", 
            label=_(u"Submitted to ministry"),  
            listing=True, 
            add=False ),   
        dict( name="question_type", 
            listing=True, 
            property=schema.Choice( title=_(u"Question Type"), 
                        description=_("(O)rdinary or (P)rivate Notice"), 
                        vocabulary=vocabulary.QuestionType) ,
              ),                                    
        dict( name="response_type",  
            listing=True,
            property=schema.Choice( title=_(u"Response Type"), 
                      description=_("(O)ral or (W)ritten"), 
                      vocabulary=vocabulary.ResponseType),

             ),
        dict( name="sitting_time", 
            label=_(u"Sitting Time"), 
            listing=True ),
        ])

class EventItemDescriptor( ParliamentaryItemDescriptor ):
    display_name =_(u"Event")
    container_name =_(u"Events")
    fields = deepcopy( ParliamentaryItemDescriptor.fields )    
    fields.extend([
        dict( name="event_item_id", omit=True ),
        dict( name="item_id", omit=True ),
        dict( name="event_date", 
            label=_(u"Date"), 
            listing_column=day_column("event_date", _(u"Date")), 
            listing=True, 
            edit_widget=SelectDateWidget, 
            add_widget=SelectDateWidget ),
    ])




class MotionAmendmentDescriptor( ModelDescriptor ):
    display_name = _(u"Motion amendment")
    container_name = _(u"Motion amendments")
    
    fields = [
        dict( name="amendment_id", omit=True ),
        dict( name="motion_id", omit=True ),
        dict( name="amended_id", omit=True ),
        dict( name="title", 
                label=_(u"Subject"), 
                listing=True,
                edit_widget = widgets.LongTextWidget),
        dict( name="body_text", 
                label=_(u"Motion Amendment Text"),
                property = schema.Text( title=u"Motion Amendment" ),
                view_widget=HTMLDisplay,
                edit_widget=RichTextEditor, 
                add_widget=RichTextEditor
              ),
        dict( name="submission_date", 
                label=_(u"Submission Date"),  
                edit_widget=SelectDateWidget, 
                add_widget=SelectDateWidget),
        dict( name="vote_date", 
                label=_(u"Vote Date"),  
                edit_widget=SelectDateWidget, 
                add_widget=SelectDateWidget),
        dict( name="accepted_p",  label=_(u"Accepted")),
        ]
class SittingDescriptor( ModelDescriptor ):
    display_name = _(u"Sitting")
    container_name = _(u"Sittings")
    
    fields = [
        dict( name="sitting_id", omit=True ),
        dict( name="group_id", omit=True ),
        dict( name="sitting_type_id", 
              listing_column = vocab_column( "sitting_type_id", 
                _(u"Sitting Type"), 
                vocabulary.SittingTypes ),
              property = schema.Choice( 
                    title=_(u"Sitting Type"), 
                    source=vocabulary.SittingTypes,
                    required=True) ),
        dict( name="start_date", 
            label=_(u"Start Date"),  
            listing_column=day_column("start_date", 
                _(u'Start Date')),
            edit_widget=SelectDateTimeWidget, 
            add_widget=SelectDateTimeWidget),
        dict( name="end_date", 
                label=_(u"End Date"),  
                listing_column=day_column("end_date", 
                    _(u'End Date')),
                edit_widget=SelectDateTimeWidget, 
                add_widget=SelectDateTimeWidget),
        ]

    schema_invariants = [EndAfterStart]
    
    
class SessionDescriptor( ModelDescriptor ):
    display_name = _(u"Parliamentary session")
    container_name = _(u"Parliamentary sessions")
    
    fields = [
        dict( name="session_id", omit=True),
        dict( name="parliament_id", omit=True),
        dict( name="short_name", label=_(u"Short Name"), listing=True ),
        dict( name="full_name", label=_(u"Full Name") ),
        dict( name="start_date", 
            label=_(u"Start Date"), 
            listing=True, 
            listing_column=day_column("start_date", 
                _(u'Start Date')),
            edit_widget=SelectDateWidget, 
            add_widget=SelectDateWidget),
        dict( name="end_date", 
            label=_(u"End Date"), 
            listing=True, 
            listing_column=day_column("end_date", 
                _(u'End Date')),
            edit_widget=SelectDateWidget, 
            add_widget=SelectDateWidget),
        dict( name="notes", label=_(u"Notes"), required=False)
        ]
    schema_invariants = [EndAfterStart]
            
class DebateDescriptor ( ModelDescriptor ):
    display_name = _(u"Debate")
    container_name = _(u"Debate")
    
    fields = [
        dict( name="sitting_id", omit=True ), 
        dict( name="debate_id", omit=True ),                
        dict( name="short_name", 
                label=_(u"Short Name"), 
                listing=True,
                listing_column=name_column("short_name", 
                    _(u'Name')) ), 
        dict( name="body_text", label=_(u"Transcript"),
              property = schema.Text( title=u"Transcript" ),
              view_widget=HTMLDisplay,
              edit_widget=RichTextEditor, 
              add_widget=RichTextEditor
              ),   
        ]             
        
class AttendanceDescriptor( ModelDescriptor ):
    display_name =_(u"Sitting attendance")
    container_name =_(u"Sitting attendances")
    
    attendanceVocab = DatabaseSource(
        domain.AttendanceType, 
                    token_field='committee_type_id', 
                    title_field='committee_type', 
                    value_field='committee_type_id' )                                                                    
        
    fields = [
        dict( name="sitting_id", omit=True ),
        dict( name="member_id", listing=True,
                property = schema.Choice(title=_(u"Attendance"), 
                source=DatabaseSource(domain.Person,  
                    title_field='fullname', 
                    token_field='user_id', 
                    value_field = 'user_id')), 
              listing_column=member_fk_column("member_id", 
                _(u'Member of Parliament') ) 
              ),
        dict( name="attendance_id", listing=True, 
                property = schema.Choice( 
                    title=_(u"Attendance"), 
                    source=attendanceVocab, 
                    required=True),
                listing_column = vocab_column(
                    "attendance_id", 
                    _(u'Attendance'), 
                    attendanceVocab )),            
        ]
        
class AttendanceTypeDescriptor( ModelDescriptor ):        
    display_name =_(u"Sitting attendance")
    container_name =_(u"Sitting attendances")
    
    fields = [
        dict (name="attendance_id", omit=True ),
        dict (name="attendance_type", label=_(u"Attendance type") ),
        ]
        


class BillConsignatoryDescriptor( ModelDescriptor ):
    display_name = _(u"Consignatory")
    container_name = _(u"Consignatories")
    
    fields = [
        dict(name="bill_id", omit = True),
        dict( name="user_id",
              property=schema.Choice( 
                title=_(u"Consignatory"), 
                source=DatabaseSource(domain.Person,  
                    title_field='fullname', 
                    token_field='user_id', 
                    value_field = 'user_id')),
              listing_column=member_fk_column("user_id", 
                _(u'Consignatory')), 
            listing=True, 
            ),  
    ]


        
class ResponseDescriptor( ModelDescriptor ):
    display_name = _(u"Response")
    container_name = _(u"Responses")
    
    fields = [
        dict( name="response_id", omit=True ),
        dict( name="question_id", omit=True ), #XXX
        dict( name="response_text", 
                label=_(u"Response"), 
                description=_(u"Response to the Question"),
                view_widget=HTMLDisplay,
                edit_widget=RichTextEditor, 
                add_widget=RichTextEditor ),
        dict( name="sitting_time", 
                label=_(u"Sitting Time"), 
                description=_(u"Time of the Sitting"), 
                listing=True ),
        ]        

class ConstituencyDescriptor( ModelDescriptor ):
    provinceSource=DatabaseSource(domain.Province,
                    token_field='province_id', 
                    title_field='province', 
                    value_field='province_id')
    regionSource=DatabaseSource(domain.Region,
                    token_field='region_id', 
                    title_field='region', 
                    value_field='region_id')
    fields = [
        dict( name="constituency_id", omit=True ),
        dict( name="name", 
            label=_(u"Name"), 
            description=_("Name of the constituency"), 
            listing=True ),
        dict(name="province",
            property = schema.Choice( 
                title=_(u"Province"), 
                source=provinceSource,            
                required=True ),
            listing_column = vocab_column("province", 
                _(u"Province"), 
                provinceSource ), 
            listing=True,
            ),
        dict( name="region", 
            label=_(u"Region"),
            property = schema.Choice( 
                title=_(u"Region"), 
                source=regionSource,              
                required=True ),
             listing_column = vocab_column("region", 
                _(u"Region"), 
                regionSource), 
            listing=True,
            ),
        dict( name="start_date", 
                label=_(u"Start Date"), 
                listing=True, 
                listing_column=day_column('start_date', _(u"Start Date")), 
                edit_widget=SelectDateWidget, 
                add_widget=SelectDateWidget),
        dict( name="end_date", label=_(u"End Date"), 
                listing=True , 
                listing_column=day_column('end_date', _(u"End Date")), 
                edit_widget=SelectDateWidget, 
                add_widget=SelectDateWidget),        
        ]

schema_invariants = [EndAfterStart]
        
class ProvinceDescriptor( ModelDescriptor ):
    fields = [
        dict( name="province_id", omit=True ),
        dict( name="province", 
                label=_(u"Province"), 
                description=_(u"Name of the Province"), 
                listing=True ),
        ]
        
class RegionDescriptor( ModelDescriptor ):
    fields = [
        dict( name="region_id", omit=True ),
        dict( name="region", 
                label=_(u"Region"), 
                description=_(u"Name of the Region"), 
                listing=True ), 
        ]

class CountryDescriptor( ModelDescriptor ):
    fields = [
        dict( name="country_id", 
                label=_(u"Country Code"), 
                description =_(u"ISO Code of the  country")),
        dict( name="country_name", 
                label=_(u"Country"), 
                description=_(u"Name of the Country"), 
                listing=True ), 
        ]        
		
class ConstituencyDetailDescriptor( ModelDescriptor ):
    fields = [
        dict( name="constituency_detail_id", omit=True ),
        dict( name="constituency_id", 
                label=_(u"Name"), 
                description=_("Name of the constituency"), 
                listing=False, 
                omit=True ),
        dict( name="date", 
                label=_(u"Date"), 
                description=_(u"Date the data was submitted from the Constituency"), 
                listing=True,  
                listing_column=day_column("date", "Date"),
                edit_widget=SelectDateWidget, 
                add_widget=SelectDateWidget),
        dict( name="population", 
                label=_(u"Population"), 
                description=_(u"Total Number of People living in this Constituency"), 
                listing=True ),                
        dict( name="voters", 
                label=_(u"Voters"), 
                description=_(u"Number of Voters registered in this Constituency"), 
                listing=True ),
        ]

class AddressTypeDescriptor( ModelDescriptor ):
    display_name =_(u"Address type")
    container_name =_(u"Address types")
    
    fields = [
        dict( name="address_type_id", omit=True ),
        dict( name="address_type_name", label=_(u"Address Type") ),
    ]
        
class AddressDescriptor ( ModelDescriptor ):
    display_name = _(u"Address")
    container_name = _(u"Addresses")
    
    fields = [        
        dict( name="address_id", omit=True ),
        dict( name="role_title_id", omit=True ),
        dict( name="user_id", omit=True ),
        dict( name="address_type_id", 
            property = schema.Choice(
            title =_(u"Address Type"),
            source=DatabaseSource(domain.AddressType, 
                title_field='address_type_name',
                token_field='address_type_id',
                value_field='address_type_id'),)
             ),                                                                
        dict( name="po_box", label=_(u"P.O. Box") ),
        dict( name="address", 
                property = schema.TextLine( 
                    title =_(u"Address"),required=False ),
              edit_widget=zope.app.form.browser.TextAreaWidget, 
              add_widget=zope.app.form.browser.TextAreaWidget,
              ),        
        dict( name="city", label=_(u"City") ),
        dict( name="zipcode", label=_(u"Zip Code") ),
        dict( name="country",  
                property = schema.Choice( title=_(u"Country"), 
                source=DatabaseSource(domain.Country, 
                     title_field='country_name',
                     token_field='country_id', 
                     value_field='country_id' ),                                        
                required=True ), 
             ),
        dict( name="phone",  
                property = schema.Text( title=_(u"Phone Number(s)"), 
                description=_(u"Enter one phone number per line"), 
                required=False ),
              edit_widget=zope.app.form.browser.TextAreaWidget, 
              add_widget=zope.app.form.browser.TextAreaWidget,
              #view_widget=zope.app.form.browser.ListDisplayWidget,
              ),
        dict( name="fax", 
                property = schema.Text( 
                    title=_(u"Fax Number(s)"),  
                    description=_(u"Enter one fax number per line"), 
                    required=False ),
              edit_widget=zope.app.form.browser.TextAreaWidget, 
              add_widget=zope.app.form.browser.TextAreaWidget,              
              ),
        dict( name="email", 
              property = schema.TextLine( 
                title =_(u"Email"), 
                description=_(u"Email address"),
                constraint=check_email,
                required=False
                ),
             ),
        dict( name="im_id", 
            label=_(u"Instant Messenger Id"), 
            description=_(u"ICQ, AOL IM, GoogleTalk...")),
        dict( name="status", omit=True ),
        ]
        
    schema_invariants = [POBoxOrAddress]		
################
# Hansard
################
class RotaDescriptor( ModelDescriptor ):
    fields = [
        dict( name="rota_id", omit=True ),         
        dict( name="reporter_id", omit=True), #XXX
        dict( name="identifier", 
            title=_("Rota Identifier"), listing=True),
        dict( name="start_date", 
            label=_(u"Start Date"), 
            listing_column=day_column("start_date", 
                _(u"Start Date") ), 
            listing=True , 
            edit_widget=SelectDateWidget, 
            add_widget=SelectDateWidget),
        dict( name="end_date", 
            label=_(u"End Date"), 
            listing_column=day_column("end_date", 
                _(u"End Date")), 
                listing=True, 
                edit_widget=SelectDateWidget, 
                add_widget=SelectDateWidget ),
        ]

    schema_invariants = [EndAfterStart]
        

 
class DocumentSourceDescriptor( ModelDescriptor ): 
    display_name =_(u"Document source")
    container_name =_(u"Document sources")
    
    fields = [
        dict( name="document_source_id", omit=True ),
        dict( name="document_source", label=_(u"Document Souce") ),
    ] 
    
class TabledDocumentDescriptor( ModelDescriptor): 
    display_name =_(u"Tabled document")
    container_name =_(u"Tabled documents")
    
    fields = [
        dict( name="tabled_document_id", omit=True ),
        dict( name="title", label=_(u"Title"), listing=True ),
        dict( name="summary",  label=_(u"Summary") ),
        dict( name="owner_id", 
            property = schema.Choice( 
                title=_(u"Owner"), 
                    source=DatabaseSource(
                        domain.ParliamentMember, 
                        title_field='fullname', 
                        token_field='user_id', 
                        value_field = 'user_id' )), 
            listing_column=vocab_column( "owner_id" , _(u'Owner'),
                DatabaseSource(domain.ParliamentMember, 
                    title_field='fullname', 
                    token_field='user_id', 
                    value_field = 'user_id' ), ),              
              listing = True 
            ),        
        dict( name="table_date", 
            label=_(u"Date"), 
            listing_column=day_column("table_date", 
                _(u"Date")), 
            listing=True, 
            edit_widget=SelectDateWidget, 
            add_widget=SelectDateWidget ),    
    ]

class ItemScheduleDescriptor(ModelDescriptor):
    display_name =_(u"Item scheduling")
    container_name =_(u"Item schedulings")

    fields = [
        dict( name="sitting_id", omit=True ),
        dict( name="schedule_id", omit=True ),
        dict( name="item_id", 
              property = schema.Choice(
                  title=_(u"Item"),
                  source=DatabaseSource(
                      domain.ParliamentaryItem,
                      token_field='parliamentary_item_id',
                      value_field = 'parliamentary_item_id',
                      title_getter=lambda obj: "%s - %s" % (type(obj).__name__, obj.short_name),

                      )
                  ),
              listing = False,
              ),        
        ]


