


import sqlalchemy as rdb
from sqlalchemy.orm import mapper, relation, column_property

import schema
import domain

# Users
mapper( domain.User, schema.users,
        polymorphic_on=schema.users.c.type,
        polymorphic_identity='user',
       )

mapper (domain.Keyword, schema.keywords)
# Groups
mapper( domain.Group, schema.groups,
        properties={
            'members': relation( domain.GroupMembership ),
#            'keywords': relation( domain.Keyword,  secondary=schema.groups_keywords,  )            
            },
        polymorphic_on=schema.groups.c.type,
        polymorphic_identity='group'
        )

# Keywords for groups
#mapper (domain.Keyword, schema.keywords,
#         properties = {
#                'groups': relation(domain.Group, secondary=schema.groups_keywords, backref='keywords'),
#                
#                   })


# do we really need a primary key on group memberships to map?

# we need to specify join clause for user explicitly because we have multiple fk
# to the user table.
mapper( domain.GroupMembership, schema.user_group_memberships,
        properties={
            'user': relation( domain.User,
                              primaryjoin=rdb.and_(schema.user_group_memberships.c.user_id==schema.users.c.user_id ),
                              lazy=False ),
            'group': relation( domain.Group,
                               primaryjoin=schema.user_group_memberships.c.group_id==schema.groups.c.group_id,
                               lazy=False ),                              
            'replaced': relation( domain.GroupMembership,
                                  primaryjoin=schema.user_group_memberships.c.replaced_id==schema.user_group_memberships.c.membership_id,
                                  lazy=True ),
                              
            }
        )

# how to make multiple properties over the same value set, not disjoint
#mapper( domain.User, schema.groups )

# group subclasses
mapper( domain.Government, schema.governments,
        inherits=domain.Group,                
        polymorphic_on=schema.groups.c.type,
        polymorphic_identity='government'
        )

mapper( domain.Parliament, schema.parliaments,
        inherits=domain.Group,                
        polymorphic_on=schema.groups.c.type,
        polymorphic_identity='parliament'
        )
        
mapper( domain.PoliticalParty, schema.political_parties,
        inherits=domain.Group,                        
        polymorphic_on=schema.groups.c.type,
        polymorphic_identity='political-party'
        )

mapper( domain.Ministry, schema.ministries,
        inherits=domain.Group,
        polymorphic_on=schema.groups.c.type,
        polymorphic_identity='ministry'
        )

mapper( domain.Committee, schema.committees,
        inherits=domain.Group,
        polymorphic_on=schema.groups.c.type,
        polymorphic_identity='committee'
        )    
        
mapper( domain.ExtensionGroup, schema.extension_groups,
        inherits=domain.Group,
        polymorphic_on=schema.groups.c.type,
        polymorphic_identity='extension'
        )                         



    
mapper( domain.ParliamentMember, 
        inherits=domain.User,
          properties={
           'fullname' : column_property(
                             (schema.users.c.first_name + u" " + 
                             schema.users.c.middle_name + u" " + 
                             schema.users.c.last_name).label('fullname')
                                           ),
           'short_name' : column_property(
                             (schema.users.c.last_name + u", " + 
                             #schema.users.c.middle_name + u" " +
                             schema.users.c.first_name).label('short_name')
                                           )
                    },
        polymorphic_identity='memberofparliament'
      )

# A parliament member is described by 
# membership in the parliament (group + parliament_id)
# plus the additional data in the parliament_members table.
#SELECT * FROM "user_group_memberships", "users", "groups", "parliaments", "parliament_members" 
#WHERE 
#( "user_group_memberships"."user_id" = "users"."user_id" 
#  AND "user_group_memberships"."group_id" = "groups"."group_id" 
#  AND "parliaments"."parliament_id" = "groups"."group_id" 
#  AND "parliament_members"."membership_id" = "user_group_memberships"."membership_id" )

#_mp = rdb.join(schema.user_group_memberships, schema.parliament_members, 
#               schema.user_group_memberships.c.membership_id == schema.parliament_members.c.membership_id).join( 
#                    schema.parliaments,
#                    schema.user_group_memberships.c.group_id == schema.parliaments.c.parliament_id )

_mp = rdb.join(schema.user_group_memberships, schema.parliament_members, 
                schema.user_group_memberships.c.membership_id == schema.parliament_members.c.membership_id)
                
mapper ( domain.MemberOfParliament , _mp,
         primary_key=[schema.user_group_memberships.c.membership_id], 
          properties={
            'short_name' : column_property(
                             rdb.sql.select(
                             [(schema.users.c.last_name + u", " + 
                             #schema.users.c.middle_name + u" " +
                             schema.users.c.first_name)],
                             schema.user_group_memberships.c.user_id==schema.users.c.user_id
                                    ).label('short_name')
                                           ),
#XXX useful to sort by  constituency ?                                          
#            'constituency' : column_property(
#                             rdb.sql.select(
#                             [schema.constituencies.c.name],
#                             schema.parliament_members.c.constituency_id==schema.constituencies.c.constituency_id
#                                    ).label('constituency')
#                                           ),
               
          }        
        )
        
# Ministers and Committee members are defined by their group membership in a 
# ministry or committee (group)        
mapper( domain.Minister, schema.user_group_memberships, 
            properties={
            'short_name' : column_property(
                             rdb.sql.select(
                             [(schema.users.c.first_name + u" " + 
                             #schema.users.c.middle_name + u" " +
                             schema.users.c.last_name)],
                             schema.user_group_memberships.c.user_id==schema.users.c.user_id
                                    ).label('short_name')
                                           )
          })
mapper( domain.CommitteeMember, schema.user_group_memberships ,
            properties={
            'short_name' : column_property(
                             rdb.sql.select(
                             [(schema.users.c.last_name + u", " + 
                             #schema.users.c.middle_name + u" " +
                             schema.users.c.first_name)],
                             schema.user_group_memberships.c.user_id==schema.users.c.user_id
                                    ).label('short_name')
                                           )
          })
mapper( domain.ExtensionMember, schema.user_group_memberships, 
            properties={
            'short_name' : column_property(
                             rdb.sql.select(
                             [(schema.users.c.last_name + u", " + 
                             #schema.users.c.middle_name + u" " +
                             schema.users.c.first_name)],
                             schema.user_group_memberships.c.user_id==schema.users.c.user_id
                                    ).label('short_name')
                                           )
          })
mapper( domain.PartyMember, schema.user_group_memberships, 
            properties={
            'short_name' : column_property(
                             rdb.sql.select(
                             [(schema.users.c.last_name + u", " + 
                             #schema.users.c.middle_name + u" " +
                             schema.users.c.first_name)],
                             schema.user_group_memberships.c.user_id==schema.users.c.user_id
                                    ).label('short_name')
                                           )
          })


mapper( domain.HansardReporter, schema.reporters,
        inherits=domain.User,
        polymorphic_identity='reporter')


mapper( domain.ParliamentSession, schema.parliament_sessions )
mapper( domain.GroupSitting, schema.sittings )


##############################
# Parliamentary Items

mapper( domain.QuestionChange, schema.question_changes )
mapper( domain.QuestionVersion, schema.question_versions,
        properties= {'change':relation( domain.QuestionChange, uselist=False ) }
        )
mapper( domain.Question, schema.questions,
        properties = {
             'versions':relation( domain.QuestionVersion, backref='question'),
             'changes':relation( domain.QuestionChange, backref='question')
             }
        )

mapper( domain.Response, schema.responses)

mapper( domain.MotionChange, schema.motion_changes )
mapper( domain.MotionVersion, schema.motion_versions,
        properties= {'change':relation( domain.MotionChange, uselist=False)}
        )
mapper( domain.Motion, schema.motions,
        properties = {
             'versions':relation( domain.MotionVersion, backref='motion'),
             'changes':relation( domain.MotionChange, backref='motion'),
             'session':relation( domain.ParliamentSession )
             }
        )

mapper( domain.MotionAmendment, schema.motion_amendments)

mapper( domain.BillChange, schema.bill_changes )
mapper( domain.BillVersion, schema.bill_versions, 
        properties= {'change':relation( domain.BillChange, uselist=False)}
        )
mapper( domain.Bill, schema.bills,
        properties = {
             'versions':relation( domain.BillVersion, backref='bill'),
             'changes':relation( domain.BillChange, backref='bill')
             }
        )
######################
#

#mapper( domain.ConstituencyChange, schema.constituency_changes )
#mapper( domain.ConstituencyVersion, schema.constituency_version )
#mapper( domain.Constituency, schema.constituencies, 
#		properties = {
#			'versions':relation( domain.ConstituencyVersion, backref='Constituency' ),
#			'changes':relation( domain.ConstituencyChange, backref='Constituency')
#			}
#		)         

mapper( domain.Constituency, schema.constituencies )    
mapper( domain.Province, schema.provinces )    
mapper( domain.Region, schema.regions )
mapper( domain.Country, schema.countries )
mapper( domain.ConstituencyDetail, schema.constituency_details )
mapper( domain.CommitteeType, schema.committee_type )   
mapper( domain.SittingType, schema.sitting_type )     
mapper( domain.GroupSittingAttendance, schema.sitting_attendance,
        properties={
            'short_name' : column_property(
                             rdb.sql.select(
                             [(schema.users.c.last_name + u", " + 
                             #schema.users.c.middle_name + u" " +
                             schema.users.c.first_name)],
                             schema.sitting_attendance.c.member_id==schema.users.c.user_id
                                    ).distinct().label('short_name')
                                           )
                  }
         )
mapper( domain.AttendanceType, schema.attendance_type )
mapper( domain.MemberTitle, schema.user_role_type )


        

    
