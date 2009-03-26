# encoding: utf-8
"""
form validations for custom forms
"""

import datetime
from zope import interface
from bungeni.core.i18n import _

from ore.alchemist import Session

from bungeni.models import interfaces, domain, schema

import sqlalchemy as rdb


from bungeni.ui.queries.utils import validate_date_in_interval, validate_open_interval

from bungeni.ui.queries import utils
from bungeni.ui.utils import get_date


def null_validator(*args, **kwargs):
    return []


def validate_start_date_within_parent( parent, data ):
    """ Check that the start date is inside the restrictictions.
    It must not start before the contextParents start date or end
    after the contextsParents end date"""
    errors =[]   
    if data['start_date'] is not None:
        start = get_date(data['start_date'])    
        if parent.start_date is not None:
            pstart = get_date(parent.start_date)
            if start < pstart:
                errors.append( interface.Invalid( 
                _(u"Start date must be after (%s)") % pstart, 
                "start_date" ))
        if parent.end_date is not None:
            pend = get_date(parent.end_date)
            if start > pend:
                errors.append( interface.Invalid( 
                _(u"Start date must be prior to (%s)") % pend, 
                "start_date" ))     
    return errors               
    
def validate_end_date_within_parent( parent, data ):
    """
    Check that the end date is inside the restrictictions.
    It must not end before the context.Parents start date or end
    after the context.Parents end date    
    """    
    errors =[]   
    if data['end_date'] is not None:
        end = get_date(data['end_date'])                
        if parent.start_date is not None:
            pstart = get_date(parent.start_date)
            if end < pstart:
                errors.append( interface.Invalid( 
                _(u"End date must be after (%s)")  % pstart, 
                "end_date" ))
        if parent.end_date is not None:
            pend = get_date(parent.end_date)        
            if end > pend:
                errors.append( interface.Invalid( 
                _(u"End date must be prior to (%s)") % pend, 
                "end_date" ))  
    return errors




 
def validate_date_range_within_parent(action, data, context, container):
    errors = validate_start_date_within_parent( container.__parent__, data )
    errors = errors + validate_end_date_within_parent( container.__parent__, data )
    return errors


        


class AllPartyMemberships(object):
    """ Helper class to get all partymemberships
    for all users """

all_party_memberships = rdb.join( 
        schema.user_group_memberships, schema.groups).join(
           schema.political_parties)
        
rdb.orm.mapper(AllPartyMemberships, all_party_memberships)     

def validate_party_membership(action, data, context, container):
    errors = []
    if interfaces.IPartyMember.providedBy(context):
        party_member = context
        user_id = context.user_id
    else:
        party_member = None
        user_id = data['user_id']
    session = Session()                
    if data['start_date']:
        for r in utils.validate_membership_in_interval(party_member, 
                    AllPartyMemberships, 
                    data['start_date'],
                    user_id):  
            overlaps = r.short_name                                                                             
            errors.append(interface.Invalid(
                _("The person is a member in (%s) at that date") % overlaps, 
                "start_date" ))                    
    if data['end_date']:    
        for r in utils.validate_membership_in_interval(party_member, 
                    AllPartyMemberships, 
                    data['end_date'],
                    user_id):    
            overlaps = r.short_name                      
            errors.append(interface.Invalid(
                _("The person is a member in (%s) at that date") % overlaps, 
                "end_date" ))                                
    for r in utils.validate_open_membership(party_member, AllPartyMemberships, user_id):
        overlaps = r.short_name      
        errors.append(interface.Invalid(
                    _("The person is a member in (%s) at that date") % overlaps, 
                    "end_date" )) 
    return errors                    
    




def validate_parliament_dates(action, data, context, container):
    """Parliaments must not overlap."""
    errors = []
    if interfaces.IParliament.providedBy(context):
        parliament = context
    else:
        parliament = None
    results = validate_date_in_interval(parliament, 
                domain.Parliament, 
                data['start_date'])
    for result in results:
        overlaps = result.short_name
        errors.append(interface.Invalid(
            _("The start date overlaps with (%s)") % overlaps, "start_date"))
    if data['end_date']:
        results = validate_date_in_interval(parliament, 
                    domain.Parliament, 
                    data['start_date'])           
        for result in results:
            overlaps = result.short_name
            errors.append(interface.Invalid(
                _("The end date overlaps with (%s)") % overlaps, "end_date"))
            
    results = validate_date_in_interval(parliament, domain.Parliament, data['election_date'])
    for result in results:
        overlaps = result.short_name
        errors.append(interface.Invalid(
            _("The election date overlaps with (%s)") % 
            overlaps, 
            "election_date")
            )
        
    results = validate_open_interval(parliament, domain.Parliament)
    for result in results:
        overlaps = result.short_name
        errors.append(interface.Invalid(
            _("Another parliament is not yet dissolved (%s)") % overlaps,
            "election_date"))
        
    return errors



def validate_government_dates(action, data, context, container):
    errors = []
    if interfaces.IGovernment.providedBy(context):
        government = context
    else:
        government = None
            
    if container.__parent__.end_date is not None:
        if data['start_date'] > container.__parent__.end_date:
            errors.append(  interface.Invalid(
                _("Start date cannot be after the parliaments dissolution (%s)") 
                % container.__parent__.end_date , 
                "start_date") )
    if container.__parent__.start_date > data['start_date']:
        errors.append( interface.Invalid(
            _("Start date must start after the swearing in of the parliament (%s)") 
            % container.__parent__.start_date , 
            "start_date") )   
    results = validate_date_in_interval(government, 
                    domain.Government, 
                    data['start_date'])
    for result in results:
        overlaps = result.short_name
        errors.append(interface.Invalid(
            _("The start date overlaps with (%s)") % overlaps, 
            "start_date"))
    if data['end_date']:
        results = validate_date_in_interval(government, 
                    domain.Government, 
                    data['start_date'])            
        for result in results:
            overlaps = result.short_name
            errors.append(interface.Invalid(
                _("The end date overlaps with (%s)") % overlaps, 
                "end_date"))
            
    results = validate_open_interval(government, domain.Government)
    for result in results:
        overlaps = result.short_name
        errors.append(interface.Invalid(
            _("Another Government is not yet dissolved (%s)") % overlaps,
            "start_date"))
        
    return errors
  
def validate_group_membership_dates(action, data, context, container):
    """ A User must be member of a group only once at a time """
    errors =[]
    group_id = container.__parent__.group_id    
    if interfaces.IGroupMembership.providedBy(context):
        group_membership = context
    else:         
        group_membership = None
    user_id = data['user_id']           
    session = Session()
    if data['start_date']:
        for r in utils.validate_membership_in_interval(group_membership, 
                    domain.GroupMembership, 
                    data['start_date'],
                    user_id, group_id):  
            overlaps = r.group.short_name                                                                             
            errors.append(interface.Invalid(
                _("The person is a member in (%s) at that date") % overlaps, 
                "start_date" ))                    
    if data['end_date']:    
        for r in utils.validate_membership_in_interval(group_membership, 
                    domain.GroupMembership, 
                    data['end_date'],
                    user_id, group_id):    
            overlaps = r.group.short_name                      
            errors.append(interface.Invalid(
                _("The person is a member in (%s) at that date") % overlaps, 
                "end_date" ))                                
    for r in utils.validate_open_membership(group_membership, 
                domain.GroupMembership, 
                user_id, group_id):
        overlaps = r.group.short_name      
        errors.append(interface.Invalid(
                    _("The person is a member in (%s) at that date") % overlaps, 
                    "end_date" )) 

    return errors
                 

class GroupMemberTitle(object):
    """ Titels that may be held by multiple persons of the
    group at the same time"""     

group_member_title = rdb.join(schema.user_group_memberships, 
        schema.role_titles).join(
            schema.user_role_types)
            
                        
rdb.orm.mapper( GroupMemberTitle, group_member_title )                         


def validate_member_titles(action, data, context, container):
    """Titles for members follow the restrictions:
    A person must have the same title only once (e.g. you cannot
    be chairperson in a group twice at a time)       
    If a Title is unique (e.g. chairperson) there can be only one person 
    at a time in this group holding this title, other titles like member 
    may be applied to several persons at the same time""" 
    def get_q_user(date):
        return session.query(GroupMemberTitle).filter(
                rdb.and_(
                    schema.user_group_memberships.c.group_id == group_id,
                    schema.user_group_memberships.c.membership_id == membership_id,
                    schema.role_titles.c.title_name_id == title_name_id,
                    rdb.or_(
                        rdb.between(
                            date, 
                            schema.role_titles.c.start_date,
                            schema.role_titles.c.end_date),
                        schema.role_titles.c.end_date == None  
                        )                  
                    )
                )
    def get_q_unique(date):
        return session.query(GroupMemberTitle).filter(
            rdb.and_(
                schema.user_group_memberships.c.group_id == group_id,
                schema.user_role_types.c.user_unique == True,
                schema.role_titles.c.title_name_id == title_name_id,
                rdb.or_(
                    rdb.between(
                        date, 
                        schema.role_titles.c.start_date,
                        schema.role_titles.c.end_date),
                    schema.role_titles.c.end_date == None  
                    )                  
                )  
            )                 
    errors = []
    group_id = container.__parent__.group_id    
    user_id = container.__parent__.user_id    
    membership_id = container.__parent__.membership_id    
    session = Session()
    title_name_id = data['title_name_id']
    if interfaces.IMemberRoleTitle.providedBy(context):
        roletitle = context
    else:
        roletitle = None        
    date = datetime.date.today()        
    
    if data['start_date']:
        date = data['start_date']
        q = get_q_user(date)
        results = q.all()    
        for result in results:
            overlaps = result.user_role_name        
            if roletitle:
                if roletitle.role_title_id == result.role_title_id:
                    continue
                else:                    
                    errors.append( interface.Invalid(
                        _(u"This persons allready has the title %s") % 
                        overlaps, 
                        "start_date" ))            
            else:
                errors.append( interface.Invalid(
                    _(u"This persons allready has the title %s") % 
                    overlaps, 
                    "start_date" )) 
    if data['end_date']:
        date = data['end_date']
        q = get_q_user(date)
        results = q.all()   
        for result in results:
            overlaps = result.user_role_name        
            if roletitle:
                if roletitle.role_title_id == result.role_title_id:
                    continue
                else:                    
                    errors.append( interface.Invalid(
                        _(u"This persons allready has the title %s") % 
                        overlaps, 
                        "end_date" ))            
            else:
                errors.append( interface.Invalid(
                    _(u"This persons allready has the title %s") % 
                    overlaps, 
                    "end_date" ))                                              
    if data['start_date']:
        date = data['start_date']
        q = get_q_unique(date)
        results = q.all()    
        for result in results:
            overlaps = result.user_role_name        
            if roletitle:
                if roletitle.role_title_id == result.role_title_id:
                    continue
                else:               
                    errors.append( interface.Invalid(
                        _(u"A person with the title %s allready exists") % 
                        overlaps, 
                        "start_date" ))  
            else:
                errors.append( interface.Invalid(
                    _(u"A person with the title %s allready exists") % 
                    overlaps, 
                    "start_date" ))                                      
            
    if data['end_date']:
        date = data['end_date']
        q = get_q_unique(date)
        results = q.all()   
        for result in results:
            overlaps = result.user_role_name                
            if roletitle:
                if roletitle.role_title_id == result.role_title_id:
                    continue
                else:                           
                    errors.append( interface.Invalid(
                        _(u"A person with the title %s allready exists") % 
                        overlaps, 
                        "end_date" ))                                                               
            else:
                errors.append( interface.Invalid(
                    _(u"A person with the title %s allready exists") % 
                    overlaps, 
                    "end_date" ))                                         
    return errors


