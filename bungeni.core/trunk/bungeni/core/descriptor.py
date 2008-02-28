from ore.alchemist.model import ModelDescriptor
from ore.alchemist.vocabulary import DatabaseSource
from copy import deepcopy
from zope import schema
import vocabulary
import domain
from alchemist.ui import widgets

from i18n import _

class UserDescriptor( ModelDescriptor ):
    fields = [
        dict( name="user_id", omit=True),
        dict( name="titles", label=_(u"Title(s)"), description=_(u"Indicate any titles the person may hold")),
        dict( name="first_name", label=_(u"First Name"), listing=True),
        dict( name="last_name", label=_(u"Last Name"), listing=True),
        dict( name="middle_name", label=_(u"Middle Name")),
        dict( name="email", label=_(u"Email")),
        dict( name="login", label=_(u"Login Name")),
        dict( name="national_id", label=_(u"National Id")),
        dict( name="gender", label=_(u"Gender")),
        dict( name="date_of_birth", label=_(u"Date of Birth")),
        dict( name="birth_country", label=_(u"Country of Birth"), description =_(u"ISO Code of the  country")),
#        dict( name="birth_country", 
#            property = schema.Choice( title=_(u"Country of Birth"), 
#                                       source=DatabaseSource(domain.Country, 'country_name', 'country_id' ),
#                                       required=True )
#            ),
        dict( name="date_of_death", label=_(u"Date of Death"), view_permission="bungeni.AdminUsers", edit_permission="bungeni.AdminUsers"),
        dict( name="password", omit=True ),
        dict( name="salt", omit=True),
        dict( name="active_p", label=_(u"Active"), view_permission="bungeni.AdminUsers", edit_permission="bungeni.AdminUsers"),
        dict( name="type", omit=True ),
        ]

class MemberDescriptor( UserDescriptor ):

    fields = deepcopy( UserDescriptor.fields )
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

   fields = [
        dict( name="title", label=_(u"Title") ),
        dict( name="start_date", label=_(u"Start Date") ),
        dict( name="end_date", label=_(u"End Date") ),
        dict( name="active_p", label=_(u"Active") ),
        dict( name="notes", label=_(u"Notes") ),
        dict( name="substitution_p", label=_(u"Substituted") ),
        dict( name="substitution_type", label=_(u"Type of Substitution") ),
        dict( name="replaced_id", omit=True),
        dict( name="user_id", omit=True),
        dict( name="group_id", omit=True),
        dict( name="status", omit=True )
        ]

class MpDescriptor ( ModelDescriptor ):
    fields = deepcopy(GroupMembershipDescriptor.fields)
    fields.extend([
        dict( name="constituency_id", 
            property=schema.Choice( title=_(u"Constituency"), source=DatabaseSource(domain.Constituency, 'constituency_id', 'name'))
            ),        
        dict( name="elected_nominated", label=_(u"elected/nominated")),
        #dict( name="start_date", label=_(u"Start Date"), listing=True ),
        #dict( name="end_date", label=_(u"End Date"), listing=True ), 
        dict( name="leave_reason", label=_("Leave Reason")),     
    ])

        
class GroupDescriptor( ModelDescriptor ):

    fields = [
        dict( name="group_id", omit=True ),
        dict( name="short_name", label=_(u"Name"), listing=True),
        dict( name="full_name", label=_(u"Full Name")),
        dict( name="description", property=schema.Text(title=_(u"Description"))),
        dict( name="start_date", label=_(u"Start Date"), listing=True ),
        dict( name="end_date", label=_(u"End Date"), listing=True ),        
        dict( name="status", label=_(u"Status"), edit=False, add=False, listing=True )        
        ]
                    
class ParliamentDescriptor( GroupDescriptor ):
    
    fields = [
        dict( name="group_id", omit=True ),
        dict( name="parliament_id", omit=True ),
        dict( name="short_name", label=_(u"Parliament Identifier"), description=_(u"Unique identifier of each Parliament (e.g. nth Parliament)"), listing=True ),
        dict( name="full_name", label=_(u"Name"), description=_(u"Parliament name"), listing=True ),
        dict( name="description", property=schema.Text(title=_(u"Description"), required=False )),
        #dict( name="identifier", label=_(u"Parliament Number"), listing=True ),
        dict( name="election_date", label=_(u"Election Date"), description=_(u"Date the of the election") ),        
        dict( name="start_date", label=_(u"In power from"),  description=_(u"Date the of the swearing in") ),
        dict( name="end_date", label=_(u"In power till"),  description=_(u"Date the of the dissolution") ),
        ]
        
class CommitteeDescriptor( GroupDescriptor ):
    
    fields = deepcopy( GroupDescriptor.fields )
    fields.extend([
        #dict( name='parliament_id', 
        #    property=schema.Choice( title=_(u"Parliament"), source=DatabaseSource(domain.Parliament,"short_name", "parliament_id")),
        #    ),
        dict( name='parliament_id', omit=True ),
        dict( name = 'committee_type_id',
            property=schema.Choice( title=_(u"Type of committee"), source=DatabaseSource(domain.CommitteeType, 'committee_type', 'committee_type_id')),
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
        dict( name='dissolution_date', label=_(u"Dissolution date")),
        dict( name='reinstatement_date', label=_(u"Reinstatement Date")),              
    ])
    
class PolitcalPartyDescriptor( GroupDescriptor ):
     
    fields = deepcopy( GroupDescriptor.fields )    
    fields.extend([
        dict( name='logo', label=_(u"Logo"))
     ])
     
class MinistryDescriptor( GroupDescriptor ):

    fields = deepcopy( GroupDescriptor.fields )       
    fields.extend([
        dict( name='ministry_id', omit=True ),
        dict( name='government_id', omit=True ),           
    ])
    
class ParliamentSession( ModelDescriptor ):
    
    fields = deepcopy( GroupDescriptor.fields )
    fields.extend([
        dict( name="session_id", omit=True ),
        dict( name="start_date", label=_(u"Start Date")),
        dict( name="end_date", label=_(u"End Date")),                
        dict( name="notes", property=schema.Text(title=_(u"Notes")))
        ])
        
class GovernmentDescriptor( ModelDescriptor ):
    
    display_name = _(u"Government")
    #fields = deepcopy( GroupDescriptor.fields )    
    #fields.extend([
    #    dict( name="government_id", omit=True),
    #    dict( name="start_gazetted_date", label=_(u"Gazetted Start Date") ),
    #    dict( name="end_gazetted_date", label=_(u"Gazetted End Date") )
    #    ])
    fields = [
        dict( name="group_id", omit=True ),
        dict( name="short_name", label=_(u"Name"), description=_(u"Name of the Head of Government"), listing=True),
        dict( name="full_name", label=_(u"Number")),       
        dict( name="start_date", label=_(u"In power from"), listing=True ),
        dict( name="end_date", label=_(u"In power till"), listing=True ),        
        dict( name="description", property=schema.Text(title=_(u"Notes"))),
        dict( name="status", label=_(u"Status"), edit=False, add=False, listing=True ),
        dict( name="government_id", omit=True),     
        ]
    
    
class MotionDescriptor( ModelDescriptor ):
    
    display_name = _(u"Motion")
    
    fields = [
        dict( name="motion_id", omit=True ),
        dict( name="title", label=_(u"Subject"), listing=True,
              edit_widget = widgets.LongTextWidget),
        dict( name="session_id", 
              property = schema.Choice( title=_(u"Session"), source=DatabaseSource(domain.ParliamentSession, 'short_name', 'session_id'), 
              required=False )
              ),
        dict( name="submission_date", label=_(u"Submission Date"), listing=True ),
        dict( name="received_date", label=_(u"Received Date")),
        dict( name="notice_date", label=_(u"Notice Date"), listing=True),        
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
              ),
        # TODO omit for now
        dict( name="entered_by", label=_(u"Entered By"), omit=True ), 
        dict( name="party_id",
            property = schema.Choice( title=_(u"Political Party"), 
                                      source=DatabaseSource(domain.PoliticalParty, 'full_name', 'party_id' ), 
                                      required=False) ),
        dict( name="status", label=_(u"Status"), edit=False, add=False, listing=True )
        ]

class SittingDescriptor( ModelDescriptor ):
    
    display_name = _(u"Parliamentary Sitting")
    
    fields = [
        dict( name="sitting_id", omit=True ),
        dict( name="group_id", omit=True ),
        dict( name="session_id", omit=True ),
        dict( name="start_date", label=_(u"Start Date") ),
        dict( name="end_date", label=_(u"End Date") ),
        ]

class SessionDescriptor( ModelDescriptor ):
    
    display_name = _(u"Parliamentary Session")
    
    fields = [
        dict( name="session_id", omit=True),
        dict( name="parliament_id", omit=True),
        dict( name="short_name", label=_(u"Short Name"), listing=True ),
        dict( name="full_name", label=_(u"Full Name") ),
        dict( name="start_date", label=_(u"Start Date"), listing=True ),
        dict( name="end_date", label=_(u"End Date"), listing=True ),
        dict( name="notes", label=_(u"Notes") )
        ]
        
class BillDescriptor( ModelDescriptor ):
    
    display_name = _(u"Bill")
    
    fields = [
        dict( name="bill_id", omit=True ),
        dict( name="title", label=_(u"Title"), listing=True ),
        dict( name="preamble", label=_(u"Preamble")),
        dict( name="session_id", label=_(u"Session") ),
        dict( name="identifier", label=_(u"Identifer") ),
        dict( name="submission_date", label=_(u"Submission Date"), listing=True ),
        dict( name="publication_date", label=_(u"Publication Date") ),        
        dict( name="status", label=_(u"Status"), edit=False, add=False, listing=True )        
        ]

class QuestionDescriptor( ModelDescriptor ):

    display_name = _(u"Question")
    
    fields = [
        dict( name="question_id", omit=True),
        dict( name="session_id", 
                property = schema.Choice( title=_(u"Session"), source=DatabaseSource(domain.ParliamentSession,'short_name' ,'session_id'), required=False )
            ),
        dict( name="clerk_submission_date", label=_(u"Submission Date"), listing=True, omit=True ),
        dict( name="question_type", listing=True, 
              property=schema.Choice( title=_(u"Question Type"), 
                                      description=_("(O)rdinary or (P)rivate Notice"), 
                                      vocabulary=vocabulary.QuestionType) ),
        dict( name="response_type", label=_(u"Response Type"), description=_("(O)ral or (W)ritten"), listing=True ),
        dict( name="owner_id", 
              property = schema.Choice( title=_(u"Owner"), source=DatabaseSource(domain.ParliamentMember, 'last_name', 'user_id' )), 
            ),
        dict( name="subject", label=_(u"Subject"), description=_(u"Subject of the Question"), ),
        dict( name="question_text", property=schema.Text(title=_(u"Question"), required=True )),
        #label=_("Question"), description=_(u"The Question submitted")),        
        dict( name="status", label=_(u"Status"), omit=True ),
        dict( name="supplement_parent_id", omit=True), #XXX
        dict( name="sitting_id", omit=True), #XXX
        dict( name="sitting_time", label=_(u"Sitting Time"), listing=True ),
        ]
        
class ResponseDescriptor( ModelDescriptor ):
    display_name = _(u"Response")
    
    fields = [
        dict( name="response_id", omit=True ),
        dict( name="question_id", label=_(u"Question") ), #XXX
        dict( name="response_text", label=_(u"Response"), description=_(u"Response to the Question") ),
        dict( name="type", label=_(u"Response Type"), description=_(u"(I)nitial or (S)ubsequent Response"), listing=True ),		
        dict( name="sitting_id", omit=True ), #XXX
        dict( name="sitting_time", label=_(u"Sitting Time"), description=_(u"Time of the Sitting"), listing=True ),
        ]        

class ConstituencyDescriptor( ModelDescriptor ):
	fields = [
        dict( name="constituency_id", omit=True ),
        #dict( name="constituency_identifier", label=_(u"Identifier"), description=_(u"Identifier of the Constitueny, usually a Number"), listing =True ),
        dict( name="name", label=_(u"Name"), description=_("Name of the constituency"), listing=True ),
        dict(name="province",
            property = schema.Choice( title=_(u"Province"), source=DatabaseSource(domain.Province,'province', 'province_id'), 
            required=True )
            ),
         dict( name="region", label=_(u"Region"),
             property = schema.Choice( title=_(u"Region"), source=DatabaseSource(domain.Region,'region', 'region_id'), 
             required=True )
            ),
        dict( name="start_date", label=_(u"Start Date"), listing=True ),
        dict( name="end_date", label=_(u"End Date"), listing=True ),        
        ]
        
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
		
class ConstituencyDetailDescriptor( ModelDescriptor ):
    fields = [
        dict( name="constituency_detail_id", omit=True ),
        dict( name="constituency_id", label=_(u"Name"), description=_("Name of the constituency"), listing=False, omit=True ), #XXX
        #dict( name='constituency_id',
        #      property = schema.Choice( title=_(u"Constituency"), 
        #                                source=DatabaseSource(domain.Constituency, 'constituency_identifier','constituency_id'), 
        #                                required=True),
        #      
        #    ),
        dict( name="date", label=_(u"Date"), description=_(u"Date the data was submitted from the Constituency"), listing=True ),
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
        dict( name="start_date", label=_(u"Start Date"), listing=True ),
        dict( name="end_date", label=_(u"End Date"), listing=True ),
        ]
        
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
 
 
 
