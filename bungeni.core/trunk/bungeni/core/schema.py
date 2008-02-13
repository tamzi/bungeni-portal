#!/usr/bin/env python
# encoding: utf-8
"""


"""

import sqlalchemy as rdb

metadata = rdb.MetaData()


#######################
# Users 
#######################
# 
users = rdb.Table(
   "users",
   metadata,
   rdb.Column( "user_id", rdb.Integer, primary_key=True ),
   rdb.Column( "login", rdb.Unicode(16), unique=True ),
   rdb.Column( "first_name", rdb.Unicode ),
   rdb.Column( "last_name", rdb.Unicode ),
   rdb.Column( "middle_name", rdb.Unicode ),
   rdb.Column( "email", rdb.Unicode(32), nullable=False ),
   rdb.Column( "gender", rdb.String(1),
        rdb.CheckConstraint("gender in ('M', 'F')") ), # (M)ale (F)emale    ),   
   rdb.Column( "date_of_birth", rdb.DateTime ),
   rdb.Column( "birth_country", rdb.Unicode ),
   rdb.Column( "date_of_death", rdb.DateTime ),
   rdb.Column( "national_id", rdb.Unicode(32) ),
   rdb.Column( "password", rdb.String(24)),    
   rdb.Column( "salt", rdb.String(24)),    
   rdb.Column( "active_p", rdb.Boolean ),
   rdb.Column( "type", rdb.String(30), nullable=False )
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
   rdb.Column( "member_id", rdb.Integer, rdb.ForeignKey('users.user_id'), primary_key=True ),
   # this is only meant as a shortcut.. to the active parliament, else use group memberships
   rdb.Column( "parliaments.parliament_id", rdb.Integer, rdb.ForeignKey('parliaments.parliament_id') ),
   rdb.Column( "constituency_id", rdb.Integer, rdb.ForeignKey('constituencies.constituency_id') ),
   rdb.Column( "start_date", rdb.DateTime, nullable=False ),
   rdb.Column( "end_date", rdb.DateTime ),
   rdb.Column( "leave_reason", rdb.Unicode ),
   rdb.Column( "active_p", rdb.Boolean ), 
   # XXX - TODO 
   # substitutions 

   )   

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
   rdb.Column( "constituency_id", rdb.Integer, primary_key=True ),
   rdb.Column( "constituency_identifier", rdb.Unicode(16), nullable=False ),
   rdb.Column( "name", rdb.Unicode(80), nullable=False ),
   #rdb.Column( "province", rdb.Unicode ),
   rdb.Column( "province", rdb.Integer, rdb.ForeignKey('provinces.province_id') ),
   #rdb.Column( "region", rdb.Unicode ),
   rdb.Column( "region", rdb.Integer, rdb.ForeignKey('regions.region_id') ),
   rdb.Column( "start_date", rdb.DateTime, nullable=False ),
   rdb.Column( "end_date", rdb.DateTime ),   
   )
#constituency_changes = make_changes_table( constituencies, metadata )
#constituency_version = make_versions_table( constituencies, metadata )

provinces = rdb.Table(
    "provinces",
    metadata,
    rdb.Column( "province_id", rdb.Integer, primary_key=True ),
    rdb.Column( "province", rdb.Unicode(80), nullable=False ),
    )
    
regions = rdb.Table(
    "regions",
    metadata,
    rdb.Column( "region_id", rdb.Integer, primary_key=True ),
    rdb.Column( "region", rdb.Unicode(80), nullable=False ),    
    )
    
constituency_details = rdb.Table(
    "constituency_details",
    metadata,
    rdb.Column( "constituency_detail_id", rdb.Integer, primary_key=True ),
    rdb.Column( "constituency_id", rdb.Integer, rdb.ForeignKey('constituencies.constituency_id') ),
    rdb.Column( "date", rdb.DateTime, nullable=False ),
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
   rdb.Column( "group_id", rdb.Integer, primary_key=True ),
   rdb.Column( "short_name", rdb.Unicode(16) ),
   rdb.Column( "full_name", rdb.Unicode(16) ),   
   rdb.Column( "description", rdb.Unicode ),
   rdb.Column( "status", rdb.Unicode(12) ), # workflow for groups
   rdb.Column( "start_date", rdb.DateTime, nullable=False ),
   rdb.Column( "end_date", rdb.DateTime ),  #
   rdb.Column( "type", rdb.String(30), nullable=False)
   )

governments = rdb.Table(
   "government_id",
   metadata,
   rdb.Column( "government_id", rdb.Integer, rdb.ForeignKey('groups.group_id'), primary_key=True ),
   rdb.Column( "start_gazetted_date", rdb.DateTime  ),
   rdb.Column( "end_gazetted_date", rdb.DateTime ),
   )

parliaments = rdb.Table(
   "parliaments",
   metadata,
   rdb.Column( "parliament_id", rdb.Integer, rdb.ForeignKey('groups.group_id'), primary_key=True ),   
   rdb.Column( "identifier", rdb.String(5) ),
   rdb.Column( "election_date", rdb.DateTime ),
   )

ministries = rdb.Table(
   "ministries",
   metadata,
   rdb.Column( "ministry_id", rdb.Integer, rdb.ForeignKey('groups.group_id'), primary_key=True ),
   )

committees = rdb.Table(
   "committees",
   metadata,
   rdb.Column( "commitee_id", rdb.Integer, rdb.ForeignKey('groups.group_id'), primary_key=True ),
   )

political_parties = rdb.Table(
   "political_parties",
   metadata,
   rdb.Column( "party_id", rdb.Integer, rdb.ForeignKey('groups.group_id'), primary_key=True ),   
   )


#
# group memberships encompasses any user participation in a group, including
# substitutions.

user_group_memberships = rdb.Table(
   "user_group_memberships",
   metadata,
   rdb.Column( "membership_id", rdb.Integer, primary_key=True),
   rdb.Column( "user_id", rdb.Integer, rdb.ForeignKey( 'users.user_id')),
   rdb.Column( "group_id", rdb.Integer, rdb.ForeignKey( 'groups.group_id')),
   rdb.Column( "title", rdb.Unicode(16)), # title of user's group role
   rdb.Column( "start_date", rdb.DateTime, default=rdb.PassiveDefault('now') ),
   rdb.Column( "end_date", rdb.DateTime ),
   rdb.Column( "notes", rdb.Unicode ),
   rdb.Column( "substitution_p", rdb.Boolean, default=False ),
   # we use this as an easier query to end_date in queries, needs to be set by
   # a cron process against end_date < current_time
   rdb.Column( "active_p", rdb.Boolean, default=False ),
   # these fields are only present when a membership is a result of substitution   
   rdb.Column( "replaced_id", rdb.Integer, rdb.ForeignKey('users.user_id') ),
   rdb.Column( "substitution_type", rdb.Unicode(100) ),
   )
  
# a bill assigned to a committee, a question assigned to a ministry
group_item_assignments = rdb.Table(
   "group_assignments",
   metadata,
   rdb.Column( "assignment_id", rdb.Integer, primary_key=True ),
   rdb.Column( "object_id", rdb.Integer ), # any object placed here needs to have a class hierarchy sequence
   rdb.Column( "group_id", rdb.Integer, rdb.ForeignKey('groups.group_id') ),
   rdb.Column( "title", rdb.Unicode(16)), # title of user's group role
   rdb.Column( "start_date", rdb.DateTime, default=rdb.PassiveDefault('now') ),
   rdb.Column( "end_date", rdb.DateTime ),   
   rdb.Column( "due_date", rdb.DateTime ),    
   rdb.Column( "notes", rdb.Unicode ),
   )

##################
# Activity 
# 
parliament_sessions = rdb.Table(
   "sessions",
   metadata,
   rdb.Column( "session_id", rdb.Integer, primary_key=True ),
   rdb.Column( "parliament_id", rdb.Integer, rdb.ForeignKey('parliaments.parliament_id'), unique=True),
   rdb.Column( "short_name", rdb.Unicode(16) ),
   rdb.Column( "full_name", rdb.Unicode(16) ),      
   rdb.Column( "start_date", rdb.DateTime),
   rdb.Column( "end_date", rdb.DateTime),
   rdb.Column( "notes", rdb.Unicode )   
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
   rdb.Column( "sitting_id", rdb.Integer, primary_key=True ),
   rdb.Column( "group_id", rdb.Integer, rdb.ForeignKey('groups.group_id') ),
   rdb.Column( "session_id", rdb.Integer, rdb.ForeignKey('sessions.session_id')),
   rdb.Column( "start_date", rdb.DateTime),
   rdb.Column( "end_date", rdb.DateTime),   
   )   

sitting_schedule = rdb.Table(
   "sitting_schedule",
   metadata,
   rdb.Column( "sitting_id", rdb.Integer, rdb.ForeignKey('group_sittings.sitting_id')),
   rdb.Column( "item_id",  rdb.Integer, nullable=False),   
   rdb.Column( "item_type", rdb.Unicode ),
   rdb.Column( "order", rdb.Integer ),
   )
   
sitting_attendance = rdb.Table(
   "sitting_attendance",
   metadata,
   rdb.Column( "sitting_id", rdb.Integer, rdb.ForeignKey('group_sittings.sitting_id') ),
   rdb.Column( "member_id",  rdb.Integer, rdb.ForeignKey('users.user_id') ),
   )
# 

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
            rdb.Column( "date", rdb.DateTime, default=rdb.PassiveDefault('now') ),
            rdb.Column( "description", rdb.Unicode),
            rdb.Column( "notes", rdb.Unicode),
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
    
ItemSequence = rdb.Sequence('item_sequence')

item_votes = rdb.Table( 
   'item_votes',
   metadata,
   rdb.Column( "vote_id", rdb.Integer, primary_key=True ),
   rdb.Column( "item_id", rdb.Integer, nullable=False ),
   rdb.Column( "date", rdb.DateTime ),
#   rdb.Column( "division_p",  rdb.Boolean ), # isn't a division implied by the vote?
   rdb.Column( "affirmative_votes", rdb.Integer),
   rdb.Column( "negative_votes", rdb.Integer ),
   rdb.Column( "remarks", rdb.Unicode  ),   
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
   rdb.Column( "object_type", rdb.Unicode, nullable=False ),
   rdb.Column( "party_id",  rdb.Integer, nullable=False ),
   rdb.Column( "party_type", rdb.Unicode, nullable=False ),
   rdb.Column( "last_delivery", rdb.DateTime, nullable=False ),   
   # delivery period
   # rdb.Column( "delivery_period",  rdb.Integer ),
   # delivery type
   # rdb.Column( "delivery_type", rdb.Integer ),
   )



questions = rdb.Table(
   "questions",
   metadata,
   rdb.Column( "question_id", rdb.Integer, ItemSequence, primary_key=True ),
   #   rdb.Column( "parliament_id", rdb.Integer, rdb.ForeignKey('parliaments.parliament_id') ),
   rdb.Column( "session_id", rdb.Integer, rdb.ForeignKey('sessions.session_id')),
   rdb.Column( "clerk_submission_date", rdb.DateTime ),
   rdb.Column( "question_type", rdb.Unicode(1), 
                rdb.CheckConstraint("question_type in ('O', 'P')"), default=u"O" ), # (O)rdinary (P)rivate Notice
   rdb.Column( "response_type", rdb.Unicode(1), 
                rdb.CheckConstraint("response_type in ('O', 'W')"), default=u"O" ), # (O)ral (W)ritten

   # TODO - ? normalize to use user item associations.
   rdb.Column( "owner", rdb.Integer, rdb.ForeignKey('parliament_members.member_id'), nullable=False),
   
   # Workflow State
   rdb.Column( "status", rdb.Unicode(16) ),
   
   # if this is a supplementary question, this is the original/previous question
   rdb.Column( "supplement_parent_id", rdb.Integer, rdb.ForeignKey('questions.question_id')  ),
     
   # after the question is scheduled
   rdb.Column( "sitting_id", rdb.Integer, rdb.ForeignKey('group_sittings.sitting_id')  ),
   rdb.Column( "sitting_time", rdb.DateTime )
   )


question_changes = make_changes_table( questions, metadata )
question_versions = make_versions_table( questions, metadata )

#print 'change', repr(question_changes.c.question_id)
#print 'version', repr(question_versions.c.question_id)


responses = rdb.Table(
   "responses",
   metadata,
   rdb.Column( "response_id", rdb.Integer, primary_key=True ),
   rdb.Column( "question_id", rdb.Integer, rdb.ForeignKey('questions.question_id') ),
   rdb.Column( "response_text", rdb.Unicode ),
   rdb.Column( "type", rdb.Unicode, rdb.CheckConstraint("type in ('I','S')"), default=u"I"), # (I)nitial (S)ubsequent
   rdb.Column( "sitting_id", rdb.Integer, rdb.ForeignKey('group_sittings.sitting_id') ),
   rdb.Column( "sitting_time", rdb.DateTime )
   )

motions = rdb.Table(
   "motions",
   metadata,
   rdb.Column( "motion_id", rdb.Integer, ItemSequence, primary_key=True ),
   rdb.Column( "session_id", rdb.Integer, rdb.ForeignKey('sessions.session_id')),
   rdb.Column( "submission_date", rdb.DateTime ),
   rdb.Column( "public", rdb.Boolean ),
   rdb.Column( "title", rdb.Unicode ),
   rdb.Column( "identifier", rdb.Integer),
   rdb.Column( "owner_id", rdb.Integer, rdb.ForeignKey('users.user_id') ),
   rdb.Column( "body_text", rdb.Unicode ),
   rdb.Column( "received_date", rdb.DateTime ),
   rdb.Column( "entered_by", rdb.Integer, rdb.ForeignKey('users.user_id') ),   
   rdb.Column( "party_id", rdb.Integer, rdb.ForeignKey('political_parties.party_id')  ), # if the motion was sponsored by a party
   rdb.Column( "notice_date", rdb.DateTime ),
   rdb.Column( "status",  rdb.Unicode(12) ),
   )

motion_changes = make_changes_table( motions, metadata )
motion_versions = make_versions_table( motions, metadata )

motion_amendments = rdb.Table(
   "motion_amendments",
   metadata,
   rdb.Column( "amendment_id", rdb.Integer, primary_key=True ),
   rdb.Column( "motion_id", rdb.Integer, rdb.ForeignKey('motions.motion_id')  ),
   rdb.Column( "amended_id", rdb.Integer,  ),
   rdb.Column( "body_text", rdb.Unicode ),  
   rdb.Column( "submission_date", rdb.DateTime ),    
   rdb.Column( "accepted_p", rdb.Boolean ),
   rdb.Column( "title", rdb.Unicode ), 
   rdb.Column( "vote_date", rdb.DateTime ),   
   )

bills = rdb.Table(
   "bills",
   metadata,
   rdb.Column( "bill_id", rdb.Integer, ItemSequence, primary_key=True ),
   rdb.Column( "ministry_id", rdb.Integer, rdb.ForeignKey('groups.group_id') ),
   rdb.Column( "identifier",  rdb.Integer),
   rdb.Column( "preamble", rdb.Unicode ),   
   rdb.Column( "title", rdb.Unicode ), 
   rdb.Column( "body_text",  rdb.Unicode ),
   rdb.Column( "submission_date", rdb.DateTime ),
   rdb.Column( "publication_date", rdb.DateTime ),
   rdb.Column( "status", rdb.Unicode(12) ),
   )
   
bill_changes = make_changes_table( bills, metadata )
bill_versions = make_versions_table( bills, metadata )

committee_reports = ()
debates = ()




#######################
# Hansard
#######################   

rotas = rdb.Table(
   "rotas",
   metadata,
   rdb.Column( "rota_id", rdb.Integer, primary_key=True ),
   rdb.Column( "reporter_id", rdb.Integer, rdb.ForeignKey('users.user_id') ),
   rdb.Column( "identifier", rdb.Unicode ),
   rdb.Column( "start_date", rdb.DateTime ),
   rdb.Column( "end_date", rdb.DateTime )
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
    

