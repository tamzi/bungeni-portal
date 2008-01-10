from ore.alchemist.model import ModelDescriptor
from i18n import _

class UserDescriptor( ModelDescriptor ):
    fields = [
        dict( name="user_id", omit=True),
        dict( name="first_name", label=_(u"First Name")),
        dict( name="last_name", label=_(u"Last Name")),
        dict( name="middle_name", label=_(u"Middle Name")),
        dict( name="email", label=_(u"Email")),
        dict( name="national_id", label=_(u"National Id")),
        dict( name="gender", label=_(u"Gender")),
        dict( name="date_of_birth", label=_(u"Date of Birth")),
        dict( name="birth_country", label=_(u"Country of Birth")),
        dict( name="date_of_death", label=_(u"Date of Death"), view_permission="bungeni.AdminUsers", write_permission="bungeni.AdminUsers"),
        dict( name="password", omit=True ),
        dict( name="salt", omit=True),
        dict( name="active_p", label=_(u"Active"), view_permission="bungeni.AdminUsers", write_permission="bungeni.AdminUsers"),
        dict( name="type", omit=True ),
        ]

class ParliamentMembers( UserDescriptor ):

    fields = [
        dict( name="member_id", omit=True ),
        # this is only meant as a shortcut.. to the active parliament, else use group memberships
        dict( name="parliaments.parliament_id",),
        dict( name="constituency_id", label=_(u"Constituency")),
        # these are again short cuts..
        dict( name="start_date", label=_(u"Start Date")),
        dict( name="end_date", label=_(u"End Date")  ),
        dict( name="leave_reason", label=_(u"Leave Reason")  ),
        dict( name="active_p", label=_(u"Active"), write_permission="bungeni.AdminUsers"),
        ]

    
class MotionDescriptor( ModelDescriptor ):

    fields = [
        dict( name="motion_id", omit=True ),
        dict( name="session_id", label=_(u"Session") ),
        dict( name="submission_date", label=_(u"Submission Date") ),
        dict( name="received_date", label=_(u"Received Date")),
        dict( name="notice_date", label=_(u"Notice Date")),        
        dict( name="type",label=_(u"Type")),
        dict( name="subject", label=_(u"Subject") ),
        dict( name="identifier", label=_(u"Identifier")),
        dict( name="owner_id", label=_(u"Owner")),
        dict( name="motion_text", label=_(u"Motion Text")),
        dict( name="entered_by", label=_(u"Entered By")),
        dict( name="party_id", label=_(u"Party") ),
        dict( name="status", label=_(u"Status") )
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

