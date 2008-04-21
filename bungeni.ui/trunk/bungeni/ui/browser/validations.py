# encoding: utf-8
"""
form validations for custom forms
"""

import datetime
from zope import interface
from bungeni.core.i18n import _

from ore.alchemist import Session

import bungeni.core.schema
import sqlalchemy.orm

import pdb

##############
# Validate if start/end dates are in the date range of its peers 

# object to get the connection from so we can execute a sql statement
class _TmpSqlQuery( object):
    pass    
sqlalchemy.orm.mapper( _TmpSqlQuery, bungeni.core.schema.parliaments )

def checkDateInInterval( pp_key, checkDate, sql_statement):
    """
    check if the checkDate ...
    the passed sql statement must follow the restrictions:
    %(date)s is the date to check (must be present!)
    %(parent_key)s is usually the parents primary key (can be omitted to check all)
    """
    if (type(checkDate) is datetime.datetime or type(checkDate) is datetime.date):
        session = Session()
        checkDict = { 'date': checkDate, 'parent_key': pp_key }
        sql_text = sql_statement % (checkDict)
        connection = session.connection(_TmpSqlQuery)      
        query = connection.execute(sql_text)
        result = query.fetchone()
        if result is None:
            return result
        else:
            return result[0]            
    else:
        raise TypeError        


sql_checkSessionInterval = """
                         SELECT "short_name"  
                         FROM "public"."sessions" 
                         WHERE ( ( "parliament_id" = %(parent_key)s ) 
                                AND ( '%(date)s' 
                                    BETWEEN "start_date" AND "end_date") )
                        """
sql_checkSittingInterval = """
                        SELECT "start_date" || ' - ' || "end_date" AS interval
                        FROM "public"."group_sittings" 
                        WHERE ( ( "session_id" = %(parent_key)s )
                                AND ( '%(date)s' 
                                    BETWEEN "start_date" AND "end_date") )
                        """
sql_checkGovernmentInterval = """
                            SELECT "groups"."short_name" 
                            FROM "public"."government", "public"."groups" 
                            WHERE ( ( "government"."government_id" = "groups"."group_id" )
                                AND ( '%(date)s' 
                                    BETWEEN "start_date" AND "end_date") )
                        """
    
sql_checkParliamentInterval = """
                            SELECT "groups"."short_name" 
                            FROM "public"."parliaments", "public"."groups" 
                            WHERE ( ( "parliaments"."parliament_id" = "groups"."group_id" )
                                AND ( '%(date)s' 
                                    BETWEEN "start_date" AND "end_date") )
                        """


#############
## Add Forms specific validation

#Parliament

def CheckParliamentDatesAdd( context, data ):
    """
    Parliaments must not overlap
    """
    errors =[]    
    overlaps = checkDateInInterval(None, data['start_date'], sql_checkParliamentInterval)
    if overlaps is not None:
        errors.append( interface.Invalid(_("The Parliament overlaps with (%s)" % overlaps)) )
    return errors
    
#ministries
def CheckMinistryDatesInsideGovernmentDatesAdd( context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    errors =[]
    if context.__parent__.start_date > data['start_date']:
        errors.append( interface.Invalid(_("Start date must start after the swearing in of the government (%s)" % context.__parent__.start_date )) )
    if (context.__parent__.end_date is not None) and (data['end_date'] is not None):
        if data['end_date'] > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("End date cannot be after the governments dissolution (%s)" % context.__parent__.end_date )) )
    if (context.__parent__.end_date is not None):
        if data['start_date'] > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("Start date cannot be after the governments dissolution (%s)" % context.__parent__.end_date )) )            
    return errors
    
#ministers
def CheckMinisterDatesInsideMinistryDatesAdd( context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    errors =[]
    if context.__parent__.start_date > data['start_date']:
        errors.append( interface.Invalid(_("Start date must start after the ministry start date (%s)" % context.__parent__.start_date )) )
    if (context.__parent__.end_date is not None) and (data['end_date'] is not None):
        if data['end_date'] > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("End date cannot be after the ministries end date (%s)" % context.__parent__.end_date )) )
    if (context.__parent__.end_date is not None):
        if data['start_date'] > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("Start date cannot be after the ministries end date (%s)" % context.__parent__.end_date )) )            
    return errors
    
#gov

def CheckGovernmentsDateInsideParliamentsDatesAdd( context, data ):
    """
    start date must be >= parents start date
    """
    errors =[]
    #### check dates in interval    
    overlaps = checkDateInInterval(None, data['start_date'], sql_checkGovernmentInterval)
    if overlaps is not None:
        errors.append( interface.Invalid(_("The Government overlaps with (%s)" % overlaps)) )
    if data['end_date'] is not None:
        overlaps = checkDateInInterval(None, data['end_date'], sql_checkGovernmentInterval)
        if overlaps is not None:
            errors.append( interface.Invalid(_("The Government overlaps with (%s)" % overlaps)) ) 
    if (context.__parent__.end_date is not None):
        if data['start_date'] > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("Start date cannot be after the parliaments dissolution (%s)" % context.__parent__.end_date )) )
    if context.__parent__.start_date > data['start_date']:
        errors.append( interface.Invalid(_("Start date must start after the swearing in of the parliament (%s)" % context.__parent__.start_date )) )    
    return errors
#Extension groups

def CheckExtensionGroupDatesInsideParentDatesAdd( context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    errors =[]
    if context.__parent__.start_date > data['start_date']:
        errors.append( interface.Invalid(_("Start date must start after the swearing in of the parliament (%s)" % context.__parent__.start_date )) )
    if (context.__parent__.end_date is not None) and (data['end_date'] is not None):
        if data['end_date'] > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("End date cannot be after the parliaments dissolution (%s)" % context.__parent__.end_date )) )
    if (context.__parent__.end_date is not None):
        if data['start_date'] > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("Start date cannot be after the parliaments dissolution (%s)" % context.__parent__.end_date )) )            
    return errors

#Extension members

def CheckExtensionMemberDatesInsideParentDatesAdd( context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    errors =[]
    if context.__parent__.start_date > data['start_date']:
        errors.append( interface.Invalid(_("Start date must start after the groups start date (%s)" % context.__parent__.start_date )) )
    if (context.__parent__.end_date is not None) and (data['end_date'] is not None):
        if data['end_date'] > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("End date cannot be after the groups end date (%s)" % context.__parent__.end_date )) )
    if (context.__parent__.end_date is not None):
        if data['start_date'] > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("Start date cannot be after the groups end date (%s)" % context.__parent__.end_date )) )            
    return errors
    
# committee members
def CheckCommitteeMembersDatesInsideParentDatesAdd( context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    errors =[]
    if context.__parent__.start_date > data['start_date']:
        errors.append( interface.Invalid(_("Start date must start after the start date of the committee (%s)" % context.__parent__.start_date )) )
    if (context.__parent__.end_date is not None) and (data['end_date'] is not None):
        if data['end_date'] > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("End date cannot be after the committees dissolution (%s)" % context.__parent__.end_date )) )
    if (context.__parent__.end_date is not None):
        if data['start_date'] > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("Start date cannot be after the committees dissolution (%s)" % context.__parent__.end_date )) )            
    return errors
    
#committees

def CheckCommitteesDatesInsideParentDatesAdd( context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    errors =[]
    if context.__parent__.start_date > data['start_date']:
        errors.append( interface.Invalid(_("Start date must start after the swearing in of the parliament (%s)" % context.__parent__.start_date )) )
    if (context.__parent__.end_date is not None) and (data['end_date'] is not None):
        if data['end_date'] > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("End date cannot be after the parliaments dissolution (%s)" % context.__parent__.end_date )) )
    if (context.__parent__.end_date is not None):
        if data['start_date'] > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("Start date cannot be after the parliaments dissolution (%s)" % context.__parent__.end_date )) )            
    return errors
    
#MPs

def CheckMPsDatesInsideParentDatesAdd( context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    errors =[]
    if context.__parent__.start_date > data['start_date']:
        errors.append( interface.Invalid(_("Start date must start after the swearing in of the parliament (%s)" % context.__parent__.start_date )) )
    if (context.__parent__.end_date is not None) and (data['end_date'] is not None):
        if data['end_date'] > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("End date cannot be after the parliaments dissolution (%s)" % context.__parent__.end_date )) )
    if (context.__parent__.end_date is not None):
        if data['start_date'] > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("Start date cannot be after the parliaments dissolution (%s)" % context.__parent__.end_date )) )
             
    return errors
    
#sessions

def CheckSessionDatesInsideParentDatesAdd( context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    errors =[]
    #### check dates in interval    
    overlaps = checkDateInInterval(context.__parent__.parliament_id, data['start_date'], sql_checkSessionInterval)
    if overlaps is not None:
        errors.append( interface.Invalid(_("The session overlaps with (%s)" % overlaps)) )
    if data['end_date'] is not None:
        overlaps = checkDateInInterval(context.__parent__.parliament_id, data['end_date'], sql_checkSessionInterval)
        if overlaps is not None:
            errors.append( interface.Invalid(_("The session overlaps with (%s)" % overlaps)) )    
    if context.__parent__.start_date > data['start_date']:
        errors.append( interface.Invalid(_("A Session must start after the swearing in of the parliament (%s)" % context.__parent__.start_date )) )
    if (context.__parent__.end_date is not None) and (data['end_date'] is not None):
        if data['end_date'] > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("A Session cannot take place after the parliaments dissolution (%s)" % context.__parent__.end_date )) )
    if (context.__parent__.end_date is not None):
        if data['start_date'] > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("A Session cannot take place after the parliaments dissolution (%s)" % context.__parent__.end_date )) )            
    return errors
    
#sittings

def CheckSittingDatesInsideParentDatesAdd( context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    errors =[]
    #### check dates in interval    
    overlaps = checkDateInInterval(context.__parent__.session_id, data['start_date'], sql_checkSittingInterval)
    if overlaps is not None:
        errors.append( interface.Invalid(_("The sitting overlaps with (%s)" % overlaps)) )
    if data['end_date'] is not None:
        overlaps = checkDateInInterval(context.__parent__.session_id, data['end_date'], sql_checkSittingInterval)
        if overlaps is not None:
            errors.append( interface.Invalid(_("The sitting overlaps with (%s)" % overlaps)) )    
    if context.__parent__.start_date > data['start_date'].date():
        errors.append( interface.Invalid(_("Start must be after Session Start Date (%s)" % context.__parent__.start_date )) )
    if context.__parent__.end_date is not None:
        if data['end_date'].date() > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("End must be before Session End Date (%s)" % context.__parent__.end_date )) )
        if data['start_date'].date() > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("Start must be before Session End Date (%s)" % context.__parent__.end_date )) )
    return errors

##################
# Edit forms specific validation

# sittings

def CheckSittingDatesInsideParentDatesEdit( context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    errors =[]
    if context.__parent__.__parent__.start_date > data['start_date'].date():
        errors.append( interface.Invalid(_("Start must be after Session Start Date (%s)" % context.__parent__.__parent__.start_date )) )
    if context.__parent__.__parent__.end_date is not None:
        if data['end_date'].date() > context.__parent__.__parent__.end_date:
            errors.append(  interface.Invalid(_("End must be before Session End Date (%s)" % context.__parent__.__parent__.end_date ) ) )
        if data['start_date'].date() > context.__parent__.__parent__.end_date:
            errors.append(  interface.Invalid(_("Start must be before Session End Date (%s)" % context.__parent__.__parent__.end_date )) )            
    return errors
    
                        
