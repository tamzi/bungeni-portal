
import sqlalchemy as rdb
from sqlalchemy.orm import mapper, relation, column_property, deferred, backref

import schema
import domain

# Users
# general representation of a person
mapper( domain.User, schema.users,         
       )

mapper (domain.Keyword, schema.keywords)

# Groups
mapper( domain.Group, schema.groups,
        primary_key=[schema.groups.c.group_id],
        properties={
            'members': relation( domain.GroupMembership ),
            'group_principal_id': column_property(
                ("group." + schema.groups.c.type + "." + 
                rdb.cast(schema.groups.c.group_id, rdb.String)
                ).label('group_principal_id')),
             'contained_groups' : relation( domain.Group, 
                    backref =  
                    backref('parent_group',  
                    remote_side=schema.groups.c.group_id)
                    ),                            
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

# delegate rights to act on behalf of a user
mapper (domain.UserDelegation, schema.user_delegations, 
        properties={
            'user': relation( domain.User,
                        primaryjoin=rdb.and_(
                            schema.user_delegations.c.user_id==
                            schema.users.c.user_id ),
                      uselist=False,
                      lazy=True ),  
            'delegation': relation( domain.User,
                        primaryjoin=rdb.and_(
                            schema.user_delegations.c.delegation_id==
                            schema.users.c.user_id,
                            schema.users.c.active_p=='A'
                             ),
                      uselist=False,
                      lazy=True ),                                                        
                }                      
        )
# group subclasses
mapper( domain.Government,
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

mapper( domain.Ministry,
        inherits=domain.Group,
        polymorphic_on=schema.groups.c.type,
        polymorphic_identity='ministry'
        )

mapper( domain.Committee, schema.committees,
        inherits=domain.Group,
        polymorphic_on=schema.groups.c.type,
        polymorphic_identity='committee',
        properties={
            'committee_type': relation( domain.CommitteeType,
                              uselist=False,
                              lazy=False ),
            },                                      
        )    
        

mapper( domain.Office, schema.offices,
        inherits=domain.Group,
        polymorphic_on=schema.groups.c.type,
        polymorphic_identity='office'
        )   

   

                

# Ministers and Committee members are defined by their group membership in a 
# ministry or committee (group)     

# we need to specify join clause for user explicitly because we have multiple fk
# to the user table.
mapper( domain.GroupMembership, schema.user_group_memberships,
        properties={
            'user': relation( domain.User,
                              primaryjoin=rdb.and_(
                              schema.user_group_memberships.c.user_id==
                              schema.users.c.user_id ),
                              uselist=False,
                              lazy=False ),
            'group': relation( domain.Group,
                               primaryjoin=
                               schema.user_group_memberships.c.group_id==
                               schema.groups.c.group_id,
                               uselist=False,
                               lazy=True ),                              
            'replaced': relation( domain.GroupMembership,
                                  primaryjoin=
                                  schema.user_group_memberships.c.replaced_id==
                                  schema.user_group_memberships.c.membership_id,
                                  uselist=False,
                                  lazy=True ),
            'member_titles': relation( domain.MemberRoleTitle ) 
            },
        polymorphic_on=schema.user_group_memberships.c.membership_type,          
        polymorphic_identity='member',            
        )



mapper ( domain.MemberOfParliament , 
        schema.parliament_memberships,
         inherits=domain.GroupMembership,
         primary_key=[schema.user_group_memberships.c.membership_id], 
          properties={
            'constituency': relation( domain.Constituency,
                                primaryjoin=(
                                schema.parliament_memberships.c.constituency_id==
                                schema.constituencies.c.constituency_id),
                              uselist=False,
                              lazy=False ),
            'constituency_id':[schema.parliament_memberships.c.constituency_id], 
            'start_date' :  column_property(schema.user_group_memberships.c.start_date.label('start_date')), 
            'end_date' :  column_property(schema.user_group_memberships.c.end_date.label('end_date')),
               
          },      
        polymorphic_on=schema.user_group_memberships.c.membership_type,          
        polymorphic_identity='parliamentmember'  
        )
        
   
mapper( domain.Minister, 
        inherits=domain.GroupMembership,
        polymorphic_on=schema.user_group_memberships.c.membership_type,          
        polymorphic_identity='minister',        
        )        
 
mapper( domain.CommitteeMember, 
        inherits=domain.GroupMembership,
        polymorphic_on=schema.user_group_memberships.c.membership_type,          
        polymorphic_identity='committeemember',                
        )  
                
mapper( domain.PartyMember, 
        inherits=domain.GroupMembership,
        polymorphic_on=schema.user_group_memberships.c.membership_type,          
        polymorphic_identity='partymember',        
        )  
                
mapper( domain.OfficeMember, 
        inherits=domain.GroupMembership,
        polymorphic_on=schema.user_group_memberships.c.membership_type,          
        polymorphic_identity='officemember',        
        )  
                                         
 
                
# staff assigned to a group (committee, ...)


mapper( domain.CommitteeStaff,
        inherits=domain.GroupMembership,
        polymorphic_on=schema.user_group_memberships.c.membership_type,          
        polymorphic_identity='committeestaff',        
        )

                
mapper( domain.ParliamentSession, schema.parliament_sessions )
mapper( domain.GroupSitting, schema.sittings,
        properties = {
            'sitting_type': relation(
                domain.SittingType, uselist=False),
            'group': relation( domain.Group,
                               primaryjoin=schema.sittings.c.group_id==schema.groups.c.group_id,
                               uselist=False,
                               lazy=True ),  
            'start_date' :  column_property(schema.sittings.c.start_date.label('start_date')), 
            'end_date' :  column_property(schema.sittings.c.end_date.label('end_date')), 
            'item_schedule' : relation(domain.ItemSchedule, order_by=schema.items_schedule.c.planned_order),                                            
            })

mapper( domain.ResourceType, schema.resource_types )
mapper( domain.Resource, schema.resources )
mapper( domain.ResourceBooking, schema.resourcebookings)

mapper( domain.Venue, schema.venues )

##############################
# Parliamentary Items

mapper( domain.ParliamentaryItem, schema.parliamentary_items,
        polymorphic_on=schema.parliamentary_items.c.type,
        polymorphic_identity='item', 
        properties = {          
                    'owner': relation( domain.User,
                              primaryjoin=rdb.and_(schema.parliamentary_items.c.owner_id==schema.users.c.user_id ),
                              uselist=False,
                              lazy=False ),
                }
         )


mapper( domain.Question, schema.questions,
        inherits=domain.ParliamentaryItem,
        polymorphic_on=schema.parliamentary_items.c.type,
        polymorphic_identity='question',
        properties = {
             'changes':relation( domain.QuestionChange, backref='origin'),  
             'ministry': relation( domain.Ministry),
             }
        )
        
mapper( domain.QuestionChange, schema.question_changes )
mapper( domain.QuestionVersion, schema.question_versions,
        properties= {'change': relation( domain.QuestionChange, uselist=False),
                     'head': relation( domain.Question, uselist=False)}
        )




mapper( domain.Motion, schema.motions,
        inherits=domain.ParliamentaryItem,
        polymorphic_on=schema.parliamentary_items.c.type,
        polymorphic_identity='motion',
        properties = {
             'changes':relation( domain.MotionChange, backref='origin'),
             }
        )
        
mapper( domain.MotionChange, schema.motion_changes )
mapper( domain.MotionVersion, schema.motion_versions,
        properties= {'change':relation( domain.MotionChange, uselist=False),
                     'head': relation( domain.Motion, uselist=False)}
        )

        
mapper( domain.Bill, schema.bills,
        inherits=domain.ParliamentaryItem,
        polymorphic_on=schema.parliamentary_items.c.type,
        polymorphic_identity='bill',
        properties = {
             'changes':relation( domain.BillChange, backref='origin')
             }
        )
mapper( domain.BillChange, schema.bill_changes )
mapper( domain.BillVersion, schema.bill_versions, 
        properties= {'change':relation( domain.BillChange, uselist=False),
                     'head': relation( domain.Bill, uselist=False)}
        )


mapper( domain.EventItem, schema.event_items, 
        inherits=domain.ParliamentaryItem,
        inherit_condition=(
                    schema.event_items.c.event_item_id == 
                    schema.parliamentary_items.c.parliamentary_item_id),
        polymorphic_on=schema.parliamentary_items.c.type,
        polymorphic_identity='event')

mapper( domain.AgendaItem, schema.agenda_items, 
        inherits=domain.ParliamentaryItem,
        polymorphic_on=schema.parliamentary_items.c.type,
        polymorphic_identity='agendaitem',
        properties = {
             'changes' : relation( domain.AgendaItemChange, backref='origin'),
             'group' : relation(domain.Group, 
                primaryjoin=(schema.agenda_items.c.group_id==schema.groups.c.group_id ),
                backref = 'agenda_items',
                lazy = False,
                uselist=False,)
             })
mapper( domain.AgendaItemChange, schema.agenda_item_changes )  
mapper( domain.AgendaItemVersion, schema.agenda_item_versions,
        properties= {'change':relation( domain.AgendaItemChange, uselist=False),
                     'head': relation( domain.AgendaItem, uselist=False)}
        )
              
mapper( domain.TabledDocument, schema.tabled_documents,
        inherits=domain.ParliamentaryItem,
        polymorphic_on=schema.parliamentary_items.c.type,
        polymorphic_identity='tableddocument',
        properties = {
             'changes':relation( domain.TabledDocumentChange, backref='origin'),
             } )
mapper( domain.TabledDocumentChange, schema.tabled_document_changes )
mapper( domain.TabledDocumentVersion, schema.tabled_document_versions,
        properties= {'change':relation( domain.TabledDocumentChange, uselist=False),
                     'head': relation( domain.TabledDocument, uselist=False)}
        )



#Items scheduled for a sitting expressed as a relation
# to their item schedule
        
mapper(domain.ItemSchedule, schema.items_schedule,
       properties = {
           'item': relation(
               domain.ParliamentaryItem,
               uselist=False),
           'discussion': relation(
               domain.ScheduledItemDiscussion,
               uselist=False,
               cascade='all, delete-orphan'),
           'category': relation( domain.ItemScheduleCategory, uselist=False),    
           'sitting' : relation( domain.GroupSitting, uselist=False),     
           }
       ) 

mapper(domain.ScheduledItemDiscussion, schema.item_discussion)

mapper( domain.ItemScheduleCategory , schema.item_schedule_category)

# items scheduled for a sitting
# expressed as a join between item and schedule


       
mapper( domain.Consignatory, schema.consignatories,
        properties= {'item': relation(domain.ParliamentaryItem, uselist=False),
                      'user': relation(domain.User, uselist=False)})
#mapper( domain.Debate, schema.debates )

mapper( domain.MotionAmendment, schema.motion_amendments)

mapper( domain.BillType, schema.bill_types )        
#mapper( domain.DocumentSource, schema.document_sources )
#


mapper( domain.HoliDay, schema.holidays )
        
######################
#
    

mapper( domain.Constituency, schema.constituencies,
        properties={
        'province': relation( domain.Province,
                              uselist=False,
                              lazy=False ),
        'region': relation( domain.Region,
                              uselist=False,
                              lazy=False ),                              
        }
    )    
mapper( domain.Province, schema.provinces )    
mapper( domain.Region, schema.regions )
mapper( domain.Country, schema.countries )
mapper( domain.ConstituencyDetail, schema.constituency_details,
    properties={
    'constituency': relation( domain.Constituency,
                              uselist=False,
                              lazy=True,
                              backref = 'details' ),
    } )
mapper( domain.CommitteeType, schema.committee_type )   
mapper( domain.SittingType, schema.sitting_type )     
mapper( domain.GroupSittingAttendance, schema.sitting_attendance,
        properties={
            'user': relation( domain.User,
                              uselist=False,
                              lazy=False ),
            'attendance_type': relation( domain.AttendanceType,
                                uselist = False,
                                lazy = False ),                              
                  }
         )
mapper( domain.AttendanceType, schema.attendance_type )
mapper( domain.MemberTitle, schema.user_role_types )
mapper( domain.MemberRoleTitle, schema.role_titles.join(schema.addresses),
    properties={
        'title_name': relation( domain.MemberTitle,
                              uselist=False,
                              lazy=False ),
    }                              
)

mapper( domain.AddressType, schema.address_types )
mapper( domain.UserAddress, schema.addresses)

mapper(domain.GroupItemAssignment, schema.group_item_assignments,
        properties={             
            'group': relation(domain.Group, 
                primaryjoin=(schema.group_item_assignments.c.group_id==schema.groups.c.group_id ),
                backref = 'group_assignments',
                lazy = True,
                uselist=False,),
            'item': relation(
               domain.ParliamentaryItem,
                backref = 'item_assignments',               
               uselist=False),                            
        }
        )             
mapper(domain.ItemGroupItemAssignment, schema.group_item_assignments,
        inherits=domain.GroupItemAssignment,)
        
mapper(domain.GroupGroupItemAssignment, schema.group_item_assignments,
        inherits=domain.GroupItemAssignment)        
        
mapper(domain.Report, schema.reports,
        properties={             
            'group': relation(domain.Group, 
                primaryjoin=(schema.reports.c.group_id == schema.groups.c.group_id ),
                backref = 'reports',
                lazy = True,
                uselist=False,),}

)        
