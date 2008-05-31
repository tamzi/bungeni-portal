
from ore.alchemist import Session
from ore.alchemist.model import ModelDescriptor
from ore.alchemist.vocabulary import DatabaseSource
from copy import deepcopy
from zope import schema, interface
from zc.table import column

#from z3c.form.browser import image

from bungeni.ui.datetimewidget import SelectDateWidget, SelectDateTimeWidget
from bungeni.ui import widget

from alchemist.ui import widgets
from bungeni.ui.login import check_email

import vocabulary
import domain
from i18n import _



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
        member = session.query( domain.ParliamentMember ).get( value )
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
     
     
####
#  Constraints / Invariants
#  

def ElectionAfterStart(obj):
    """ Start Date must be after Election Date"""        
    if obj.election_date >= obj.start_date:
        raise interface.Invalid(_("A parliament has to be elected before it can be sworn in"), "election_date", "start_date")
   
def EndAfterStart(obj):
    """ End Date must be after Start Date"""    
    if obj.end_date is None: return
    if obj.end_date <= obj.start_date:
        raise interface.Invalid(_("End Date must be after Start Date"), "start_date", "end_date")

def DissolutionAfterReinstatement( obj ):       
    """ A committee must be disolved before it can be reinstated """   
    if (obj.dissolution_date is None) or (obj.reinstatement_date is None): return
    if obj.dissolution_date > obj.reinstatement_date:
        raise interface.Invalid(_("A committee must be disolved before it can be reinstated"), "dissolution_date", "reinstatement_date" )

def ActiveAndSubstituted( obj ):
    """ A person cannot be active and substituted at the same time"""
    if obj.active_p and obj.replaced_id:
        raise interface.Invalid(_("A person cannot be active and substituted at the same time"), "active_p", "replaced_id")

def SubstitudedEndDate( obj ):
    """ If a person is substituted he must have an end date"""
    if not (obj.end_date) and obj.replaced_id:    
        raise interface.Invalid(_("If a person is substituted End Date must be set"), "replaced_id", "end_date")
        
def InactiveNoEndDate( obj ):
    """ If you set a person inactive you must provide an end date """
    if not obj.active_p:
        if not (obj.end_date):
            raise interface.Invalid(_("If a person is inactive End Date must be set"), "end_date", "active_p")
        
                
        

def DeathBeforeLife(User):
    """Check if date of death is after date of birth"""
    if User.date_of_death is None: return
    if User.date_of_death < User.date_of_birth:       
        raise interface.Invalid(_(u"One cannot die before being born"), "date_of_death", "date_of_birth")
    
def IsDeceased(User):
    """If a user is deceased a date of death must be given"""
    if User.active_p is None: 
        if User.date_of_death is None: 
            return
        else: 
            raise interface.Invalid(_(u"If a user is deceased he must have the status 'D'"), "date_of_death", "active_p" )
    if User.active_p == 'D':
        if User.date_of_death is None:
            raise interface.Invalid(_(u"A Date of Death must be given if a user is deceased"), "date_of_death", "active_p" )
    else:
        if User.date_of_death is not None:
            raise interface.Invalid(_(u"If a user is deceased he must have the status 'D'"), "date_of_death", "active_p" )
            
####
# Descriptors

class UserDescriptor( ModelDescriptor ):
    fields = [
        dict( name="user_id", omit=True),
        dict( name="titles", 
              label=_(u"Title(s)"), 
              description=_(u"Indicate any titles the person may hold")),
        dict( name="first_name", label=_(u"First Name"), listing=True),
        dict( name="last_name", label=_(u"Last Name"), listing=True),
        dict( name="middle_name", label=_(u"Middle Name")),
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
              property = schema.Choice( title=_(u"Gender"), values=['M', 'F'] ) ),
        dict( name="date_of_birth", 
              label=_(u"Date of Birth"), 
              edit_widget=SelectDateWidget, 
              add_widget=SelectDateWidget),
        dict( name="birth_country", 
              property = schema.Choice( title=_(u"Country of Birth"), 
                                        source=DatabaseSource(domain.Country, 'country_name',
                                                             'country_id' ),
                                        required=True )
            ),
        dict( name="date_of_death", label=_(u"Date of Death"),
              view_permission="bungeni.AdminUsers", 
              edit_permission="bungeni.AdminUsers",
              edit_widget=SelectDateWidget, add_widget=SelectDateWidget),
        dict( name="password", omit=True ),
        dict( name="description", 
              property=schema.Text(title=_(u"Description"), required=False),
              view_widget=widget.HTMLDisplay,
              edit_widget=widget.RichTextEditor, 
              add_widget=widget.RichTextEditor 
               ),
        dict( name="salt", omit=True),
        dict( name="active_p", label=_(u"Active"), 
              property = schema.Choice( title=_(u"Active"), values=['A', 'I', 'D'], default='A' ),
              view_permission="bungeni.AdminUsers", 
              edit_permission="bungeni.AdminUsers",  listing=True),
        dict( name="type", omit=True ),
        ]
        
    schema_invariants = [DeathBeforeLife, IsDeceased]




class MemberDescriptor( UserDescriptor ):

    fields = deepcopy( UserDescriptor.fields )
#    fields.extend([
#        dict( name='fullname', label=_(u"Fullname"),listing=True),
#        ])
#    fields.extend([
#        dict( name="member_id", omit=True ),
#        dict( name="elected_nominated", label=_("elected/nominated"), description=_("Is the MP (E)lected or (N)ominated")),
#        # this is only meant as a shortcut.. to the active parliament, else use group memberships 
#        # note that parliament_id = group_id      
#        dict( name="parliament_id",
#             property = schema.Choice( title=_(u"Parliament"), 
#                                       source=DatabaseSource(domain.Parliament, 'identifier', 'parliament_id' ),
#                                       required=True )
#              ), 
#        dict( name="constituency_id",
#             property = schema.Choice( title=_(u"Constituency"), 
#                                       source=DatabaseSource(domain.Constituency, 
#                                                             'constituency_identifier', 
#                                                             'constituency_id'),
#                                       required=True )
#              ),                
#        # these are again short cuts..
#        dict( name="start_date", label=_(u"Start Date"), listing=True),
#        dict( name="end_date", label=_(u"End Date"), listing=True ),
#        dict( name="leave_reason", label=_(u"Leave Reason")  ),
#        ])


        
class HansardReporterDescriptor( UserDescriptor ):
	
    fields = deepcopy( UserDescriptor.fields )	        

class GroupMembershipDescriptor( ModelDescriptor ):
   TitleSource= vocabulary.QuerySource(vocabulary.title_in_group, 
                                          token_field='user_role_name', 
                                          value_field='user_role_type_id', 
                                          filter_field='group_id', 
                                          filter_value= None, #'group_id', 
                                          order_by_field='user_role_name')   
#   SubstitutionSource = vocabulary.QuerySource(vocabulary.substitution_member,
#                                          token_field='fullname', 
#                                          value_field='membership_id', 
#                                          filter_field='group_id', 
#                                          filter_value= None, #'group_id', 
#                                          order_by_field='last_name')  
   SubstitutionSource = DatabaseSource(domain.ParliamentMember,  'fullname', 'user_id')                                          
   fields = [
#        dict( name="title", label=_(u"Title") ),
        dict( name="title", 
               property=schema.Choice( title=_(u"Title"),
                                       source=TitleSource),
                listing_column = lookup_fk_column( "title", _(u'<a href="?order_by=title">Title</a>'), domain.MemberTitle, 'user_role_name' ), 
                listing=True,                                      
           ),   
        dict( name="user_id",
              property=schema.Choice( title=_(u"Member of Parliament"), 
                                      source=DatabaseSource(domain.ParliamentMember,  'fullname', 'user_id')),
              listing_column=member_fk_column("user_id", _(u'<a href="?order_by=short_name">Member of Parliament</a>')), listing=True,
            ),                 
        dict( name="start_date", label=_(u"Start Date"), 
            listing_column=day_column("start_date", _(u'<a href="?order_by=start_date">Start Date</a>') ), listing=True,
            edit_widget=SelectDateWidget, add_widget=SelectDateWidget ),
        dict( name="end_date", label=_(u"End Date"), listing=True,
            listing_column=day_column("end_date", _(u'<a href="?order_by=end_date">End Date</a>')), 
            edit_widget=SelectDateWidget, add_widget=SelectDateWidget ),
        dict( name="active_p", label=_(u"Active"), view=False),
        dict( name="notes", label=_(u"Notes"), view_widget=widget.HTMLDisplay,
                                                edit_widget=widget.RichTextEditor,
                                                add_widget=widget.RichTextEditor
                                             ),
        dict( name="substitution_type", label=_(u"Type of Substitution"), add = False ),
        dict( name="replaced_id", 
                property=schema.Choice( title=_(u"Substituted by"), source=SubstitutionSource, required=False),
                add = False
                ),
# the Member that is selectable depends on the context (group she/he is in)          
#        dict( name="user_id",
#              property=schema.Choice( title=_(u"Member of Parliament"), 
#                                      source=DatabaseSource(domain.ParliamentMember,  'fullname', 'user_id')),
#              listing_column=member_fk_column("user_id", _(u"Member of Parliament") )
#            ),     
        dict( name="group_id", omit=True),
        dict( name="membership_id", omit=True),
        dict( name="status", omit=True )
        ]
        
   schema_invariants = [EndAfterStart,ActiveAndSubstituted,SubstitudedEndDate,InactiveNoEndDate]

class MpDescriptor ( ModelDescriptor ):
    display_name = _(u"Member of Parliament")
    fields = deepcopy(GroupMembershipDescriptor.fields)    
    constituencySource=DatabaseSource(domain.Constituency,  'name', 'constituency_id')
    #mpTypeSource= ['E', 'N', 'O']
    fields.extend([
        dict( name="constituency_id",
            property=schema.Choice( title=_(u"Constituency"), source=constituencySource,),
            listing_column=vocab_column( "constituency_id" , _(u'<a href="?order_by=constituency">Constituency</a>'), constituencySource, ),
            listing=True),   
        dict( name="elected_nominated", 
            property=schema.Choice( title=_(u"elected/nominated"), values=['E', 'N', 'O']), listing=True,
            #u'<a href="?order_by=elected_nominated">elected/nominated</a>'
            ),
        dict( name="leave_reason", label=_("Leave Reason")),     
    ])
    schema_invariants = [EndAfterStart, ActiveAndSubstituted, SubstitudedEndDate, InactiveNoEndDate]
    
class PartyMemberDescriptor( ModelDescriptor ):
    display_name=_(u"Party Member")
    fields = deepcopy(GroupMembershipDescriptor.fields)
    #fields.extend([
    #     dict( name="user_id",
    #          property=schema.Choice( title=_(u"Person"), 
    #                                  source=DatabaseSource(domain.ParliamentMember,  'fullname', 'user_id')),
    #          listing_column=member_fk_column("user_id", _(u"Person")), listing=True,
    #        ),
    #        ])

class ExtensionMemberDescriptor( ModelDescriptor ):
    display_name =_(u"Additional members")
    fields = deepcopy(GroupMembershipDescriptor.fields)
    #fields.extend([
    #     dict( name="user_id",
    #          property=schema.Choice( title=_(u"Person"), 
    #                                  source=DatabaseSource(domain.ParliamentMember,  'fullname', 'user_id')),
    #          listing_column=member_fk_column("user_id", _(u"Person") ),
    #          listing=True,),
    #       ])


class GroupDescriptor( ModelDescriptor ):

    fields = [
        dict( name="group_id", omit=True ),
        dict( name="type", omit=True ),
        dict( name="short_name", label=_(U"Name"), listing=True,
              listing_column=name_column("short_name", _(u'<a href="?order_by=short_name">Name</a>'))),
        dict( name="full_name", label=_(u"Full Name"), listing=True,
              listing_column=name_column("full_name", _(u'<a href="?order_by=full_name">Full Name</a>'))),
        dict( name="description", property=schema.Text(title=_(u"Description") , required=False ),
              view_widget=widget.HTMLDisplay,
              edit_widget=widget.RichTextEditor,
              add_widget=widget.RichTextEditor),
        dict( name="start_date", label=_(u"Start Date"), listing=True, 
              listing_column=day_column("start_date", _(u'<a href="?order_by=start_date">Start Date</a>')), edit_widget=SelectDateWidget, add_widget=SelectDateWidget),
        dict( name="end_date", label=_(u"End Date"), listing=True, 
              listing_column=day_column('end_date', _(u'<a href="?order_by=end_date">End Date</a>')), edit_widget=SelectDateWidget, add_widget=SelectDateWidget),        
        #dict( name="status",  label=_(u"Status"), edit=False, add=False, listing=True )        
        dict( name="status", omit=True),
        ]

    schema_invariants = [EndAfterStart]
                        
class ParliamentDescriptor( GroupDescriptor ):
    display_name = _(u"Parliament")    
    fields = [
        dict( name="group_id", omit=True ),
        dict( name="parliament_id", omit=True ),
        dict( name="short_name", label=_(u"Parliament Identifier"), 
              description=_(u"Unique identifier of each Parliament (e.g. nth Parliament)"), 
              listing=True ),
        dict( name="full_name", label=_(u"Name"), 
              description=_(u"Parliament name"), 
              listing=True,
              listing_column=name_column("full_name", "Name") ),
        dict( name="description", 
              property=schema.Text(title=_(u"Description"), required=False),
              view_widget=widget.HTMLDisplay,
              edit_widget=widget.RichTextEditor, 
              add_widget=widget.RichTextEditor 
               ),
        dict( name="election_date",
              label=_(u"Election Date"), 
              description=_(u"Date the of the election"),
              edit_widget=SelectDateWidget, 
              add_widget=SelectDateWidget 
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
    fields = deepcopy( GroupDescriptor.fields )
    typeSource = DatabaseSource(domain.CommitteeType, 'committee_type', 'committee_type_id')
    fields.extend([
        dict( name='parliament_id', omit=True ),
        dict( name='committee_id', omit=True ),
        dict( name = 'committee_type_id',
                property=schema.Choice( title=_(u"Type of committee"), 
                    source=typeSource),
                listing_column=vocab_column( "committee_type_id" , _(u"Type"), typeSource, ), listing=True,
            
            ),
        dict( name='no_members', label=_(u"Number of members"), description=_(u"") ),
        dict( name='min_no_members', label =_(u"Minimum Number of Members")),
        dict( name='quorum', label=_(u"Quorum")),
        dict( name='no_clerks', label=_(u"Number of clerks")),
        dict( name='no_researchers', label=_(u"Number of researchers")),
        dict( name='proportional_representation', label=_(u"Proportional reprensentation")),
        dict( name='researcher_required', label=_(u"Researcher required")),
        dict( name='default_chairperson', label=_(u"Default chairperson")),
        dict( name='default_position', label=_(u"Default Position")),
        dict( name='dissolution_date', label=_(u"Dissolution date"), edit_widget=SelectDateWidget, add_widget=SelectDateWidget ),
        dict( name='reinstatement_date', label=_(u"Reinstatement Date"), edit_widget=SelectDateWidget, add_widget=SelectDateWidget ),              
    ])
    schema_invariants = [EndAfterStart, DissolutionAfterReinstatement]
    
class CommitteeMemberDescriptor( ModelDescriptor ):
    display_name = _(u"Committee Members")
    fields = deepcopy(GroupMembershipDescriptor.fields)
#    membersVocab = vocabulary.QuerySource(vocabulary.mp_committees, 
#                                          token_field='fullname', 
#                                          value_field='user_id', 
#                                          filter_field='committee_id', 
#                                          filter_value= None, #'group_id', 
#                                          order_by_field='last_name',
#                                          title_field='fullname' )  
#    membersVocab = DatabaseSource(domain.ParliamentMember,  'fullname', 'user_id')                                                 
#    fields.extend([
#            dict( name="user_id", listing=True,
#                property = schema.Choice(title=_(u"Committee member"), source=membersVocab, ),
#                listing_column=member_fk_column("user_id", _(u"Committee Member") ) ),
#    ])   
    
    schema_invariants = [EndAfterStart, ActiveAndSubstituted, SubstitudedEndDate, InactiveNoEndDate]
     
        
class PoliticalPartyDescriptor( GroupDescriptor ):
    display_name = _(u"Political Party")     
    fields = deepcopy( GroupDescriptor.fields )    
    fields.extend([
        dict( name='logo', label=_(u"Logo"),  )
     ])
#        view_widget=image.ImageWidget,
#        add_widget=image.ImageWidget,
#        edit_widget=image.ImageWidget

     
    schema_invariants = [EndAfterStart]
    
class ExtensionGroupDescriptor( GroupDescriptor ):
    display_name = _(u"Group extensions")
    fields = deepcopy( GroupDescriptor.fields )    
    fields.extend([
        dict(name="group_type", listing=True,
            property = schema.Choice(title=_(u"Extension for"), values=['ministry', 'committee',])
            ),
        dict(name="extension_type_id", omit=True),  
        dict(name="parliament_id", omit=True),           
    ])   
     
class MinistryDescriptor( GroupDescriptor ):
    display_name = _(u"Ministry")
    fields = deepcopy( GroupDescriptor.fields )       
    fields.extend([
        dict( name='ministry_id', omit=True ),
        dict( name='government_id', omit=True ),
                   
    ])
    
    schema_invariants = [EndAfterStart]
    
class MinisterDescriptor( ModelDescriptor ):    
    display_name = _(u"Minister")
    fields = deepcopy(GroupMembershipDescriptor.fields)
   # membersVocab = vocabulary.QuerySource(vocabulary.mp_ministers, 
   #                                       token_field='fullname', 
   #                                       value_field='user_id', 
   #                                       filter_field='ministry_id', 
   #                                       filter_value=None, 
   #                                       order_by_field='last_name',
   #                                       title_field='fullname' ) 
#    membersVocab = DatabaseSource(domain.ParliamentMember,  'fullname', 'user_id')                                               
#    fields.extend([
#            dict( name="user_id", listing=True,
#                property = schema.Choice(title=_(u"Minister"), source=membersVocab, ),
#                listing_column=member_fk_column("user_id", _(u"Minister") ) ),
#    ])   
    
    schema_invariants = [ActiveAndSubstituted,SubstitudedEndDate,InactiveNoEndDate]
    
class ParliamentSession( ModelDescriptor ):
    display_name = _(u"Parliamentary Session")    
    fields = deepcopy( GroupDescriptor.fields )
    fields.extend([
        dict( name="session_id", omit=True ),
        dict( name="start_date", label=_(u"Start Date"), 
            listing_column=day_column("start_date", _(u'<a href="?order_by=start_date">Start Date</a>')), 
            edit_widget=SelectDateWidget, add_widget=SelectDateWidget),
        dict( name="end_date", label=_(u"End Date"), 
            listing_column=day_column('end_date', _(u'<a href="?order_by=end_date">End Date</a>')),
            edit_widget=SelectDateWidget, add_widget=SelectDateWidget),                
        dict( name="notes", property=schema.Text(title=_(u"Notes"), required=False ),
              view_widget=widget.HTMLDisplay,
              edit_widget=widget.RichTextEditor,
              add_widget=widget.RichTextEditor )
        ])
        
    schema_invariants = [EndAfterStart]        
        
class GovernmentDescriptor( ModelDescriptor ):
    
    display_name = _(u"Government")
    fields = [
        dict( name="group_id", omit=True ),
        dict( name="short_name", label=_(u"Name"), description=_(u"Name of the Head of Government"), listing=True),
        dict( name="full_name", label=_(u"Number")),       
        dict( name="start_date", label=_(u"In power from"), listing=True, 
              listing_column=day_column("start_date", _(u"In power from")), edit_widget=SelectDateWidget, add_widget=SelectDateWidget ),
        dict( name="end_date", label=_(u"In power till"), listing=True,
              listing_column=day_column("end_date", _(u"In power till")), edit_widget=SelectDateWidget, add_widget=SelectDateWidget ),
        dict( name="description", property=schema.Text(title=_(u"Notes") , required=False),
                view_widget=widget.HTMLDisplay,
                edit_widget=widget.RichTextEditor,
                add_widget=widget.RichTextEditor
            ),
        dict( name="status", omit=True), # label=_(u"Status"), edit=False, add=False, listing=True ),
        dict( name="government_id", omit=True), 
        dict( name="parliament_id", omit=True),   
        dict( name="type", omit=True ),  
        ]
    
    schema_invariants = [EndAfterStart]    
    
class MotionDescriptor( ModelDescriptor ):
    
    display_name = _(u"Motion")
    
    fields = [
        dict( name="motion_id", omit=True ),
        dict( name="title", label=_(u"Subject"), listing=True,
              edit_widget = widgets.LongTextWidget),
        dict( name="session_id", 
              property = schema.Choice( title=_(u"Session"), source=DatabaseSource(domain.ParliamentSession, 'session_id', 'session_id', 'short_name'), 
              required=False )
              ),
        dict( name="submission_date", label=_(u"Submission Date"), listing=True ,  edit_widget=SelectDateWidget, add_widget=SelectDateWidget),
        dict( name="received_date", label=_(u"Received Date"),  edit_widget=SelectDateWidget, add_widget=SelectDateWidget),
        dict( name="notice_date", label=_(u"Notice Date"), listing=True, edit_widget=SelectDateWidget, add_widget=SelectDateWidget),        
#        dict( name="type", label=_(u"Public"),
#              edit_widget = widgets.YesNoInputWidget,
#              view_widget = widgets.YesNoDisplayWidget),
        dict( name="identifier", label=_(u"Identifier")),
        #XXX get the members of the current (same value as the motion) parliament only!
#        dict( name="owner_id",
#              property = schema.Choice( title=_(u"Owner"), source=DatabaseSource(domain.ParliamentMember, 'last_name', 'user_id' ), required=False )
#              ),
        dict( name="body_text", label=_(u"Motion Text"),
              property = schema.Text( title=u"Motion" ),
              view_widget=widget.HTMLDisplay,
              edit_widget=widget.RichTextEditor, 
              add_widget=widget.RichTextEditor
              ),
        # TODO omit for now
        dict( name="entered_by", label=_(u"Entered By"), omit=True ), 
        dict( name="party_id",
            property = schema.Choice( title=_(u"Political Party"), 
                                      source=DatabaseSource(domain.PoliticalParty, 'short_name', 'party_id' ), 
                                      required=False) ),
        dict( name="status", label=_(u"Status"), edit=False, add=False, listing=True ),
        #XXX Hack for Cairo
        dict( name="sitting_id", 
              property = schema.Choice( title=_(u"Sitting"), source=DatabaseSource(domain.GroupSitting, 'sitting_id', 'sitting_id', 'short_name'), 
              required=False )
              ),
        ]


class MotionAmendmentDescriptor( ModelDescriptor ):
    
    display_name = _(u"Motion Amendment")
    fields = [
        dict( name="amendment_id", omit=True ),
        dict( name="motion_id", omit=True ),
        dict( name="amended_id", omit=True ),
        dict( name="title", label=_(u"Subject"), listing=True,
              edit_widget = widgets.LongTextWidget),
        dict( name="body_text", label=_(u"Motion Amendment Text"),
              property = schema.Text( title=u"Motion Amendment" ),
              view_widget=widget.HTMLDisplay,
              edit_widget=widget.RichTextEditor, 
              add_widget=widget.RichTextEditor
              ),
        dict( name="submission_date", label=_(u"Submission Date"),  edit_widget=SelectDateWidget, add_widget=SelectDateWidget),
        dict( name="vote_date", label=_(u"Vote Date"),  edit_widget=SelectDateWidget, add_widget=SelectDateWidget),
        dict( name="accepted_p",  label=_(u"Accepted")),
        ]
class SittingDescriptor( ModelDescriptor ):
    
    display_name = _(u"Sittings")
    
    fields = [
        dict( name="sitting_id", omit=True ),
        dict( name="group_id", omit=True ),
        dict( name="session_id", omit=True ),
        dict( name="start_date", label=_(u"Start Date"),  
            listing_column=day_column("start_date", _(u'<a href="?order_by=start_date">Start Date</a>')),
            edit_widget=SelectDateTimeWidget, add_widget=SelectDateTimeWidget),
        dict( name="end_date", label=_(u"End Date"),  
            listing_column=day_column("end_date", _(u'<a href="?order_by=end_date">End Date</a>')),
            edit_widget=SelectDateTimeWidget, add_widget=SelectDateTimeWidget),
        dict( name="sitting_type", 
              listing_column = vocab_column( "sitting_type", _(u"Sitting Type"), vocabulary.SittingTypes ),
              property = schema.Choice( title=_(u"Sitting Type"), 
                                        source=vocabulary.SittingTypes,
                                        required=False) ),
        ]

    schema_invariants = [EndAfterStart]
    
class SessionDescriptor( ModelDescriptor ):
    
    display_name = _(u"Parliamentary Session")
    
    fields = [
        dict( name="session_id", omit=True),
        dict( name="parliament_id", omit=True),
        dict( name="short_name", label=_(u"Short Name"), listing=True ),
        dict( name="full_name", label=_(u"Full Name") ),
        dict( name="start_date", label=_(u"Start Date"), listing=True, 
            listing_column=day_column("start_date", _(u'<a href="?order_by=start_date">Start Date</a>')),
            edit_widget=SelectDateWidget, add_widget=SelectDateWidget),
        dict( name="end_date", label=_(u"End Date"), listing=True, 
            listing_column=day_column("end_date", _(u'<a href="?order_by=end_date">End Date</a>')),
            edit_widget=SelectDateWidget, add_widget=SelectDateWidget),
        dict( name="notes", label=_(u"Notes"), required=False)
        ]
    schema_invariants = [EndAfterStart]
            
class DebateDescriptor ( ModelDescriptor ):
    display_name = _(u"Debates")
    fields = [
        dict( name="sitting_id", omit=True ), 
        dict( name="debate_id", omit=True ),                
        dict( name="short_name", label=_(u"Short Name"), listing=True,
              listing_column=name_column("short_name", _(u'<a href="?order_by=short_name">Name</a>')) ), 
        dict( name="body_text", label=_(u"Transcript"),
              property = schema.Text( title=u"Transcript" ),
              view_widget=widget.HTMLDisplay,
              edit_widget=widget.RichTextEditor, 
              add_widget=widget.RichTextEditor
              ),   
        ]             
        
class AttendanceDescriptor( ModelDescriptor ):
    display_name =_(u"Sitting Attendance")
    attendanceVocab = DatabaseSource(domain.AttendanceType, 'attendance_type', 'attendance_id' )
#    membersVocab = vocabulary.QuerySource(vocabulary.mps_sitting, 
#                                          token_field='fullname', 
#                                          value_field='user_id', 
#                                          filter_field='sitting_id', 
#                                          filter_value=None, 
#                                          order_by_field='last_name',
#                                          title_field='fullname' )      
    
    sql_members ='''SELECT "users"."titles" || ' ' || "users"."first_name" || ' ' || "users"."middle_name" || ' ' || "users"."last_name" as user_name, 
                      "users"."user_id" 
                       FROM  "public"."users" 
                       WHERE  "users"."user_id" = %(member_id)s                                                                  
                    '''
    membersVocab = vocabulary.SQLQuerySource( sql_members, 'user_name', 'user_id', {'member_id':'$member_id'} )                                                                        
    fields = [
        dict( name="sitting_id", omit=True ),
        dict( name="member_id", listing=True,
                property = schema.Choice(title=_(u"Attendance"), source=membersVocab, ),
              listing_column=member_fk_column("member_id", _(u'<a href="?order_by=short_name">Member of Parliament</a>') ) ),
        dict( name="attendance_id", listing=True, 
                property = schema.Choice( title=_(u"Attendance"), source=attendanceVocab, required=True),
                listing_column = vocab_column("attendance_id", _(u'<a href="?order_by=attendance_id">Attendance</a>'), attendanceVocab )),            
        ]
        
class AttendanceTypeDescriptor( ModelDescriptor ):        
    display_name =_(u"Sitting Attendance")
    
    fields = [
        dict (name="attendance_id", omit=True ),
        dict (name="attendance_type", label=_(u"Attendance type") ),
        ]
        
class BillDescriptor( ModelDescriptor ):
    
    display_name = _(u"Bill")
    
    fields = [
        dict( name="bill_id", omit=True ),
        dict( name="title", label=_(u"Title"), listing=True ),
        dict( name="preamble", label=_(u"Preamble"), 
                view_widget=widget.HTMLDisplay,
                edit_widget=widget.RichTextEditor, 
                add_widget=widget.RichTextEditor),
        dict( name="body_text", label=_(u"Text"), 
                view_widget=widget.HTMLDisplay,
                edit_widget=widget.RichTextEditor, 
                add_widget=widget.RichTextEditor),                
        dict( name="session_id", label=_(u"Session") ),
        dict( name="identifier", label=_(u"Identifer") ),
        dict( name="submission_date", label=_(u"Submission Date"), listing=True,  
              edit_widget=SelectDateWidget, add_widget=SelectDateWidget,
              listing_column=day_column("submission_date", _(u"Submission Date")) ),
        dict( name="publication_date", label=_(u"Publication Date"),  edit_widget=SelectDateWidget, add_widget=SelectDateWidget ),        
        dict( name="status", label=_(u"Status"), edit=False, add=False, listing=True ),
         #XXX Hack for Cairo
        dict( name="sitting_id", 
              property = schema.Choice( title=_(u"Sitting"), source=DatabaseSource(domain.GroupSitting, 'sitting_id', 'sitting_id', 'short_name'), 
              required=False )
              ),        
        ]

class QuestionDescriptor( ModelDescriptor ):

    display_name = _(u"Question")
    
    fields = [
        dict( name="question_id", omit=True),
#        dict( name="session_id", 
#                property = schema.Choice( title=_(u"Session"), source=DatabaseSource(domain.ParliamentSession,'short_name' ,'session_id'), required=False )
#            ),
        dict( name="clerk_submission_date", label=_(u"Submission Date"), listing=True, omit=True ),
        dict( name="question_type", listing=True, 
              property=schema.Choice( title=_(u"Question Type"), 
                                      description=_("(O)rdinary or (P)rivate Notice"), 
                                      vocabulary=vocabulary.QuestionType) ),
        dict( name="response_type",  listing=True,
             property=schema.Choice( title=_(u"Response Type"), 
                                      description=_("(O)ral or (W)ritten"), 
                                      vocabulary=vocabulary.ResponseType),
        
             ),
        dict( name="owner_id", 
              property = schema.Choice( title=_(u"Owner"), source=DatabaseSource(domain.ParliamentMember, 'fullname', 'user_id' )), 
            ),
        dict( name="subject", label=_(u"Subject"), description=_(u"Subject of the Question"), edit_widget = widgets.LongTextWidget ),
        dict( name="question_text", property=schema.Text(title=_(u"Question"), required=True ),
              view_widget=widget.HTMLDisplay,
              edit_widget=widget.RichTextEditor, 
              add_widget=widget.RichTextEditor
        
            ),
        #label=_("Question"), description=_(u"The Question submitted")),        
        dict( name="status", label=_(u"Status"), modes="listing"),
        dict( name="supplement_parent_id", omit=True), #XXX
        #dict( name="sitting_id", omit=True), #XXX
         #XXX Hack for Cairo
        dict( name="sitting_id", 
              property = schema.Choice( title=_(u"Sitting"), source=DatabaseSource(domain.GroupSitting, 'sitting_id', 'sitting_id', 'short_name'), 
              required=False )
              ),
        dict( name="sitting_time", label=_(u"Sitting Time"), listing=True ),
        dict( name="receive_notification", label=_(u"Receive notification"), description=_(u"Select this option to receive notifications for this question."), listing=True ),
        ]
        
class ResponseDescriptor( ModelDescriptor ):
    display_name = _(u"Response")
    
    fields = [
        dict( name="response_id", omit=True ),
        dict( name="question_id", omit=True ), #XXX
        dict( name="response_text", label=_(u"Response"), description=_(u"Response to the Question"),
              view_widget=widget.HTMLDisplay,
              edit_widget=widget.RichTextEditor, 
              add_widget=widget.RichTextEditor ),
        dict( name="response_type", label=_(u"Response Kind"), description=_(u"(I)nitial or (S)ubsequent Response"), listing=True ),		
        dict( name="sitting_id", omit=True ), #XXX
        dict( name="sitting_time", label=_(u"Sitting Time"), description=_(u"Time of the Sitting"), listing=True ),
        ]        

class ConstituencyDescriptor( ModelDescriptor ):
    provinceSource=DatabaseSource(domain.Province,'province', 'province_id')
    regionSource=DatabaseSource(domain.Region,'region', 'region_id')
    fields = [
        dict( name="constituency_id", omit=True ),
        dict( name="name", label=_(u"Name"), description=_("Name of the constituency"), listing=True ),
        dict(name="province",
            property = schema.Choice( title=_(u"Province"), source=provinceSource,            
            required=True ),
            listing_column = vocab_column("province", _(u"Province"), provinceSource ), listing=True,
            ),
        dict( name="region", label=_(u"Region"),
             property = schema.Choice( title=_(u"Region"), source=regionSource,              
             required=True ),
             listing_column = vocab_column("region", _(u"Region"), regionSource), listing=True,
            ),
        dict( name="start_date", label=_(u"Start Date"), 
                listing=True, listing_column=day_column('start_date', _(u"Start Date")), 
                edit_widget=SelectDateWidget, add_widget=SelectDateWidget),
        dict( name="end_date", label=_(u"End Date"), 
                listing=True , listing_column=day_column('end_date', _(u"End Date")), 
                edit_widget=SelectDateWidget, add_widget=SelectDateWidget),        
        ]

schema_invariants = [EndAfterStart]
        
class ProvinceDescriptor( ModelDescriptor ):
    fields = [
        dict( name="province_id", omit=True ),
        dict( name="province", label=_(u"Province"), description=_(u"Name of the Province"), listing=True ),
        ]
        
class RegionDescriptor( ModelDescriptor ):
    fields = [
        dict( name="region_id", omit=True ),
        dict( name="region", label=_(u"Region"), description=_(u"Name of the Region"), listing=True ), 
        ]

class CountryDescriptor( ModelDescriptor ):
    fields = [
        dict( name="country_id", label=_(u"Country Code") , description =_(u"ISO Code of the  country")),
        dict( name="country_name", label=_(u"Country"), description=_(u"Name of the Country"), listing=True ), 
        ]        
		
class ConstituencyDetailDescriptor( ModelDescriptor ):
    fields = [
        dict( name="constituency_detail_id", omit=True ),
        dict( name="constituency_id", label=_(u"Name"), description=_("Name of the constituency"), listing=False, omit=True ), #XXX
        dict( name="date", label=_(u"Date"), description=_(u"Date the data was submitted from the Constituency"), 
            listing=True,  listing_column=day_column("date", "Date"),
                edit_widget=SelectDateWidget, add_widget=SelectDateWidget),
        dict( name="population", label=_(u"Population"), description=_(u"Total Number of People living in this Constituency"), listing=True ),                
        dict( name="voters", label=_(u"Voters"), description=_(u"Number of Voters registered in this Constituency"), listing=True ),
        ]
        
        
        		
################
# Hansard
################
class RotaDescriptor( ModelDescriptor ):
    fields = [
        dict( name="rota_id", omit=True ),         
        dict( name="reporter_id", omit=True), #XXX
        #    property = schema.Choice( title=_(u"Hansard Reporter"), source=vocabulary.ParliamentMembers, required=True ) #XXX
        #    ),
        dict( name="identifier", title=_("Rota Identifier"), listing=True),
        dict( name="start_date", label=_(u"Start Date"), listing_column=day_column("start_date", _(u"Start Date") ), listing=True , edit_widget=SelectDateWidget, add_widget=SelectDateWidget),
        dict( name="end_date", label=_(u"End Date"), listing_column=day_column("end_date", _(u"End Date")), listing=True, edit_widget=SelectDateWidget, add_widget=SelectDateWidget ),
        ]

    schema_invariants = [EndAfterStart]
        
#class TakeDescriptor( ModelDescriptor ):
#    fields = [        
#        dict( name="take_id", omit=True ),
#        dict( name="rota_id", 
#              property = schema.Choice( title=_(u"Rota"), source=vocabulary.Rota, required=True )
#            ),
#        dict( name="identifier", title=_(u"Take Identifier"), listing=True ),
#        ]
        
# take_media

#class TranscriptIdentifier( ModelDescriptor ):
 
 
 
