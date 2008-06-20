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
sql_checkSittingSessionInterval = """
                        SELECT "start_date" || ' - ' || "end_date" AS interval
                        FROM "public"."group_sittings" 
                        WHERE ( ( "session_id" = %(parent_key)s )
                                 
                                AND ( '%(date)s' 
                                    BETWEEN "start_date" AND "end_date") )
                        """
sql_checkSittingGroupInterval = """
                        SELECT "start_date" || ' - ' || "end_date" AS interval
                        FROM "public"."group_sittings" 
                        WHERE (  ( "group_id" = %(parent_key)s )
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
    errors = errors + checkEndDate( parent, data )
    return errors
    

#############
## Add Forms specific validation

#Parliament

def CheckParliamentDatesAdd( self,  context, data ):
    """
    Parliaments must not overlap
    """       
    errors = checkStartEndDatesInInterval(None, data, sql_checkParliamentInterval)
    #for parliaments we have to check election date as well
    overlaps = checkDateInInterval(None, data['election_date'], sql_checkParliamentInterval)
    if overlaps is not None:
        errors.append(interface.Invalid(_("The election date overlaps with (%s)") % overlaps, "election_date" ))   
    overlaps = checkDateInInterval(None, data['election_date'], sql_checkForOpenParliamentInterval )   
    if overlaps is not None:
        errors.append(interface.Invalid(_("Another parliament is not yet dissolved (%s)") % overlaps, "election_date" ))            
    return errors

def CheckParliamentDatesAdd1( self, context, data ):
    """
    Parliaments must not overlap
    """       
    errors = checkStartEndDatesInInterval(None, data, sql_checkParliamentInterval)
    #for parliaments we have to check election date as well
    overlaps = checkDateInInterval(None, data['election_date'], sql_checkParliamentInterval)
    if overlaps is not None:
        errors.append(interface.Invalid(_("The election date overlaps with (%s)") % overlaps, "election_date" ))   
    overlaps = checkDateInInterval(None, data['election_date'], sql_checkForOpenParliamentInterval )   
    if overlaps is not None:
        errors.append(interface.Invalid(_("Another parliament is not yet dissolved (%s)") % overlaps, "election_date" ))            
    return errors
        
#ministries
def CheckMinistryDatesInsideGovernmentDatesAdd( self,  context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    return checkDates(context.__parent__ , data )

    
#ministers
def CheckMinisterDatesInsideMinistryDatesAdd( self,  context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    return checkDates(context.__parent__ , data )

    
#gov

def CheckGovernmentsDateInsideParliamentsDatesAdd( self,  context, data ):
    """
    start date must be >= parents start date
    """
    errors = checkStartEndDatesInInterval( None, data, sql_checkGovernmentInterval)
    #### check dates in interval    
    if (context.__parent__.end_date is not None):
        if data['start_date'] > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("Start date cannot be after the parliaments dissolution (%s)" % context.__parent__.end_date ), "start_date") )
    if context.__parent__.start_date > data['start_date']:
        errors.append( interface.Invalid(_("Start date must start after the swearing in of the parliament (%s)" % context.__parent__.start_date ), "start_date") )    
    return errors
#Extension groups

def CheckExtensionGroupDatesInsideParentDatesAdd( self,  context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    return checkDates(context.__parent__ , data )
    

#Extension members

def CheckExtensionMemberDatesInsideParentDatesAdd( self,  context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    return checkDates(context.__parent__ , data )
    

    
# committee members
def CheckCommitteeMembersDatesInsideParentDatesAdd( self,  context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    return checkDates(context.__parent__ , data )
    

    
#committees

def CheckCommitteesDatesInsideParentDatesAdd( self,  context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    return checkDates(context.__parent__ , data )
    

    
#MPs

def CheckMPsDatesInsideParentDatesAdd( self,  context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    return checkDates(context.__parent__ , data )
    

    
#sessions

def CheckSessionDatesInsideParentDatesAdd( self,  context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    errors = checkStartEndDatesInInterval(context.__parent__.parliament_id, data , sql_checkSessionInterval)     
    errors = errors + checkDates(context.__parent__ , data )
    return errors
    
   
    
#sittings

def CheckSittingDatesInsideParentDatesAdd( self,  context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    if getattr(context.__parent__, 'session_id', None):
        errors = checkStartEndDatesInInterval(context.__parent__.session_id, data, sql_checkSittingSessionInterval)
    elif getattr(context.__parent__, 'group_id', None):          
        errors = checkStartEndDatesInInterval(context.__parent__.group_id, data, sql_checkSittingGroupInterval)
    if context.__parent__.start_date > data['start_date'].date():
        errors.append( interface.Invalid(_("Start must be after Session Start Date (%s)") % context.__parent__.start_date, "start_date" ) )
    if context.__parent__.end_date is not None:
        if data['end_date'].date() > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("End must be before Session End Date (%s)") % context.__parent__.end_date, "end_date" ) )
        if data['start_date'].date() > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("Start must be before Session End Date (%s)") % context.__parent__.end_date, "start_date" ) )
    return errors

def CheckMemberTitleDateAdd( self, context, data):
    errors =  checkDates(context.__parent__ , data )
    return errors

##################
# Edit forms specific validation

sql_checkMySittingSessionInterval = """
                            SELECT "group_sittings_1"."start_date"  || ' - ' ||  "group_sittings_1"."end_date" AS interval
                            FROM "public"."group_sittings" ,  "public"."group_sittings" AS  "group_sittings_1"
                            WHERE ((("group_sittings_1"."session_id" = "group_sittings"."session_id" ) 
                                        AND ( "group_sittings"."sitting_id" = %(parent_key)s ) )
                                    AND ( "group_sittings_1"."sitting_id" !=  %(parent_key)s )
                                    AND ( '%(date)s' 
                                        BETWEEN  "group_sittings_1"."start_date" AND  "group_sittings_1"."end_date"))
                           """
sql_checkMySittingGroupInterval = """
                            SELECT "group_sittings_1"."start_date"  || ' - ' ||  "group_sittings_1"."end_date" AS interval
                            FROM "public"."group_sittings" ,  "public"."group_sittings" AS  "group_sittings_1"
                            WHERE ((( "group_sittings_1"."group_id" = "group_sittings"."group_id" )
                                        AND ( "group_sittings"."sitting_id" = %(parent_key)s ) )
                                    AND ( "group_sittings_1"."sitting_id" !=  %(parent_key)s )
                                    AND ( '%(date)s' 
                                        BETWEEN  "group_sittings_1"."start_date" AND  "group_sittings_1"."end_date"))
                           """
                           

sql_checkMySessionInterval = """
                         SELECT "sessions_1"."short_name"  
                         FROM "public"."sessions", "public"."sessions"  AS "sessions_1"
                         WHERE ( ( "sessions_1"."parliament_id" = "sessions"."parliament_id" )
                                AND ( "sessions"."session_id" = %(parent_key)s )
                                AND ( "sessions_1"."session_id" != %(parent_key)s )
                                AND ( '%(date)s' 
                                    BETWEEN "sessions_1"."start_date" AND "sessions_1"."end_date") )
                        """

                        
sql_checkMyGovernmentInterval = """
                            SELECT "groups"."short_name" 
                            FROM "public"."government", "public"."groups" 
                            WHERE ( ( "government"."government_id" = "groups"."group_id" )
                                AND ( "government"."government_id" != %(parent_key)s )
                                AND ( '%(date)s' 
                                    BETWEEN "start_date" AND "end_date") )
                        """
    
sql_checkMyParliamentInterval = """
                            SELECT "groups"."short_name" 
                            FROM "public"."parliaments", "public"."groups" 
                            WHERE ( ( "parliaments"."parliament_id" = "groups"."group_id" )
                                AND ( "parliaments"."parliament_id" != %(parent_key)s )
                                AND ( '%(date)s' 
                                    BETWEEN "start_date" AND "end_date") )
                        """
                        
sql_checkForMyOpenParliamentInterval = """
                            SELECT "groups"."short_name" 
                            FROM "public"."parliaments", "public"."groups" 
                            WHERE ( ( "parliaments"."parliament_id" = "groups"."group_id" )
                                    AND ( "parliaments"."parliament_id" != %(parent_key)s )
                                    AND "end_date" IS NULL )
                        """

#Parliament

def CheckParliamentDatesEdit( self, context, data ):
    """
    Parliaments must not overlap
    """       
    errors = checkStartEndDatesInInterval(context.parliament_id, data, sql_checkMyParliamentInterval)
    #for parliaments we have to check election date as well
    overlaps = checkDateInInterval(context.parliament_id, data['election_date'], sql_checkMyParliamentInterval)
    if overlaps is not None:
        errors.append(interface.Invalid(_("The election date overlaps with (%s)") % overlaps, "election_date" ))   
    overlaps = checkDateInInterval(context.parliament_id, data['election_date'], sql_checkForMyOpenParliamentInterval )   
    if overlaps is not None:
        errors.append(interface.Invalid(_("Another parliament is not yet dissolved (%s)") % overlaps , "election_date" ))                        
    return errors

# Governments
def CheckGovernmentsDateInsideParliamentsDatesEdit( self, context, data ):
    """
    start date must be >= parents start date
    """
    errors = checkStartEndDatesInInterval( context.government_id, data, sql_checkMyGovernmentInterval)
    #### check dates in interval    
    if (context.__parent__.__parent__.end_date is not None):
        if data['start_date'] > context.__parent__.__parent__.end_date:
            errors.append(  interface.Invalid(_("Start date cannot be after the parliaments dissolution (%s)") % context.__parent__.__parent__.end_date , "start_date") )
    if context.__parent__.__parent__.start_date > data['start_date']:
        errors.append( interface.Invalid(_("Start date must start after the swearing in of the parliament (%s)") % context.__parent__.__parent__.start_date , "start_date") )    
    return errors
#Extension groups

# sittings

def CheckSittingDatesInsideParentDatesEdit( self, context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    #errors = checkStartEndDatesInInterval(context.sitting_id, data, sql_checkMySittingInterval)
    if getattr(context.__parent__.__parent__, 'session_id', None):
        errors = checkStartEndDatesInInterval(context.sitting_id, data, sql_checkMySittingSessionInterval)
    elif getattr(context.__parent__.__parent__, 'group_id', None):          
        errors = checkStartEndDatesInInterval(context.sitting_id, data, sql_checkMySittingGroupInterval)
    
    if context.__parent__.__parent__.start_date > data['start_date'].date():
        errors.append( interface.Invalid(_("Start must be after Session Start Date (%s)") % context.__parent__.__parent__.start_date, "start_date") )
    if context.__parent__.__parent__.end_date is not None:
        if data['end_date'].date() > context.__parent__.__parent__.end_date:
            errors.append(  interface.Invalid(_("End must be before Session End Date (%s)") % context.__parent__.__parent__.end_date, "end_date" ) )
        if data['start_date'].date() > context.__parent__.__parent__.end_date:
            errors.append(  interface.Invalid(_("Start must be before Session End Date (%s)") % context.__parent__.__parent__.end_date, "start_date") )            
    return errors

def CheckSessionDatesEdit( self, context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    errors = checkStartEndDatesInInterval(context.session_id , data , sql_checkMySessionInterval)     
    errors = errors + checkDates(context.__parent__.__parent__ , data )       
    return errors
    
def CheckMemberDatesEdit( self, context, data ):
    errors = checkDates(context.__parent__.__parent__ , data )       
    return errors
    
def CheckCommitteeDatesEdit( self, context, data ):
    errors = checkDates(context.__parent__.__parent__ , data )       
    return errors
    
def CommitteeMemberDatesEdit( self, context, data ):
    errors = checkDates(context.__parent__.__parent__ , data )       
    return errors      
                        
def MinistryDatesEdit( self, context, data ):
    errors = checkDates(context.__parent__.__parent__ , data )       
    return errors                               
                       
def MinisterDatesEdit( self, context, data ):
    errors = checkDates(context.__parent__.__parent__ , data )       
    return errors                               
                        
def ExtensionGroupDatesEdit( self, context, data ):
    errors = checkDates(context.__parent__.__parent__ , data )       
    return errors                                  
    
def ExtensionMemberDatesEdit( self, context, data ):
    errors = checkDates(context.__parent__.__parent__ , data )       
    return errors
              
def CheckMemberTitleDateEdit( self, context, data):
    errors =  checkDates(context.__parent__ , data )
    return errors         
        
