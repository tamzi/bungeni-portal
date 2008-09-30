#!/usr/bin/env python
# encoding: utf-8
"""


"""

import sqlalchemy as rdb
from datetime import datetime
metadata = rdb.MetaData()

ItemSequence = rdb.Sequence('item_sequence') # used for Bills, motions, questions
PrincipalSequence = rdb.Sequence('principal_sequence') # for users and groups because of the zope users and groups

#######################
# Users 
#######################
# 

users = rdb.Table(
   "users",
   metadata,
   rdb.Column( "user_id", rdb.Integer, PrincipalSequence, primary_key=True ),
   rdb.Column( "login", rdb.Unicode(16), unique=True, nullable=True ),
   rdb.Column( "titles", rdb.Unicode(32)),
   rdb.Column( "first_name", rdb.Unicode(80), nullable=False ),
   rdb.Column( "last_name", rdb.Unicode(80), nullable=False ),
   rdb.Column( "middle_name", rdb.Unicode(80) ),
   rdb.Column( "email", rdb.String(32), nullable=False ),
   rdb.Column( "gender", rdb.String(1),
        rdb.CheckConstraint("gender in ('M', 'F')")
        ), # (M)ale (F)emale       
   rdb.Column( "date_of_birth", rdb.Date ),
   rdb.Column( "birth_country", rdb.String(2), rdb.ForeignKey("countries.country_id") ),
   rdb.Column( "birth_nationality", rdb.String(2), rdb.ForeignKey("countries.country_id") ),
   rdb.Column( "current_nationality", rdb.String(2), rdb.ForeignKey("countries.country_id") ),
   rdb.Column( "uri", rdb.String(120), unique=True),
   rdb.Column( "date_of_death", rdb.Date ),
   rdb.Column( "type_of_id", rdb.String(1)),
   rdb.Column( "national_id", rdb.Unicode(32) ),
   rdb.Column( "password", rdb.String(36)), # we store salted md5 hash hexdigests
   rdb.Column( "salt", rdb.String(24)),  
   rdb.Column( "description", rdb.UnicodeText ),  
   rdb.Column( "image", rdb.Binary),
   rdb.Column( "active_p", rdb.String(1),
                rdb.CheckConstraint("active_p in ('A', 'I', 'D')"),
                default="A", #activ/inactiv/deceased
                ), 
   rdb.Column( "type", rdb.String(30), nullable=False  ),
   )

# # not in use yet, but potentially for all 
# # ownership, sponsorship, etc of bills/motions/questions
# user_item_associations = rdb.Table(
#    "user_associations",
#    metadata,
#    rdb.Column( "object_id", rdb.Integer ), # any object placed here needs to have a class hierarchy sequence
#    rdb.Column( "user_id", rdb.Integer, rdb.ForeignKey('users.user_id') ),
#    rdb.Column( "title", rdb.Unicode(16)), # title of user's assignment role
#    rdb.Column( "start_date", rdb.DateTime, default=rdb.PassiveDefault('now') ),
#    rdb.Column( "end_date", rdb.DateTime ),
#    rdb.Column( "notes", rdb.Unicode ),
#    rdb.Column( "type", rdb.Unicode(16) ),   
#    )


   

# specific user classes
parliament_members = rdb.Table(
   "parliament_members",
   metadata,
   rdb.Column( "membership_id", rdb.Integer, rdb.ForeignKey('user_group_memberships.membership_id'), primary_key=True ),
   rdb.Column( "constituency_id", rdb.Integer, rdb.ForeignKey('constituencies.constituency_id') ),
   rdb.Column( "elected_nominated", rdb.String(1), # is the MP elected, nominated, ex officio member, ...
                rdb.CheckConstraint("elected_nominated in ('E','O','N')"),
                nullable=False ),
   rdb.Column( "election_nomination_date", rdb.Date), # nullable=False ),
   rdb.Column( "leave_reason", rdb.Unicode(40) ),


   )   

# staff assigned to a group ( committee clerks, researchers, ...)

#staff_groupmember = rdb.Table(
#    "staff_groupmember",
#    metadata,
#    rdb.Column( "membership_id", rdb.Integer, rdb.ForeignKey('user_group_memberships.membership_id'), primary_key=True ),
#    # other stuff to be added here to describe staffs role etc for the group
#    )



reporters = rdb.Table(
   "reporters",
   metadata,
   rdb.Column( "reporter_id", rdb.Integer, rdb.ForeignKey('users.user_id'), primary_key=True ),
   rdb.Column( "initials", rdb.Unicode(4), nullable=False ),
   rdb.Column( "experience", rdb.Unicode(1), default=u'N'),
   rdb.Column( "typing_speed", rdb.Integer ),
   rdb.Column( "status", rdb.Unicode(1), default=u'A' ),
   )


#########################
#constituencies
#########################
constituencies = rdb.Table(
   "constituencies",
   metadata,
   rdb.Column( "constituency_id", rdb.Integer,  primary_key=True ),
   rdb.Column( "name", rdb.Unicode(80), nullable=False ),
   rdb.Column( "province", rdb.Integer, rdb.ForeignKey('provinces.province_id') ),
   rdb.Column( "region", rdb.Integer, rdb.ForeignKey('regions.region_id') ),
   rdb.Column( "start_date", rdb.Date, nullable=False ),
   rdb.Column( "end_date", rdb.Date ),   
   )
#constituency_changes = make_changes_table( constituencies, metadata )
#constituency_version = make_versions_table( constituencies, metadata )

provinces = rdb.Table(
    "provinces",
    metadata,
    rdb.Column( "province_id", rdb.Integer,  primary_key=True ),
    rdb.Column( "province", rdb.Unicode(80), nullable=False ),
    )
    
regions = rdb.Table(
    "regions",
    metadata,
    rdb.Column( "region_id", rdb.Integer,  primary_key=True ),
    rdb.Column( "region", rdb.Unicode(80), nullable=False ),    
    )
    
countries = rdb.Table(
    "countries",
    metadata,
    rdb.Column( "country_id", rdb.String(2), primary_key=True ),
    rdb.Column( "country_name", rdb.Unicode(80), nullable=False ),
    )
        
constituency_details = rdb.Table(
    "constituency_details",
    metadata,
    rdb.Column( "constituency_detail_id", rdb.Integer,  primary_key=True ),
    rdb.Column( "constituency_id", rdb.Integer, rdb.ForeignKey('constituencies.constituency_id') ),
    rdb.Column( "date", rdb.Date, nullable=False ),
    rdb.Column( "population", rdb.Integer, nullable=False ),
    rdb.Column( "voters", rdb.Integer, nullable=False ),
    )


#######################
# Groups
#######################
"""
we're using a very normalized form here to represent all kinds of groups and their relations to 
other things in the system.
"""


groups = rdb.Table(
   "groups",
   metadata,
   rdb.Column( "group_id", rdb.Integer, PrincipalSequence,  primary_key=True ),
   rdb.Column( "short_name", rdb.Unicode(40), nullable=False ),
   rdb.Column( "full_name", rdb.Unicode(80) ),   
   rdb.Column( "description", rdb.UnicodeText ),
   rdb.Column( "status", rdb.Unicode(12) ), # workflow for groups
   rdb.Column( "start_date", rdb.Date, nullable=False ),
   rdb.Column( "end_date", rdb.Date ),  #
   rdb.Column( "type", rdb.String(30),  nullable=False )
   )

governments = rdb.Table(
   "government",
   metadata,
   rdb.Column( "government_id", rdb.Integer, rdb.ForeignKey('groups.group_id'), primary_key=True ),
   rdb.Column( "parliament_id", rdb.Integer, rdb.ForeignKey('parliaments.parliament_id'), nullable=False),
   )

parliaments = rdb.Table(
   "parliaments",
   metadata,
   rdb.Column( "parliament_id", rdb.Integer, rdb.ForeignKey('groups.group_id'), primary_key=True ),   
   rdb.Column( "election_date", rdb.Date , nullable=False ),
   )

ministries = rdb.Table(
   "ministries",
   metadata,
   rdb.Column( "ministry_id", rdb.Integer, rdb.ForeignKey('groups.group_id'), primary_key=True ),
   rdb.Column( "government_id", rdb.Integer, rdb.ForeignKey('government.government_id')),
   )

committees = rdb.Table(
   "committees",
   metadata,
   rdb.Column( "committee_id", rdb.Integer, rdb.ForeignKey('groups.group_id'), primary_key=True ),
   rdb.Column( "parliament_id", rdb.Integer, rdb.ForeignKey('parliaments.parliament_id')),
   rdb.Column( "committee_type_id", rdb.Integer, rdb.ForeignKey( 'committee_types.committee_type_id')),
   rdb.Column( "no_members", rdb.Integer),
   rdb.Column( "min_no_members", rdb.Integer),
   rdb.Column( "quorum", rdb.Integer ),
   rdb.Column( "no_clerks", rdb.Integer ),
   rdb.Column( "no_researchers", rdb.Integer ),
   rdb.Column( "proportional_representation", rdb.Boolean ),
   rdb.Column( "default_chairperson", rdb.Boolean ),
   rdb.Column( "reinstatement_date", rdb.Date ),
   )

committee_type = rdb.Table(
    "committee_types",
    metadata,
    rdb.Column("committee_type_id", rdb.Integer,  primary_key=True),
    rdb.Column("committee_type", rdb.Unicode(80), nullable=False),
    rdb.Column("description", rdb.UnicodeText),
    rdb.Column("life_span", rdb.Unicode(16)),
    rdb.Column("status", rdb.String(1),             
       rdb.CheckConstraint("status in ('P','T')"),  # Indicate whether this type of committees are: ‘P' - Permanent, ‘T' - Temporary 
                nullable=False ),
                
    )

political_parties = rdb.Table(
   "political_parties",
   metadata,
   rdb.Column( "party_id", rdb.Integer, rdb.ForeignKey('groups.group_id'), primary_key=True ),   
   rdb.Column( "logo_data", rdb.Binary, ),
   rdb.Column( "logo_name", rdb.String(40)),
   rdb.Column( "logo_mimetype", rdb.String(40)),
   rdb.Column( "parliament_id", rdb.Integer, rdb.ForeignKey('parliaments.parliament_id')),   
   )

###
#  the personal role of a user in terms of their membership this group
#  The personal roles a person may have varies with the context. In a party
#  one may have the role spokesperson, member, ...

user_role_type = rdb.Table(
    "user_role_types",
    metadata,
    rdb.Column( "user_role_type_id", rdb.Integer, primary_key=True),
    rdb.Column( "user_type", rdb.String(30),  nullable=False  ),
    rdb.Column( "user_role_name", rdb.Unicode(40), nullable=False),
    rdb.Column( "user_unique", rdb.Boolean, default=False,),# nullable=False ),
    rdb.Column( "sort_order", rdb.Integer(2), nullable=False),
    )

###
#  group extensions define additional members which can be assigned to a group
#  by user_group_memberships. allthough this is not limited by the implementation of 
#  user_group_memberships the application has to restrict the group membership
#  a) to avoid invalid input
#  b) to limit the number of choices
#  

extension_groups = rdb.Table(
    "extension_groups",
    metadata,
    rdb.Column( "extension_type_id", rdb.Integer, rdb.ForeignKey('groups.group_id'), primary_key=True ),
    rdb.Column( "group_type", rdb.String(30),  nullable=False  ),
    rdb.Column( "parliament_id", rdb.Integer, rdb.ForeignKey('parliaments.parliament_id'), nullable=False),
    )

    
    


#
# group memberships encompasses any user participation in a group, including
# substitutions.

user_group_memberships = rdb.Table(
   "user_group_memberships",
   metadata,
   rdb.Column( "membership_id", rdb.Integer,  primary_key=True),
   rdb.Column( "user_id", rdb.Integer, rdb.ForeignKey( 'users.user_id')),
   rdb.Column( "group_id", rdb.Integer, rdb.ForeignKey( 'groups.group_id')),
   rdb.Column( "start_date", rdb.Date, default=datetime.now, nullable=False ),
   rdb.Column( "end_date", rdb.Date ),
   rdb.Column( "notes", rdb.UnicodeText ),   
   # we use this as an easier query to end_date in queries, needs to be set by
   # a cron process against end_date < current_time
   rdb.Column( "active_p", rdb.Boolean, default=True ),
   # these fields are only present when a membership is a result of substitution   
   # unique because you can only replace one specific group member.
   rdb.Column( "replaced_id", rdb.Integer, rdb.ForeignKey('user_group_memberships.membership_id'), unique=True ),
   rdb.Column( "substitution_type", rdb.Unicode(100) ),
   # type of membership staff or member
   rdb.Column( "membership_type", rdb.String(30), default ="member",) # nullable = False),
   )
  
# a bill assigned to a committee, a question assigned to a ministry
group_item_assignments = rdb.Table(
   "group_assignments",
   metadata,
   rdb.Column( "assignment_id", rdb.Integer,  primary_key=True ),
   rdb.Column( "object_id", rdb.Integer ), # any object placed here needs to have a class hierarchy sequence
   rdb.Column( "object_type", rdb.String(128), nullable=False ),
   rdb.Column( "group_id", rdb.Integer, rdb.ForeignKey('groups.group_id') ),
   rdb.Column( "start_date", rdb.Date, default=datetime.now, nullable=False),
   rdb.Column( "end_date", rdb.Date ),   
   rdb.Column( "due_date", rdb.Date ),
   rdb.Column( "status", rdb.String(16) ),    
   rdb.Column( "notes", rdb.UnicodeText ),
   )


##############
# Titles
##############
# To indicate the role a persons has in a specific context (Ministry, Committee, Parliament,...) 
# and for what period (from - to)

role_titles = rdb.Table(
    "role_titles",
    metadata,
    rdb.Column( "role_title_id", rdb.Integer, primary_key=True ),
    rdb.Column( "membership_id", rdb.Integer, rdb.ForeignKey('user_group_memberships.membership_id') ),
    rdb.Column( "title_name_id", rdb.Integer, rdb.ForeignKey('user_role_types.user_role_type_id') ), # title of user's group role
    rdb.Column( "start_date", rdb.Date, default=datetime.now, nullable=False),
    rdb.Column( "end_date", rdb.Date ),   
    )



############
# Addresses
############
# Adresses can be attached to a user or to a role title 
# as the official address for this function

address_types = rdb.Table (
    "address_types",
    metadata,
    rdb.Column( "address_type_id", rdb.Integer, primary_key = True ),
    rdb.Column( "address_type_name", rdb.Unicode(40) ),
    )

addresses = rdb.Table(
    "addresses",
    metadata,
    rdb.Column( "address_id", rdb.Integer, primary_key=True ),
    rdb.Column( "role_title_id", rdb.Integer, rdb.ForeignKey('role_titles.role_title_id') ), # official address
    rdb.Column( "user_id", rdb.Integer, rdb.ForeignKey( 'users.user_id') ), # personal address
    rdb.Column( "address_type_id", rdb.Integer, rdb.ForeignKey ( 'address_types.address_type_id') ),
    rdb.Column( "po_box", rdb.Unicode(40) ),
    rdb.Column( "address", rdb.Unicode(80) ),
    rdb.Column( "city", rdb.Unicode(80) ),
    rdb.Column( "zipcode", rdb.Unicode(20) ),
    rdb.Column( "country", rdb.String(2), rdb.ForeignKey("countries.country_id") ),
    rdb.Column( "phone", rdb.Unicode(80) ),
    rdb.Column( "fax", rdb.Unicode(40) ),
    rdb.Column( "email", rdb.String(40) ),
    rdb.Column( "im_id", rdb.String(40) ),
    # Workflow State -> determins visibility
    rdb.Column( "status", rdb.Unicode(16) ),
    )









#############
# Keywords
#############

keywords = rdb.Table(
    "keywords",
    metadata,
    rdb.Column( "keyword_id", rdb.Integer, primary_key=True),
    rdb.Column( "keyword_name", rdb.Unicode(32), unique=True),
    )

groups_keywords = rdb.Table(
    "groups_keywords",
    metadata,
    rdb.Column( "keyword_id", rdb.Integer, rdb.ForeignKey('keywords.keyword_id'), primary_key=True),
    rdb.Column( "group_id", rdb.Integer, rdb.ForeignKey('groups.group_id'), primary_key=True ),
    )    



##################
# Activity 
# 
parliament_sessions = rdb.Table(
   "sessions",
   metadata,
   rdb.Column( "session_id", rdb.Integer,   primary_key=True ),
   rdb.Column( "parliament_id", rdb.Integer, rdb.ForeignKey('parliaments.parliament_id')),
   rdb.Column( "short_name", rdb.Unicode(32) ),
   rdb.Column( "full_name", rdb.Unicode(32) ),      
   rdb.Column( "start_date", rdb.Date, nullable=False),
   rdb.Column( "end_date", rdb.Date),
   rdb.Column( "notes", rdb.UnicodeText )   
   )

# sittings = rdb.Table(
#    "sittings",
#    metadata,
#    rdb.Column( "sitting_id", rdb.Integer, primary_key=True ),
#    rdb.Column( "session_id", rdb.Integer, rdb.ForeignKey('sessions.session_id')),
#    rdb.Column( "start_date", rdb.DateTime),
#    rdb.Column( "end_date", rdb.DateTime),   
#    )

sittings = rdb.Table(
   "group_sittings",
   metadata,
   rdb.Column( "sitting_id", rdb.Integer,  primary_key=True ),
   rdb.Column( "group_id", rdb.Integer, rdb.ForeignKey('groups.group_id') ),
   rdb.Column( "session_id", rdb.Integer, rdb.ForeignKey('sessions.session_id')),
   rdb.Column( "start_date", rdb.DateTime( timezone=False ), nullable=False),
   rdb.Column( "end_date", rdb.DateTime( timezone=False ), nullable=False), 
   rdb.Column( "sitting_type", rdb.Integer, rdb.ForeignKey('sitting_type.sitting_type_id')),
   )   

sitting_type = rdb.Table(
    "sitting_type",
    metadata,
    rdb.Column( "sitting_type_id", rdb.Integer, primary_key=True ),
    rdb.Column( "sitting_type", rdb.Unicode(40)),
    )

sitting_schedule = rdb.Table(
   "sitting_schedule",
   metadata,
   rdb.Column( "sitting_id", rdb.Integer, rdb.ForeignKey('group_sittings.sitting_id')),
   rdb.Column( "item_id",  rdb.Integer, nullable=False),   
   rdb.Column( "item_type", rdb.Unicode(80) ),
   rdb.Column( "order", rdb.Integer ),
   )
   
sitting_attendance = rdb.Table(
   "sitting_attendance",
   metadata,
   rdb.Column( "sitting_id", rdb.Integer, rdb.ForeignKey('group_sittings.sitting_id'),  primary_key=True  ),
   rdb.Column( "member_id",  rdb.Integer, rdb.ForeignKey('users.user_id'),  primary_key=True  ),
   rdb.Column( "attendance_id", rdb.Integer, rdb.ForeignKey('attendance_type.attendance_id'), nullable=False ), 
   )
   
attendance_type = rdb.Table(
   "attendance_type",
   metadata,
   rdb.Column ("attendance_id", rdb.Integer, primary_key=True ),
   rdb.Column ("attendance_type", rdb.Unicode(40), nullable=False ),
   )
# 

debates = rdb.Table(
    "debates",
    metadata,
    rdb.Column( "debate_id", rdb.Integer, primary_key=True ),
    rdb.Column( "sitting_id", rdb.Integer, rdb.ForeignKey('group_sittings.sitting_id') ),
    rdb.Column( "short_name", rdb.Unicode(40), nullable=False ),
    rdb.Column( "body_text", rdb.UnicodeText),
    )

#######################
# Parliament
#######################   



# Parliamentary Items
# 
def make_changes_table( table, metadata ):
    """ create an object log table for an object """
    table_name = table.name
    entity_name =  table_name.endswith('s') and table_name[:-1] or table_name
    
    changes_name = "%s_changes"%( entity_name )
    fk_id = "%s_id"%( entity_name )
    #print entity_name, fk_id
    
    changes_table = rdb.Table(
            changes_name,
            metadata,
            rdb.Column( "change_id", rdb.Integer, primary_key=True ),
            rdb.Column( "content_id", rdb.Integer, rdb.ForeignKey( table.c[ fk_id ] ) ),
            rdb.Column( "action", rdb.Unicode(16) ),
            rdb.Column( "date", rdb.Date, default=datetime.now),
            rdb.Column( "description", rdb.UnicodeText),
            rdb.Column( "notes", rdb.UnicodeText),
            rdb.Column( "user_id", rdb.Unicode(32) ) # Integer, rdb.ForeignKey('users.user_id') ),
    )
    
    return changes_table
 
def make_versions_table( table, metadata ):
    """
    create a versions table, requires change log table for which some version metadata information will be stored.
    """
    table_name = table.name
    entity_name =  table_name.endswith('s') and table_name[:-1] or table_name
    
    versions_name = "%s_versions"%( entity_name )
    fk_id = "%s_id"%( entity_name )
    
    columns = [
        rdb.Column( "version_id", rdb.Integer, primary_key=True ),
        #rdb.Column( "version_created", rdb.DateTime, default=rdb.PassiveDefault('now') ),
        rdb.Column( "content_id", rdb.Integer, rdb.ForeignKey( table.c[ fk_id ] ) ),
        rdb.Column( "change_id", rdb.Integer, rdb.ForeignKey('%s_changes.change_id'%entity_name))
    ]
    
    columns.extend( [ c.copy() for c in table.columns if not c.primary_key ] )
    
    #primary = [ c.copy() for c in table.columns if c.primary_key ][0]
    #primary.primary_key = False
    #columns.insert( 2, primary )
    
    versions_table = rdb.Table(
            versions_name,
            metadata,
            *columns 
            )
            
    return versions_table
    


item_votes = rdb.Table( 
   'item_votes',
   metadata,
   rdb.Column( "vote_id", rdb.Integer, primary_key=True ),
   rdb.Column( "item_id", rdb.Integer, nullable=False ),
   rdb.Column( "date", rdb.Date ),
#   rdb.Column( "division_p",  rdb.Boolean ), # isn't a division implied by the vote?
   rdb.Column( "affirmative_votes", rdb.Integer),
   rdb.Column( "negative_votes", rdb.Integer ),
   rdb.Column( "remarks", rdb.UnicodeText  ),   
   )

item_member_votes = rdb.Table(
   "item_member_votes",
   metadata,
   rdb.Column( "vote_id", rdb.Integer, rdb.ForeignKey('item_votes') ),
   rdb.Column( "member_id",  rdb.Integer, rdb.ForeignKey('users.user_id') ),
   rdb.Column( "vote",  rdb.Boolean,),
   )

items_schedule = rdb.Table(
   "items_schedule",
   metadata,
   rdb.Column( "schedule_id", rdb.Integer, primary_key=True ),
   rdb.Column( "item_id",  rdb.Integer, nullable=False ),
   rdb.Column( "sitting_id", rdb.Integer, rdb.ForeignKey('group_sittings.sitting_id'), nullable=False ),
   rdb.Column( "order", rdb.Integer )
   )

# generic subscriptions, to any type
subscriptions = rdb.Table(
   "object_subscriptions",
   metadata,
   rdb.Column( "subscriptions_id", rdb.Integer, primary_key=True ),
   rdb.Column( "object_id",  rdb.Integer, nullable=False ),
   rdb.Column( "object_type", rdb.String(32), nullable=False ),
   rdb.Column( "party_id",  rdb.Integer, nullable=False ),
   rdb.Column( "party_type", rdb.String(32), nullable=False ),
   rdb.Column( "last_delivery", rdb.Date, nullable=False ),   
   # delivery period
   # rdb.Column( "delivery_period",  rdb.Integer ),
   # delivery type
   # rdb.Column( "delivery_type", rdb.Integer ),
   )



questions = rdb.Table(
   "questions",
   metadata,
   rdb.Column( "question_id", rdb.Integer, ItemSequence, primary_key=True ),
   
   rdb.Column( "session_id", rdb.Integer, rdb.ForeignKey('sessions.session_id')),
   rdb.Column( "clerk_submission_date", rdb.Date,),
   rdb.Column( "approval_date", rdb.Date,),  
   rdb.Column( "ministry_submit_date", rdb.Date, ), 
   rdb.Column( "question_type", rdb.Unicode(1), 
                rdb.CheckConstraint("question_type in ('O', 'P')"), default=u"O" ), # (O)rdinary (P)rivate Notice
   rdb.Column( "response_type", rdb.Unicode(1), 
                rdb.CheckConstraint("response_type in ('O', 'W')"), default=u"O" ), # (O)ral (W)ritten

   # TODO - ? normalize to use user item associations.
   rdb.Column( "owner_id", rdb.Integer),#, nullable=False ),
   rdb.Column( "parliament_id", rdb.Integer),#, nullable=False ),
   #rdb.ForeignKeyConstraint(['owner', 'parliament_id'], ['parliament_members.member_id', 'parliament_members.parliament_id']),
   rdb.Column( "subject", rdb.Unicode(80)),#, nullable=False ),
   rdb.Column( "question_text", rdb.UnicodeText),#, nullable=False ),
   # Workflow State
   rdb.Column( "status", rdb.Unicode(32) ),
   # the cerks office or speakers office may add a recommendation note
   rdb.Column( "note", rdb.UnicodeText),
   # if this is a supplementary question, this is the original/previous question
   rdb.Column( "supplement_parent_id", rdb.Integer, rdb.ForeignKey('questions.question_id')  ),
     
   # after the question is scheduled
   rdb.Column( "sitting_id", rdb.Integer, rdb.ForeignKey('group_sittings.sitting_id')  ),
   rdb.Column( "sitting_time", rdb.DateTime( timezone=False ) ),
   #
   # Receive Question Notifications -> triggers notification on workflow change
   rdb.Column( "receive_notification", rdb.Boolean, default=True ),
   rdb.Column( "ministry_id", rdb.Integer, rdb.ForeignKey('ministries.ministry_id')), 
   
   )


# if a scheduled question gets postponed we need to capture the sitting
# and implicitly the date it was scheduled
question_schedules = rdb.Table(
    "question_schedules",
    metadata,
    rdb.Column( "question_id", rdb.Integer, rdb.ForeignKey('questions.question_id'), nullable=False, primary_key=True ),
    rdb.Column( "sitting_id", rdb.Integer, rdb.ForeignKey('group_sittings.sitting_id'), nullable=False, primary_key=True  ),
    )



question_changes = make_changes_table( questions, metadata )
question_versions = make_versions_table( questions, metadata )

#print 'change', repr(question_changes.c.question_id)
#print 'version', repr(question_versions.c.question_id)


responses = rdb.Table(
   "responses",
   metadata,
   rdb.Column( "response_id", rdb.Integer, rdb.ForeignKey('questions.question_id'), primary_key=True ),
   #rdb.Column( "question_id", rdb.Integer, rdb.ForeignKey('questions.question_id'), primary_key=True ),
   rdb.Column( "response_text", rdb.UnicodeText ),
   #rdb.Column( "response_type", rdb.String(1), rdb.CheckConstraint("response_type in ('I','S')"), default=u"I"), # (I)nitial (S)ubsequent
   # 
   # for attachment to the debate record, but not actually scheduled on the floor
   rdb.Column( "sitting_id", rdb.Integer, rdb.ForeignKey('group_sittings.sitting_id') ),
   rdb.Column( "sitting_time", rdb.DateTime( timezone=False ) ),
   rdb.Column( "status",  rdb.Unicode(32) ),
   )

response_changes = make_changes_table( responses, metadata )
response_versions = make_versions_table( responses, metadata )


motions = rdb.Table(
   "motions",
   metadata,
   rdb.Column( "motion_id", rdb.Integer, ItemSequence, primary_key=True ),
   rdb.Column( "session_id", rdb.Integer, rdb.ForeignKey('sessions.session_id')),
   rdb.Column( "submission_date", rdb.Date ),
   rdb.Column( "public", rdb.Boolean ),
   rdb.Column( "title", rdb.Unicode(80) ),
   rdb.Column( "identifier", rdb.Integer),
   rdb.Column( "owner_id", rdb.Integer, rdb.ForeignKey('users.user_id') ),
   rdb.Column( "seconder_id", rdb.Integer, rdb.ForeignKey('users.user_id') ), 
   rdb.Column( "body_text", rdb.UnicodeText ),
   rdb.Column( "received_date", rdb.Date ),
   rdb.Column( "entered_by", rdb.Integer, rdb.ForeignKey('users.user_id') ),   
   rdb.Column( "party_id", rdb.Integer, rdb.ForeignKey('political_parties.party_id')  ), # if the motion was sponsored by a party
   rdb.Column( "notice_date", rdb.Date ),
   # Receive Question Notifications -> triggers notification on workflow change
   rdb.Column( "receive_notification", rdb.Boolean, default=True ),
   rdb.Column( "status",  rdb.Unicode(32) ),
   )

motion_changes = make_changes_table( motions, metadata )
motion_versions = make_versions_table( motions, metadata )

motion_amendments = rdb.Table(
   "motion_amendments",
   metadata,
   rdb.Column( "amendment_id", rdb.Integer, primary_key=True ),
   rdb.Column( "motion_id", rdb.Integer, rdb.ForeignKey('motions.motion_id')  ),
   rdb.Column( "amended_id", rdb.Integer,  ),
   rdb.Column( "body_text", rdb.UnicodeText ),  
   rdb.Column( "submission_date", rdb.Date ),    
   rdb.Column( "accepted_p", rdb.Boolean ),
   rdb.Column( "title", rdb.Unicode(80) ), 
   rdb.Column( "vote_date", rdb.Date ),   
   )

bills = rdb.Table(
   "bills",
   metadata,
   rdb.Column( "bill_id", rdb.Integer, ItemSequence, primary_key=True ),
   rdb.Column( "ministry_id", rdb.Integer, rdb.ForeignKey('ministries.ministry_id') ),
   rdb.Column( "identifier",  rdb.Integer),
   rdb.Column( "preamble", rdb.UnicodeText ),   
   rdb.Column( "title", rdb.Unicode(80) ), 
   rdb.Column( "body_text",  rdb.UnicodeText ),
   rdb.Column( "submission_date", rdb.Date ),
   rdb.Column( "publication_date", rdb.Date ),
   rdb.Column( "status", rdb.Unicode(32) ),
   )
   
bill_changes = make_changes_table( bills, metadata )
bill_versions = make_versions_table( bills, metadata )

committee_reports = ()
#debates = ()

#######################
# Files
#######################

directory_locations = rdb.Table(
    "directory_locations",
    metadata,
    rdb.Column("location_id", rdb.Integer, primary_key=True ),
    rdb.Column("repo_path", rdb.String(250), nullable=False ),
    rdb.Column("object_id", rdb.Integer, nullable=False ),
    rdb.Column("object_type", rdb.String(128), nullable=False ),
    )

#######################
# Hansard
#######################   

rotas = rdb.Table(
   "rotas",
   metadata,
   rdb.Column( "rota_id", rdb.Integer, primary_key=True ),
   rdb.Column( "reporter_id", rdb.Integer, rdb.ForeignKey('users.user_id') ),
   rdb.Column( "identifier", rdb.Unicode(60) ),
   rdb.Column( "start_date", rdb.Date ),
   rdb.Column( "end_date", rdb.Date )
   )

takes = rdb.Table(
   "takes",
   metadata,
   rdb.Column( "take_id", rdb.Integer, primary_key=True ),
   rdb.Column( "rota_id", rdb.Integer, rdb.ForeignKey('rotas.rota_id') ),
   rdb.Column( "identifier", rdb.Unicode(1) ),
   )
   
take_media = rdb.Table(
   "take_media",
   metadata,
   rdb.Column( "media_id", rdb.Integer, primary_key=True ),
   rdb.Column( "take_id", rdb.Integer, rdb.ForeignKey('takes.take_id') ),
   )
   
transcripts = rdb.Table(
   "transcripts",
   metadata,
   rdb.Column( "transcript_id", rdb.Integer, primary_key=True ),
   rdb.Column( "take_id", rdb.Integer, rdb.ForeignKey('takes.take_id')),
   rdb.Column( "reporter_id", rdb.Integer, rdb.ForeignKey('users.user_id')),   
   )

if __name__ == '__main__':    
    import sys

    if len(sys.argv) == 1:
        db_uri = 'sqlite://'
    elif len(sys.argv) != 2:
        print "schema.py DATABASE_URL"
        sys.exit(1)
    else:
        db_uri = sys.argv[1]

        db_uri = 'sqlite://'        
    db = rdb.create_engine( db_uri, echo=True)
    metadata.bind = db

    try:
        metadata.drop_all()        
        metadata.create_all()
        print 'ugm', repr(user_group_memberships.c.user_id.table)
    except:
        import pdb, traceback, sys
        traceback.print_exc()
        pdb.post_mortem(sys.exc_info()[-1])
    

