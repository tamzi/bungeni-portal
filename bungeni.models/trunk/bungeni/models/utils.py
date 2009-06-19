#!/usr/bin/env python
# encoding: utf-8

from zope.security.management import getInteraction
from zope.publisher.interfaces import IRequest
from ore.alchemist import Session
import sqlalchemy as rdb
from sqlalchemy.orm import eagerload
import domain, schema

def getUserId( ):
    interaction = getInteraction()
    for participation in interaction.participations:
        if IRequest.providedBy(participation):
            return participation.principal.id

def get_db_user_id():
    """ get the (numerical) user_id for the logged in user    
    """
    userId = getUserId()
    session = Session()
    query = session.query(domain.User).filter(
                    domain.User.login == userId)
    results = query.all()
    if len(results) == 1:
        return results[0].user_id                    


def get_all_group_ids_in_parliament(parliament_id):
    """ get all groups (group_ids) in a parliament
    including the sub (e.g. ministries) groups """
    session = Session()
    group_ids = [parliament_id,]
    query = session.query(domain.Group).filter(
        domain.Group.parent_group_id == parliament_id).options(
            eagerload('contained_groups'))                                        
    results = query.all()
    for result in results:
        group_ids.append(result.group_id)
        for group in result.contained_groups:
            group_ids.append(group.group_id)                     
    return group_ids
    
    

def get_offices_held_for_user_in_parliament(user_id, parliament_id):
    """ get the Offices (functions/titles) held by a user in a parliament """
    session = Session()
    connection = session.connection(domain.Group)
    group_ids = get_all_group_ids_in_parliament(parliament_id)
    offices_held = rdb.select([schema.groups.c.short_name,
        schema.groups.c.type,
        schema.role_titles.c.start_date,
        schema.role_titles.c.end_date,
        schema.user_role_types.c.user_role_name], 
        from_obj=[   
        rdb.join(schema.groups, schema.user_group_memberships,
        schema.groups.c.group_id == schema.user_group_memberships.c.group_id).join(
            schema.role_titles, schema.user_group_memberships.c.membership_id ==
            schema.role_titles.c.membership_id).join(schema.user_role_types,
            schema.role_titles.c.title_name_id ==
            schema.user_role_types.c.user_role_type_id)],
            whereclause =
            rdb.and_(
                schema.groups.c.group_id.in_(group_ids),
                schema.user_group_memberships.c.user_id == user_id)                
            )
    return connection.execute(offices_held)           
            
    



        
        
        
