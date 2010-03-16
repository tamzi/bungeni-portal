#!/usr/bin/env python
# encoding: utf-8

from zope import component
from zope.securitypolicy.interfaces import IPrincipalRoleMap
from zope.securitypolicy.settings import Allow, Deny
from zope.security.management import getInteraction
from zope.publisher.interfaces import IRequest
from ore.alchemist import Session
import sqlalchemy as rdb
from sqlalchemy.orm import eagerload, lazyload
import domain, schema


def get_principal():
    """ () -> either(IPrincipal, None)
    """
    interaction = getInteraction()
    for participation in interaction.participations:
        if IRequest.providedBy(participation):
            return participation.principal
    
def get_principal_id():
    """ () -> either(str, None)
    """
    principal = get_principal()
    if principal is not None:
        return principal.id


def get_db_user(context=None):
    """ get the logged in user 
    Note: context is not used, but accommodated for as a dummy optional input 
    parameter to allow usage of this utility in e.g.
    bungeni.core.apps.py: container_getter(get_db_user, 'questions')
    """
    principal_id = get_principal_id()
    session = Session()
    query = session.query(domain.User).filter(domain.User.login==principal_id)
    results = query.all()
    #session.close
    if len(results)==1:
        return results[0]

def get_db_user_id():
    """ get the (numerical) user_id for the currently logged in user
    """
    db_user = get_db_user()
    if db_user is not None:
        return db_user.user_id


def get_roles(context):
    #return [role_id for role_id, role in \
    #        component.getUtilitiesFor(IRole, context)]
    # eeks we have to loop through all groups of the
    # principal and all PrincipalRoleMaps to get all roles
    #
    prms = []
    def _build_principal_role_maps(ctx):
        if ctx is not None:
            if component.queryAdapter(ctx, IPrincipalRoleMap):  
                prms.append(IPrincipalRoleMap(ctx))
            _build_principal_role_maps(getattr(ctx,'__parent__', None))
    _build_principal_role_maps(context)
    prms.reverse()
    #
    def add_roles(principal, prms, roles):
        for prm in prms:
            l_roles = prm.getRolesForPrincipal(principal)
            for role in l_roles:
                if role[1] == Allow:
                    if not(role[0] in roles):
                        roles.append(role[0])
                elif role[1] == Deny:
                    if role[0] in roles:
                        roles.remove(role[0])
        return roles
    principal = get_principal()
    pg = principal.groups.keys()
    roles = []
    for pn in pg:
        roles = add_roles(pn, prms, roles)
    pn = principal.id
    roles = add_roles(pn, prms, roles)
    return roles


def get_all_group_ids_in_parliament(parliament_id):
    """ get all groups (group_ids) in a parliament
    including the sub (e.g. ministries) groups """
    session = Session()
    group_ids = [parliament_id,]
    query = session.query(domain.Group).filter(
        domain.Group.parent_group_id == parliament_id).options(
            eagerload('contained_groups'), 
            )
    results = query.all()
    for result in results:
        group_ids.append(result.group_id)
        for group in result.contained_groups:
            group_ids.append(group.group_id)
    #session.close              
    return group_ids
    
    
def get_ministry_ids_for_user_in_government(user_id, government_id):
    """ get the ministries where user_id is a active member """
    session = Session()
    connection = session.connection(domain.Group)
    ministries = rdb.select([schema.groups.c.group_id],
        from_obj=[
        rdb.join(schema.groups, schema.user_group_memberships,
        schema.groups.c.group_id == schema.user_group_memberships.c.group_id),
        ],
        whereclause =
            rdb.and_(
            schema.user_group_memberships.c.user_id==user_id,
            schema.groups.c.parent_group_id==government_id,
            schema.groups.c.status=='active',
            schema.user_group_memberships.c.active_p==True))
    ministry_ids = []
    for group_id in connection.execute(ministries):
        ministry_ids.append(group_id[0])
    #session.close
    return ministry_ids

def get_offices_held_for_user_in_parliament(user_id, parliament_id):
    """ get the Offices (functions/titles) held by a user in a parliament """
    session = Session()
    connection = session.connection(domain.Group)
    group_ids = get_all_group_ids_in_parliament(parliament_id)
    offices_held = rdb.select([schema.groups.c.short_name,
        schema.groups.c.full_name,
        schema.groups.c.type,
        schema.user_role_types.c.user_role_name,
        schema.role_titles.c.start_date,
        schema.role_titles.c.end_date,
        schema.user_group_memberships.c.start_date,
        schema.user_group_memberships.c.end_date,
        ], 
        from_obj=[   
        rdb.join(schema.groups, schema.user_group_memberships,
        schema.groups.c.group_id == schema.user_group_memberships.c.group_id
            ).outerjoin(
            schema.role_titles, schema.user_group_memberships.c.membership_id==
            schema.role_titles.c.membership_id).outerjoin(
                schema.user_role_types,
                schema.role_titles.c.title_name_id ==
                schema.user_role_types.c.user_role_type_id)],
            whereclause =
            rdb.and_(
                schema.groups.c.group_id.in_(group_ids),
                schema.user_group_memberships.c.user_id == user_id),  
            order_by = [schema.user_group_memberships.c.start_date,
                        schema.user_group_memberships.c.end_date,
                        schema.role_titles.c.start_date, 
                        schema.role_titles.c.end_date]                                     
            )
    o_held = connection.execute(offices_held) 
    #session.close              
    return o_held            
    
def get_group_ids_for_user_in_parliament(user_id, parliament_id):
    """ get the groups a user is member of for a specific parliament """
    session = Session()
    connection = session.connection(domain.Group)
    group_ids  = get_all_group_ids_in_parliament(parliament_id)
    my_groups = rdb.select([schema.user_group_memberships.c.group_id],
        rdb.and_(schema.user_group_memberships.c.active_p == True,
            schema.user_group_memberships.c.user_id == user_id,
            schema.user_group_memberships.c.group_id.in_(group_ids)),
        distinct=True)
    my_group_ids = []
    for group_id in connection.execute(my_groups):
        my_group_ids.append(group_id[0])
    ##session.close
    return my_group_ids
                                    
def get_parliament_for_group_id(group_id):
    if group_id is None:
        return None
    session = Session()
    group = session.query(domain.Group).get(group_id)
    #session.close    
    if group.type == 'parliament':
        return group
    else:
        return get_parliament_for_group_id(group.parent_group_id)               
        
        
        
