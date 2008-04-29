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


##############
# Validate if start/end dates are in the date range of its peers 

# object to get the connection from so we can execute a sql statement
class _TmpSqlQuery( object):
    pass    
sqlalchemy.orm.mapper( _TmpSqlQuery, bungeni.core.schema.parliaments )

def checkDateInInterval( pp_key, checkDate, sql_statement):
    """
    check if the checkDate is inside one of its 'peers'
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


def checkStartEndDatesInInterval( pp_key, data, sql_statement):
    """ Check if start and end dates are not overlapping with a prior or later peer
    """
    errors =[]    
    overlaps = checkDateInInterval(pp_key, data['start_date'], sql_statement)
    if overlaps is not None:
        errors.append( interface.Invalid(_("The start date overlaps with (%s)" % overlaps), "start_date" ))
    if data['end_date'] is not None:        
        overlaps = checkDateInInterval(pp_key, data['end_date'], sql_statement)
        if overlaps is not None:
            errors.append( interface.Invalid(_("The end date overlaps with (%s)" % overlaps), "end_date" )) 
    return errors              


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
                        WHERE ( (( "session_id" = %(parent_key)s )
                                 OR ( "group_id" = %(parent_key)s ))
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
sql_checkForOpenParliamentInterval = """
                            SELECT "groups"."short_name" 
                            FROM "public"."parliaments", "public"."groups" 
                            WHERE ( ( "parliaments"."parliament_id" = "groups"."group_id" )
                                    AND "end_date" IS NULL )
                        """





###################
# Date validations

def checkStartDate( parent, data ):
    """ Check that the start date is inside the restrictictions.
    It must not start before the contextParents start date or end
    after the contextsParents end date"""
    errors =[]   
    if data['start_date'] is not None:
        if parent.start_date is not None:
            if data['start_date'] < parent.start_date:
                errors.append( interface.Invalid( _(u"Start date must be after (%s)") % parent.start_date , "start_date" ))
        if parent.end_date is not None:
            if data['start_date'] > parent.end_date:
                errors.append( interface.Invalid( _(u"Start date must be prior to (%s)") % parent.end_date , "start_date" ))     
    return errors               
    
def checkEndDate ( parent, data ):
    """
    Check that the end date is inside the restrictictions.
    It must not end before the contextParents start date or end
    after the contextsParents end date    
    """    
    errors =[]   
    if data['end_date'] is not None:
        if parent.start_date is not None:
            if data['end_date'] < parent.start_date:
                errors.append( interface.Invalid( _(u"End date must be after (%s)")  % parent.start_date , "end_date" ))
        if parent.end_date is not None:
            if data['end_date'] > parent.end_date:
                errors.append( interface.Invalid( _(u"End date must be prior to (%s)") % parent.end_date , "end_date" ))  
    return errors



def checkDates( parent, data ):
    """
    combine checks for start and end date       
    """
    errors = checkStartDate( parent, data )
    errors.append(checkEndDate( parent, data ))
    
    

#############
## Add Forms specific validation

#Parliament

def CheckParliamentDatesAdd( context, data ):
    """
    Parliaments must not overlap
    """       
    errors = checkStartEndDatesInInterval(None, data, sql_checkParliamentInterval)
    #for parliaments we have to check election date as well
    overlaps = checkDateInInterval(None, data['election_date'], sql_checkParliamentInterval)
    if overlaps is not None:
        errors.append(interface.Invalid(_("The election date overlaps with (%s)" % overlaps), "election_date" ))                  
    return errors
    
#ministries
def CheckMinistryDatesInsideGovernmentDatesAdd( context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    return checkDates(context.__parent__ , data )

    
#ministers
def CheckMinisterDatesInsideMinistryDatesAdd( context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    return checkDates(context.__parent__ , data )

    
#gov

def CheckGovernmentsDateInsideParliamentsDatesAdd( context, data ):
    """
    start date must be >= parents start date
    """
    errors = checkStartEndDatesInInterval( None, data, sql_checkGovernmentInterval)
    #### check dates in interval    
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
    return checkDates(context.__parent__ , data )
    

#Extension members

def CheckExtensionMemberDatesInsideParentDatesAdd( context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    return checkDates(context.__parent__ , data )
    

    
# committee members
def CheckCommitteeMembersDatesInsideParentDatesAdd( context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    return checkDates(context.__parent__ , data )
    

    
#committees

def CheckCommitteesDatesInsideParentDatesAdd( context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    return checkDates(context.__parent__ , data )
    

    
#MPs

def CheckMPsDatesInsideParentDatesAdd( context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    return checkDates(context.__parent__ , data )
    

    
#sessions

def CheckSessionDatesInsideParentDatesAdd( context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    errors = checkStartEndDatesInInterval(context.__parent__.parliament_id, data , sql_checkSessionInterval)     
    return errors.append(checkDates(context.__parent__ , data ))
    
   
    
#sittings

def CheckSittingDatesInsideParentDatesAdd( context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    errors = checkStartEndDatesInInterval(context.__parent__.session_id, data, sql_checkSittingInterval)

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

sql_checkSittingInterval = """
                            SELECT "group_sittings_1"."start_date"  || ' - ' ||  "group_sittings_1"."end_date" AS interval
                            FROM "public"."group_sittings" ,  "public"."group_sittings" AS  "group_sittings_1"
                            WHERE ((( "group_sittings_1"."group_id" = "group_sittings"."group_id" 
                                        OR "group_sittings_1"."session_id" = "group_sittings"."session_id" ) 
                                        AND ( "group_sittings"."sitting_id" = %(parent_key)s ) )
                                    AND ( "group_sittings_1"."sitting_id" !=  %(parent_key)s )
                                    AND ( '%(date)s' 
                                        BETWEEN  "group_sittings_1"."start_date" AND  "group_sittings_1"."end_date"))
                           """


# sittings

def CheckSittingDatesInsideParentDatesEdit( context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    errors = checkStartEndDatesInInterval(context.sitting_id, data, sql_checkSittingInterval)
    
    if context.__parent__.__parent__.start_date > data['start_date'].date():
        errors.append( interface.Invalid(_("Start must be after Session Start Date (%s)" % context.__parent__.__parent__.start_date )) )
    if context.__parent__.__parent__.end_date is not None:
        if data['end_date'].date() > context.__parent__.__parent__.end_date:
            errors.append(  interface.Invalid(_("End must be before Session End Date (%s)" % context.__parent__.__parent__.end_date ) ) )
        if data['start_date'].date() > context.__parent__.__parent__.end_date:
            errors.append(  interface.Invalid(_("Start must be before Session End Date (%s)" % context.__parent__.__parent__.end_date )) )            
    return errors
    
                        
