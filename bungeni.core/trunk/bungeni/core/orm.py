


import sqlalchemy as rdb
from sqlalchemy.orm import mapper, relation

import schema
import domain

# Users
mapper( domain.User, schema.users,
        polymorphic_on=schema.users.c.type,
        polymorphic_identity='user')

# Groups
mapper( domain.Group, schema.groups,
        properties={
            'members': relation( domain.GroupMembership, backref='group' )
            },
        polymorphic_on=schema.groups.c.type,
        polymorphic_identity='group'
        )

# do we really need a primary key on group memberships to map?

# we need to specify join clause for user explicitly because we have multiple fk
# to the user table.
mapper( domain.GroupMembership, schema.user_group_memberships,
        properties={
            'user': relation( domain.User,
                              primaryjoin=rdb.and_(schema.user_group_memberships.c.user_id==schema.users.c.user_id, 
                                                   schema.user_group_memberships.c.group_id==schema.groups.c.group_id ),
                              lazy=False ),
#            'group': relation( domain.Group,
#                               primaryjoin=schema.user_group_memberships.c.user_id==schema.users.c.user_id,
#                               lazy=False ),                              
            'replaced': relation( domain.User,
                                  primaryjoin=schema.user_group_memberships.c.replaced_id==schema.users.c.user_id,
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


mapper( domain.ParliamentMember, schema.parliament_members,
        inherits=domain.User,
        polymorphic_identity='memberofparliament')

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
mapper( domain.ConstituencyDetail, schema.constituency_details )
        

        

    
