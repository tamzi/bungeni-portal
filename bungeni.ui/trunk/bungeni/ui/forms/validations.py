# encoding: utf-8
"""
form validations for custom forms
"""

import datetime
from zope import interface
from bungeni.core.i18n import _

from ore.alchemist import Session

from ore.alchemist.interfaces import IAlchemistContent

import bungeni.models.schema
from bungeni.models import interfaces

import sqlalchemy.orm

from bungeni.ui.queries.utils import check_with_sql, check_date_in_interval, check_start_end_dates_in_interval

import bungeni.ui.queries.sqlvalidation as sql


def null_validator(*args, **kwargs):
    return []


def validate_start_date_within_parent( parent, data ):
    """ Check that the start date is inside the restrictictions.
    It must not start before the contextParents start date or end
    after the contextsParents end date"""
    errors =[]   
    if data['start_date'] is not None:
        if parent.start_date is not None:
            if data['start_date'] < parent.start_date:
                errors.append( interface.Invalid( 
                _(u"Start date must be after (%s)") % parent.start_date , 
                "start_date" ))
        if parent.end_date is not None:
            if data['start_date'] > parent.end_date:
                errors.append( interface.Invalid( 
                _(u"Start date must be prior to (%s)") % parent.end_date , 
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
        if parent.start_date is not None:
            if data['end_date'] < parent.start_date:
                errors.append( interface.Invalid( 
                _(u"End date must be after (%s)")  % parent.start_date , 
                "end_date" ))
        if parent.end_date is not None:
            if data['end_date'] > parent.end_date:
                errors.append( interface.Invalid( 
                _(u"End date must be prior to (%s)") % parent.end_date , 
                "end_date" ))  
    return errors



def _validate_date_range_within_parent( parent, data ):
    """ combine checks for start and end date       
    """
    errors = validate_start_date_within_parent( parent, data )
    errors = errors + validate_end_date_within_parent( parent, data )
    return errors
 
 
 
def validate_date_range_within_parent(self, context, data):
    ctx = context.__parent__
    if not IAlchemistContent.providedBy(ctx):
        ctx=context.__parent__
    _validate_date_range_within_parent(ctx,data)


def check_valid_date_range(action, data, context, container):
    return checkDates(container.__parent__, data)
        
#Parliament

def validate_parliament_dates(data, context):
    if interfaces.IParliament.providedBy(context):
        errors = check_start_end_dates_in_interval(context.parliament_id, 
                data, 
                sql.checkMyParliamentInterval)
        parliament_id = context.parliament_id
        parliament = context
    elif interfaces.IParliamentContainer.providedBy(context):
        errors = check_start_end_dates_in_interval(None, 
                data, 
                sql.checkParliamentInterval)
        parliament_id = None
        parliament = None    
    else:
        raise TypeError
    overlaps = check_date_in_interval(parliament_id, 
                data['election_date'], 
                sql.checkParliamentInterval)
                
    validate_date_in_interval(parliament, domain.Parliament, data['election_date'])
                     
    if (parliament_id is not None) and (overlaps is not None):                
        import pdb; pdb.set_trace()
    if overlaps is not None:
        errors.append(interface.Invalid(
            _("The election date overlaps with (%s)") % overlaps, 
            "election_date" ))   
    overlaps = check_date_in_interval(parliament_id,
                data['election_date'], 
                sql.checkForOpenParliamentInterval )   

    validate_open_interval(parliament, domain.Parliament, data['election_date'])                
    if overlaps is not None:
        errors.append(interface.Invalid(
                _("Another parliament is not yet dissolved (%s)") % overlaps, 
                "election_date" ))            
    return errors    
        
    


def CheckParliamentDatesAdd( self,  context, data ):
    """
    Parliaments must not overlap
    """       
    
    #for parliaments we have to check election date as well


def CheckParliamentDatesEdit( self, context, data ):
    """
    Parliaments must not overlap
    """       
    errors=[]
    #for parliaments we have to check election date as well
    overlaps = check_date_in_interval(
                context.parliament_id, 
                data['election_date'], 
                sql.checkMyParliamentInterval)
    if overlaps is not None:
        errors.append(interface.Invalid(
                        _("The election date overlaps with (%s)") % overlaps, 
                        "election_date" ))   
    overlaps = check_date_in_interval(context.parliament_id, 
                    data['election_date'], 
                    sql.checkForMyOpenParliamentInterval )   
    if overlaps is not None:
        errors.append(interface.Invalid(
                _("Another parliament is not yet dissolved (%s)") % overlaps , 
                "election_date" ))                        
    return errors


def CheckGovernmentsDateInsideParliamentsDatesAdd( self,  context, data ):
    """
    A governmemnt cannot start before the parliament
    but may end after the parliament
    """
    errors = check_start_end_dates_in_interval( None, 
                data, 
                sql.checkGovernmentInterval)
    if (context.__parent__.end_date is not None):
        if data['start_date'] > context.__parent__.end_date:
            errors.append(  interface.Invalid(
            _("Start date cannot be after the parliaments dissolution (%s)" % context.__parent__.end_date ), 
                "start_date") )
    if context.__parent__.start_date > data['start_date']:
        errors.append( interface.Invalid(
            _("Start date must start after the swearing in of the parliament (%s)" % context.__parent__.start_date ), 
                "start_date") )    
    return errors
    
def CheckGovernmentsDateInsideParliamentsDatesEdit( self, context, data ):
    errors = check_start_end_dates_in_interval( context.government_id, data, sql.checkMyGovernmentInterval)
    if (context.__parent__.__parent__.end_date is not None):
        if data['start_date'] > context.__parent__.__parent__.end_date:
            errors.append(  interface.Invalid(_("Start date cannot be after the parliaments dissolution (%s)") % context.__parent__.__parent__.end_date , "start_date") )
    if context.__parent__.__parent__.start_date > data['start_date']:
        errors.append( interface.Invalid(_("Start date must start after the swearing in of the parliament (%s)") % context.__parent__.__parent__.start_date , "start_date") )    
    return errors    




def CheckSessionDatesInsideParentDatesAdd( self,  context, data ):
    """
    Session dates must be inside the parliaments start-end
    if another session has an 'open end' you cannot add another session to 
    this parliament, sessions must not overlap
    """    
    #check for overlaps: sessions must not overlap (in this parliament) 
    errors = check_start_end_dates_in_interval(context.__parent__.parliament_id, data , sql.checkSessionInterval)     
    errors = errors + _validate_date_range_within_parent(context.__parent__ , data )
    #check for open sessions: you may only add a session if all others (in this parliament) are closed
    check_dict = {'parliament_id' : context.__parent__.parliament_id}
    open_session = check_with_sql(sql.checkForOpenSessionInterval , **check_dict)
    if open_session:
        errors.append(interface.Invalid(_("The Session (%s) is not yet closed") % open_session, "start_date" ))
      
    return errors

def CheckSessionDatesEdit( self, context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    errors = check_start_end_dates_in_interval(context.session_id , data , sql.checkMySessionInterval)     
    errors = errors + _validate_date_range_within_parent(context.__parent__.__parent__ , data )       
    return errors


def checkPartyMembershipDates( self, context, data ):
    """
    A user can be member of only one party at a time
    """
    errors=[]
    check_dict = {'user_id' : context.__parent__.user_id}
    overlaps = check_with_sql( sql.checkForOpenPartymembership, **check_dict)
    if overlaps is not None:
        errors.append(interface.Invalid(_("The person is still a member in (%s)") % overlaps, "start_date" ))    
    if data['start_date']:    
        check_dict['date'] = data['start_date']       
        overlaps = check_with_sql( sql.checkPartymembershipInterval, **check_dict)
        if overlaps is not None:
            errors.append(interface.Invalid(_("The person is a member in (%s) at that date") % overlaps, "start_date" ))           
    if data['end_date']:    
        check_dict['date'] = data['end_date']       
        overlaps = check_with_sql( sql.checkPartymembershipInterval, **check_dict)
        if overlaps is not None:
            errors.append(interface.Invalid(_("The person is a member in (%s) at that date") % overlaps, "end_date" ))           
    return errors
    
#sittings

def CheckSittingDatesInsideParentDatesAdd( self,  context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    errors = check_start_end_dates_in_interval(
        context.__parent__.group_id, data, sql.checkSittingGroupInterval)
        
    if context.__parent__.start_date > data['start_date'].date():
        errors.append( interface.Invalid(_("Start must be after Session Start Date (%s)") % context.__parent__.start_date, "start_date" ) )
    if context.__parent__.end_date is not None:
        if data['end_date'].date() > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("End must be before Session End Date (%s)") % context.__parent__.end_date, "end_date" ) )
        if data['start_date'].date() > context.__parent__.end_date:
            errors.append(  interface.Invalid(_("Start must be before Session End Date (%s)") % context.__parent__.end_date, "start_date" ) )
    return errors
def CheckSittingDatesInsideParentDatesEdit( self, context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    #errors = check_start_end_dates_in_interval(context.sitting_id, data, sql.checkMySittingInterval)
    if getattr(context.__parent__.__parent__, 'session_id', None):
        errors = check_start_end_dates_in_interval(context.sitting_id, data, sql.checkMySittingSessionInterval)
    elif getattr(context.__parent__.__parent__, 'group_id', None):          
        errors = check_start_end_dates_in_interval(context.sitting_id, data, sql.checkMySittingGroupInterval)
    
    if context.__parent__.__parent__.start_date > data['start_date'].date():
        errors.append( interface.Invalid(_("Start must be after Session Start Date (%s)") % context.__parent__.__parent__.start_date, "start_date") )
    if context.__parent__.__parent__.end_date is not None:
        if data['end_date'].date() > context.__parent__.__parent__.end_date:
            errors.append(  interface.Invalid(_("End must be before Session End Date (%s)") % context.__parent__.__parent__.end_date, "end_date" ) )
        if data['start_date'].date() > context.__parent__.__parent__.end_date:
            errors.append(  interface.Invalid(_("Start must be before Session End Date (%s)") % context.__parent__.__parent__.end_date, "start_date") )            
    return errors
        
    
#Titles for group members
def CheckMemberTitleDateAdd( self, context, data):
    errors =  _validate_date_range_within_parent(context.__parent__ , data )
    checkdict= { 'title_name_id' : data['title_name_id'] , 
                 'membership_id' : context.__parent__.membership_id}  
    if data['start_date'] is not None:
        checkdict['date'] = data['start_date']                             
        overlaps = check_with_sql(sql.checkMemberTitleDuplicates, **checkdict)
        if overlaps:
            errors.append( interface.Invalid(_(u"This persons allready has the title %s") % overlaps, "start_date" ))
    if data['end_date'] is not None:
        checkdict['date'] = data['end_date']                             
        overlaps = check_with_sql(sql.checkMemberTitleDuplicates, **checkdict)
        if overlaps:
            errors.append( interface.Invalid(_(u"This persons allready has the title %s") % overlaps, "end_date" ))     
    checkdict = { 'title_name_id' : data['title_name_id'] , 
                  'group_id' : context.__parent__.group_id }
    if data['start_date'] is not None:
        checkdict['date'] = data['start_date']               
        overlaps = check_with_sql(sql.checkMemberTitleUnique, **checkdict)
        if overlaps:        
            errors.append( interface.Invalid(_(u"A person with the title %s allready exists") % overlaps, "start_date" ))        
    if data['end_date'] is not None:
        checkdict['date'] = data['end_date'] 
        overlaps=check_with_sql(sql.checkMemberTitleUnique, **checkdict)
        if overlaps:     
            errors.append( interface.Invalid(_(u"A person with the title %s allready exists") % overlaps, "end_date" ))                          
                       
    return errors


#Parliament

def check_parliament_date_no_overlap(action, data, context, container):
    """Parliaments must not overlap."""

    if context is not None:
        parliament_id = context.parliament_id
    else:
        parliament_id = None
        
    errors = checkStartEndDatesInInterval(
        parliament_id, data, sql.checkMyParliamentInterval)
    
    overlaps = checkDateInInterval(
        parliament_id, data['election_date'], sql.checkMyParliamentInterval)
    
    if overlaps is not None:
        errors.append(interface.Invalid(
            _("The election date overlaps with (%s)") % overlaps, "election_date"))
        
    overlaps = checkDateInInterval(
        parliament_id, data['election_date'], sql.checkForMyOpenParliamentInterval)
    
    if overlaps is not None:
        errors.append(interface.Invalid(
            _("Another parliament is not yet dissolved (%s)") % overlaps,
            "election_date"))
        
    return errors

# Governments
def CheckGovernmentsDateInsideParliamentsDatesEdit( self, context, data ):
    """
    start date must be >= parents start date
    """
    errors = checkStartEndDatesInInterval( context.government_id, data, sql.checkMyGovernmentInterval)
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
    #errors = checkStartEndDatesInInterval(context.sitting_id, data, sql.checkMySittingInterval)
    if getattr(context.__parent__.__parent__, 'session_id', None):
        errors = checkStartEndDatesInInterval(context.sitting_id, data, sql.checkMySittingSessionInterval)
    elif getattr(context.__parent__.__parent__, 'group_id', None):          
        errors = checkStartEndDatesInInterval(context.sitting_id, data, sql.checkMySittingGroupInterval)
    
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
    errors = checkStartEndDatesInInterval(context.session_id , data , sql.checkMySessionInterval)     
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
                        
def MinisterDatesEdit( self, context, data ):
    errors = checkDates(context.__parent__.__parent__ , data )       
    return errors                               
                        
def check_valid_date_range(action, data, context, container):
    return checkDates(container.__parent__, data)
    
def CheckMemberTitleDateEdit( self, context, data):
    errors =  _validate_date_range_within_parent(context.__parent__.__parent__ , data )
    checkdict= { 'title_name_id' : data['title_name_id'] , 
                 'role_title_id' : context.role_title_id,
                 'membership_id' : context.__parent__.__parent__.membership_id}  
    if data['start_date'] is not None:
        checkdict['date'] = data['start_date']                             
        overlaps = check_with_sql(sql.checkMyMemberTitleDuplicates, **checkdict)
        if overlaps:
            errors.append( interface.Invalid(_(u"This persons allready has the title %s") % overlaps, "start_date" ))
    if data['end_date'] is not None:
        checkdict['date'] = data['end_date']                             
        overlaps = check_with_sql(sql.checkMyMemberTitleDuplicates, **checkdict)
        if overlaps:
            errors.append( interface.Invalid(_(u"This persons allready has the title %s") % overlaps, "end_date" ))     
    checkdict = { 'title_name_id' : data['title_name_id'] , 
                  'role_title_id' : context.role_title_id ,   
                  'group_id' : context.__parent__.__parent__.group_id }
    if data['start_date'] is not None:
        checkdict['date'] = data['start_date']               
        overlaps = check_with_sql(sql.checkMyMemberTitleUnique, **checkdict)
        if overlaps:        
            errors.append( interface.Invalid(_(u"A person with the title %s allready exists") % overlaps, "start_date" ))        
    if data['end_date'] is not None:
        checkdict['date'] = data['end_date'] 
        overlaps=check_with_sql(sql.checkMyMemberTitleUnique, **checkdict)
        if overlaps:     
            errors.append( interface.Invalid(_(u"A person with the title %s allready exists") % overlaps, "end_date" ))                          

    return errors         

