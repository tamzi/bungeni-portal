from ore.alchemist.model import ModelDescriptor

from copy import deepcopy
from zope import schema
import vocabulary
from alchemist.ui import widgets

from i18n import _

class UserDescriptor( ModelDescriptor ):
    fields = [
        dict( name="user_id", omit=True),
        dict( name="first_name", label=_(u"First Name"), listing=True),
        dict( name="last_name", label=_(u"Last Name"), listing=True),
        dict( name="middle_name", label=_(u"Middle Name")),
        dict( name="email", label=_(u"Email")),
        dict( name="national_id", label=_(u"National Id")),
        dict( name="gender", label=_(u"Gender")),
        dict( name="date_of_birth", label=_(u"Date of Birth")),
        dict( name="birth_country", label=_(u"Country of Birth")),
        dict( name="date_of_death", label=_(u"Date of Death"), view_permission="bungeni.AdminUsers", edit_permission="bungeni.AdminUsers"),
        dict( name="password", omit=True ),
        dict( name="salt", omit=True),
        dict( name="active_p", label=_(u"Active"), view_permission="bungeni.AdminUsers", edit_permission="bungeni.AdminUsers"),
        dict( name="type", omit=True ),
        ]

class MemberDescriptor( UserDescriptor ):

    fields = deepcopy( UserDescriptor.fields )
    fields.extend([
        dict( name="member_id", omit=True ),
        # this is only meant as a shortcut.. to the active parliament, else use group memberships
        dict( name="parliaments.parliament_id",),
        dict( name="constituency_id", label=_(u"Constituency")), #XXX
        # these are again short cuts..
        dict( name="start_date", label=_(u"Start Date"), listing=True),
        dict( name="end_date", label=_(u"End Date"), listing=True ),
        dict( name="leave_reason", label=_(u"Leave Reason")  ),
        ])
        
class HansardReporterDescriptor( UserDescriptor ):
	
	 fields = deepcopy( UserDescriptor.fields )	        

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
        dict( name="short_name", label=_(u"Name"), listing=True ),
        dict( name="full_name", label=_(u"Full Name"), listing=True ),
        dict( name="description", property=schema.Text(title=_(u"Description"))),
        dict( name="identifier", label=_(u"Parliamentary Identifier"), listing=True ),
        dict( name="election_date", label=_(u"Election Date")),        
        dict( name="start_date", label=_(u"Start Date")),
        dict( name="end_date", label=_(u"End Date")),        
        ]
        
class CommitteeDescriptor( GroupDescriptor ):
    
    fields = deepcopy( GroupDescriptor.fields )
    
class PolitcalPartyDescriptor( GroupDescriptor ):
     
    fields = deepcopy( GroupDescriptor.fields )    
    
class MinistryDescriptor( GroupDescriptor ):

	fileds = deepcopy( GroupDescriptor.fields )       
    
    
class ParliamentSession( ModelDescriptor ):
    
    fields = deepcopy( GroupDescriptor.fields )
    fields.extend([
        dict( name="session_id", omit=True ),
        dict( name="start_date", label=_(u"Start Date")),
        dict( name="end_date", label=_(u"End Date")),                
        dict( name="notes", property=schema.Text(title=_(u"Notes")))
        ])
        
class GovernmentDescriptor( ModelDescriptor ):
    
    fields = deepcopy( GroupDescriptor.fields )    
    fields.extend([
        dict( name="government_id", omit=True),
        dict( name="start_gazetted_date", label=_(u"Gazetted Start Date") ),
        dict( name="end_gazetted_date", label=_(u"Gazetted End Date") )
        ])
    
class MotionDescriptor( ModelDescriptor ):

    fields = [
        dict( name="motion_id", omit=True ),
        dict( name="title", label=_(u"Subject"), listing=True,
              edit_widget = widgets.LongTextWidget),
        dict( name="session_id", 
              property = schema.Choice( title=_(u"Session"), source=vocabulary.ParliamentSessions, required=False )
              ),
        dict( name="submission_date", label=_(u"Submission Date"), listing=True ),
        dict( name="received_date", label=_(u"Received Date")),
        dict( name="notice_date", label=_(u"Notice Date"), listing=True),        
#        dict( name="type", label=_(u"Public"),
#              edit_widget = widgets.YesNoInputWidget,
#              view_widget = widgets.YesNoDisplayWidget),
        dict( name="identifier", label=_(u"Identifier")),
        dict( name="owner_id",
              property = schema.Choice( title=_(u"Owner"), source=vocabulary.ParliamentMembers, required=False )
              ),
        dict( name="body_text", label=_(u"Motion Text"),
              property = schema.Text( title=u"Motion" ),
              ),
        # TODO omit for now
        dict( name="entered_by", label=_(u"Entered By"), omit=True ), 
        dict( name="party_id",
            property = schema.Choice( title=_(u"Political Party"), source=vocabulary.PoliticalParties, required=False) ),
        dict( name="status", label=_(u"Status"), listing=True, edit=False )
        ]

class SittingDescriptor( ModelDescriptor ):
    fields = [
        dict( name="sitting_id", omit=True ),
        dict( name="group_id", omit=True ),
        dict( name="session_id", omit=True ),
        dict( name="start_date", label=_(u"Start Date") ),
        dict( name="end_date", label=_(u"End Date") ),
        ]

class SessionDescriptor( ModelDescriptor ):
    fields = [
        dict( name="session_id", omit=True),
        #dict( name="parliament_id",)
        dict( name="short_name", label=_(u"Short Name"), listing=True ),
        dict( name="full_name", label=_(u"Full Name") ),
        dict( name="start_date", label=_(u"Start Date"), listing=True ),
        dict( name="end_date", label=_(u"End Date"), listing=True ),
        dict( name="notes", label=_(u"Notes") )
        ]
        
class BillDescriptor( ModelDescriptor ):
    
    fields = [
        dict( name="bill_id", omit=True ),
        dict( name="title", label=_(u"Title"), listing=True ),
        dict( name="preamble", label=_(u"Preamble")),
        dict( name="session_id", label=_(u"Session") ),
        dict( name="identifier", label=_(u"Identifer") ),
        dict( name="submission_date", label=_(u"Submission Date"), listing=True ),
        dict( name="publication_date", label=_(u"Publication Date") ),        
        dict( name="status", label=_(u"Status"), listing=True )
        ]

class QuestionDescriptor( ModelDescriptor ):
	
	fields = [
		dict( name="question_id", omit=True),
		dict( name="session_id", 
				property = schema.Choice( title=_(u"Session"), source=vocabulary.ParliamentSessions, required=False )
			),
		dict( name="clerk_submission_date", label=_(u"Submission Date"), listing=True ),
		dict( name="question_type", label=_(u"Question Type"), description=_("(O)rdinary or (P)rivate Notice"),  listing=True ), 
		#dict( name="question_type",
		#		property = schema.Choice( title=_(u"Question Type"), description=_("(O)rdinary or (P)rivate Notice"), source=vocabulary.QuestionType, required=False )
        #      ),
		dict( name="response_type", label=_(u"Response Type"), description=_("(O)ral or (W)ritten"), listing=True ),
		dict( name="owner", 
				property = schema.Choice( title=_(u"Owner"), source=vocabulary.ParliamentMembers, required=True )
              ),
        dict( name="status", label=_(u"Status"), listing=True ),
        dict( name="supplement_parent_id", omit=True), #XXX
        dict( name="sitting_id", omit=True), #XXX
        dict( name="sitting_time", label=_(u"Sitting Time"), listing=True ),
        ]
        
class ResponseDescriptor( ModelDescriptor ):
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
		dict( name="name", label=_(u"Name"), description=_("Name of the constituency"), listing=True ),
		dict( name="province", label=_(u"Province"), description=_(u"Name of the Province"), listing=True ),
		dict( name="region", label=_(u"Region"), description=_(u"Name of the Region"), listing=True ),
		dict( name="voters", label=_(u"Voters"), description=_(u"Number of Voters in the constituency"), listing=True ),
		]
		

        
