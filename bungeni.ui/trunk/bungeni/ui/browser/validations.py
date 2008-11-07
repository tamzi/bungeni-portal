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

def checkBySQL( sql_statement, check_dict):
    """
    run SQL with variables in the dict
    """
    session = Session()
    sql_text = sql_statement % (check_dict)
    connection = session.connection(_TmpSqlQuery)      
    query = connection.execute(sql_text)
    result = query.fetchone()
    if result is None:
        return result
    else:
        return result[0]            


def checkDateInInterval( pp_key, checkDate, sql_statement):
    """
    check if the checkDate is inside one of its 'peers'
    the passed sql statement must follow the restrictions:
    %(date)s is the date to check (must be present!)
    %(parent_key)s is usually the parents primary key (can be omitted to check all)
    """
    if (type(checkDate) is datetime.datetime or type(checkDate) is datetime.date):
        checkDict = { 'date': checkDate, 'parent_key': pp_key }
        return checkBySQL( sql_statement, checkDict)
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

sql_checkForOpenSessionInterval = """
                           SELECT "full_name" FROM "public"."sessions" AS "sessions" 
                           WHERE "end_date" IS NULL 
                           AND "parliament_id" = %(parliament_id)s
                        """



sql_checkForOpenPartymembership = """
                            SELECT "groups"."short_name" 
                            FROM "public"."user_group_memberships", "public"."groups", "public"."political_parties" 
                            WHERE ( "user_group_memberships"."group_id" = "groups"."group_id" 
                                   AND "political_parties"."party_id" = "groups"."group_id" ) 
                              AND ( ( "user_group_memberships"."user_id" = %(user_id)s
                                    AND "user_group_memberships"."end_date" IS NULL ) )
                            
                        """
                       
sql_checkPartymembershipInterval = """
                            SELECT "groups"."short_name" 
                            FROM "public"."user_group_memberships", "public"."groups", "public"."political_parties" 
                            WHERE ( "user_group_memberships"."group_id" = "groups"."group_id" 
                                   AND "political_parties"."party_id" = "groups"."group_id" ) 
                              AND ( ( "user_group_memberships"."user_id" = %(user_id)s )
                                    AND ( '%(date)s' 
                                         BETWEEN "user_group_memberships"."start_date" AND "user_group_memberships"."end_date" ) )
                        """

# check that a member has the title only once
sql_checkMemberTitleDuplicates = """
                        SELECT "user_role_types"."user_role_name", "role_titles"."start_date", "role_titles"."end_date" 
                        FROM "public"."role_titles", "public"."user_role_types" 
                        WHERE ( "role_titles"."title_name_id" = "user_role_types"."user_role_type_id" ) 
                        AND ( ( "role_titles"."title_name_id" = %(title_name_id)s AND "role_titles"."membership_id" = %(membership_id)s ) )
                        AND (('%(date)s' BETWEEN "role_titles"."start_date" AND "role_titles"."end_date")
                             OR (('%(date)s' >= "role_titles"."start_date" AND "role_titles"."end_date" IS NULL)))
                        """
# some member title must be unique at a given time
# in a given group ministery, parliament, ...
# only one minister, speaker, ...
sql_checkMemberTitleUnique = """
                        SELECT "user_role_types"."user_role_name", "role_titles"."start_date", "role_titles"."end_date" 
                        FROM "public"."role_titles", "public"."user_role_types", "public"."user_group_memberships" 
                        WHERE ( "role_titles"."title_name_id" = "user_role_types"."user_role_type_id" 
                            AND "role_titles"."membership_id" = "user_group_memberships"."membership_id" ) 
                        AND ( ( "role_titles"."title_name_id" = %(title_name_id)s 
                                AND "user_group_memberships"."group_id" = %(group_id)s
                                AND "user_role_types"."user_unique" = True ) )
                        AND  ( ('%(date)s' BETWEEN "role_titles"."start_date" AND "role_titles"."end_date")
                             OR (('%(date)s' >= "role_titles"."start_date" AND "role_titles"."end_date" IS NULL)) ) 
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
    if another session has an 'open end' you cannot add another session to this parliament
    sessions must not overlap
    """    
    #check for overlaps: sessions must not overlap (in this parliament) 
    errors = checkStartEndDatesInInterval(context.__parent__.parliament_id, data , sql_checkSessionInterval)     
    errors = errors + checkDates(context.__parent__ , data )
    #check for open sessions: you may only add a session if all others (in this parliament) are closed
    check_dict = {'parliament_id' : context.__parent__.parliament_id}
    open_session = checkBySQL(sql_checkForOpenSessionInterval , check_dict)
    if open_session:
        errors.append(interface.Invalid(_("The Session (%s) is not yet closed") % open_session, "start_date" ))
      
    return errors

#political parties
def checkPartyDates( self, context, data):
    """
    political groups exist inside a parliament
    """
    return checkDates(context.__parent__ , data )
    
#party membership
def checkPartyMembershipDates( self, context, data ):
    """
    A user can be member of only one party at a time
    """
    errors=[]
    check_dict = {'user_id' : context.__parent__.user_id}
    overlaps = checkBySQL( sql_checkForOpenPartymembership, check_dict)
    if overlaps is not None:
        errors.append(interface.Invalid(_("The person is still a member in (%s)") % overlaps, "start_date" ))    
    if data['start_date']:    
        check_dict['date'] = data['start_date']       
        overlaps = checkBySQL( sql_checkPartymembershipInterval, check_dict)
        if overlaps is not None:
            errors.append(interface.Invalid(_("The person is a member in (%s) at that date") % overlaps, "start_date" ))           
    if data['end_date']:    
        check_dict['date'] = data['end_date']       
        overlaps = checkBySQL( sql_checkPartymembershipInterval, check_dict)
        if overlaps is not None:
            errors.append(interface.Invalid(_("The person is a member in (%s) at that date") % overlaps, "end_date" ))           
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
#Titles for group members
def CheckMemberTitleDateAdd( self, context, data):
    errors =  checkDates(context.__parent__ , data )
    checkdict= { 'title_name_id' : data['title_name_id'] , 
                 'membership_id' : context.__parent__.membership_id}  
    if data['start_date'] is not None:
        checkdict['date'] = data['start_date']                             
        overlaps = checkBySQL(sql_checkMemberTitleDuplicates, checkdict)
        if overlaps:
            errors.append( interface.Invalid(_(u"This persons allready has the title %s") % overlaps, "start_date" ))
    if data['end_date'] is not None:
        checkdict['date'] = data['end_date']                             
        overlaps = checkBySQL(sql_checkMemberTitleDuplicates, checkdict)
        if overlaps:
            errors.append( interface.Invalid(_(u"This persons allready has the title %s") % overlaps, "end_date" ))     
    checkdict = { 'title_name_id' : data['title_name_id'] , 
                  'group_id' : context.__parent__.group_id }
    if data['start_date'] is not None:
        checkdict['date'] = data['start_date']               
        overlaps = checkBySQL(sql_checkMemberTitleUnique, checkdict)
        if overlaps:        
            errors.append( interface.Invalid(_(u"A person with the title %s allready exists") % overlaps, "start_date" ))        
    if data['end_date'] is not None:
        checkdict['date'] = data['end_date'] 
        overlaps=checkBySQL(sql_checkMemberTitleUnique, checkdict)
        if overlaps:     
            errors.append( interface.Invalid(_(u"A person with the title %s allready exists") % overlaps, "end_date" ))                          
                       
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

#XXX
sql_checkForMyOpenPartymembership = """
                            SELECT "groups"."short_name" 
                            FROM "public"."user_group_memberships", "public"."groups", "public"."political_parties" 
                            WHERE ( "user_group_memberships"."group_id" = "groups"."group_id" 
                                   AND "political_parties"."party_id" = "groups"."group_id" ) 
                              AND ( ( "user_group_memberships"."user_id" = %(user_id)s
                                    AND "user_group_memberships"."end_date" IS NULL ) )
                              AND ( "user_group_memberships"."membership_id" != %(parent_key)s )                            
                        """
#XXX                        
sql_checkMyPartymembershipInterval = """
                            SELECT "groups"."short_name" 
                            FROM "public"."user_group_memberships", "public"."groups", "public"."political_parties" 
                            WHERE ( "user_group_memberships"."group_id" = "groups"."group_id" 
                                   AND "political_parties"."party_id" = "groups"."group_id" ) 
                              AND ( ( "user_group_memberships"."user_id" = %(user_id)s )
                                    AND ( '%(date)s' 
                                         BETWEEN "user_group_memberships"."start_date" AND "user_group_memberships"."end_date" ) )
                              AND ( "user_group_memberships"."membership_id" != %(parent_key)s )                                                                     
                        """

# check that a member has the title only once
sql_checkMyMemberTitleDuplicates = """
                        SELECT "user_role_types"."user_role_name", "role_titles"."start_date", "role_titles"."end_date" 
                        FROM "public"."role_titles", "public"."user_role_types" 
                        WHERE ( "role_titles"."title_name_id" = "user_role_types"."user_role_type_id" ) 
                        AND ( ( "role_titles"."title_name_id" = %(title_name_id)s AND "role_titles"."membership_id" = %(membership_id)s ) )
                        AND (('%(date)s' BETWEEN "role_titles"."start_date" AND "role_titles"."end_date")
                             OR (('%(date)s' >= "role_titles"."start_date" AND "role_titles"."end_date" IS NULL)))
                        AND ( "role_titles"."role_title_id" != %(role_title_id)s )
                        """
# some member title must be unique at a given time
# in a given group ministery, parliament, ...
# only one minister, speaker, ...
sql_checkMyMemberTitleUnique = """
                        SELECT "user_role_types"."user_role_name", "role_titles"."start_date", "role_titles"."end_date" 
                        FROM "public"."role_titles", "public"."user_role_types", "public"."user_group_memberships" 
                        WHERE ( "role_titles"."title_name_id" = "user_role_types"."user_role_type_id" 
                            AND "role_titles"."membership_id" = "user_group_memberships"."membership_id" ) 
                        AND ( ( "role_titles"."title_name_id" = %(title_name_id)s 
                                AND "user_group_memberships"."group_id" = %(group_id)s
                                AND "user_role_types"."user_unique" = True ) )
                        AND  ( ('%(date)s' BETWEEN "role_titles"."start_date" AND "role_titles"."end_date")
                             OR (('%(date)s' >= "role_titles"."start_date" AND "role_titles"."end_date" IS NULL)) ) 
                        AND ( "role_titles"."role_title_id" != %(role_title_id)s )                             
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
    errors =  checkDates(context.__parent__.__parent__ , data )
    checkdict= { 'title_name_id' : data['title_name_id'] , 
                 'role_title_id' : context.role_title_id,
                 'membership_id' : context.__parent__.__parent__.membership_id}  
    if data['start_date'] is not None:
        checkdict['date'] = data['start_date']                             
        overlaps = checkBySQL(sql_checkMyMemberTitleDuplicates, checkdict)
        if overlaps:
            errors.append( interface.Invalid(_(u"This persons allready has the title %s") % overlaps, "start_date" ))
    if data['end_date'] is not None:
        checkdict['date'] = data['end_date']                             
        overlaps = checkBySQL(sql_checkMyMemberTitleDuplicates, checkdict)
        if overlaps:
            errors.append( interface.Invalid(_(u"This persons allready has the title %s") % overlaps, "end_date" ))     
    checkdict = { 'title_name_id' : data['title_name_id'] , 
                  'role_title_id' : context.role_title_id ,   
                  'group_id' : context.__parent__.__parent__.group_id }
    if data['start_date'] is not None:
        checkdict['date'] = data['start_date']               
        overlaps = checkBySQL(sql_checkMyMemberTitleUnique, checkdict)
        if overlaps:        
            errors.append( interface.Invalid(_(u"A person with the title %s allready exists") % overlaps, "start_date" ))        
    if data['end_date'] is not None:
        checkdict['date'] = data['end_date'] 
        overlaps=checkBySQL(sql_checkMyMemberTitleUnique, checkdict)
        if overlaps:     
            errors.append( interface.Invalid(_(u"A person with the title %s allready exists") % overlaps, "end_date" ))                          

    return errors         

def QuestionAdd( self, context, data ):
    return []
    
def QuestionEdit( self, context, data ):
    return []

def ResponseEdit( self, context, data ):
    return []

def ResponseAdd ( self, context, data ):
    return []      
        
