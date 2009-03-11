# encoding: utf-8
"""
form validations for custom forms
"""

import datetime
from zope import interface
from bungeni.core.i18n import _

from ore.alchemist import Session

import bungeni.models.schema
import sqlalchemy.orm

from bungeni.ui.queries.utils import checkBySQL, checkDateInInterval, checkStartEndDatesInInterval

import bungeni.ui.queries.sqlvalidation as sql


##############
# Validate if start/end dates are in the date range of its peers 



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
    errors = checkStartEndDatesInInterval(None, data, sql.checkParliamentInterval)
    #for parliaments we have to check election date as well
    overlaps = checkDateInInterval(None, data['election_date'], sql.checkParliamentInterval)
    if overlaps is not None:
        errors.append(interface.Invalid(_("The election date overlaps with (%s)") % overlaps, "election_date" ))   
    overlaps = checkDateInInterval(None, data['election_date'], sql.checkForOpenParliamentInterval )   
    if overlaps is not None:
        errors.append(interface.Invalid(_("Another parliament is not yet dissolved (%s)") % overlaps, "election_date" ))            
    return errors

def CheckParliamentDatesAdd1( self, context, data ):
    """
    Parliaments must not overlap
    """       
    errors = checkStartEndDatesInInterval(None, data, sql.checkParliamentInterval)
    #for parliaments we have to check election date as well
    overlaps = checkDateInInterval(None, data['election_date'], sql.checkParliamentInterval)
    if overlaps is not None:
        errors.append(interface.Invalid(_("The election date overlaps with (%s)") % overlaps, "election_date" ))   
    overlaps = checkDateInInterval(None, data['election_date'], sql.checkForOpenParliamentInterval )   
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
    errors = checkStartEndDatesInInterval( None, data, sql.checkGovernmentInterval)
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
    errors = checkStartEndDatesInInterval(context.__parent__.parliament_id, data , sql.checkSessionInterval)     
    errors = errors + checkDates(context.__parent__ , data )
    #check for open sessions: you may only add a session if all others (in this parliament) are closed
    check_dict = {'parliament_id' : context.__parent__.parliament_id}
    open_session = checkBySQL(sql.checkForOpenSessionInterval , check_dict)
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
    overlaps = checkBySQL( sql.checkForOpenPartymembership, check_dict)
    if overlaps is not None:
        errors.append(interface.Invalid(_("The person is still a member in (%s)") % overlaps, "start_date" ))    
    if data['start_date']:    
        check_dict['date'] = data['start_date']       
        overlaps = checkBySQL( sql.checkPartymembershipInterval, check_dict)
        if overlaps is not None:
            errors.append(interface.Invalid(_("The person is a member in (%s) at that date") % overlaps, "start_date" ))           
    if data['end_date']:    
        check_dict['date'] = data['end_date']       
        overlaps = checkBySQL( sql.checkPartymembershipInterval, check_dict)
        if overlaps is not None:
            errors.append(interface.Invalid(_("The person is a member in (%s) at that date") % overlaps, "end_date" ))           
    return errors
    
#sittings

def CheckSittingDatesInsideParentDatesAdd( self,  context, data ):
    """
    start date must be >= parents start date
    end date must be <= parents end date (if parents end date is set)
    """
    errors = checkStartEndDatesInInterval(
        context.__parent__.group_id, data, sql.checkSittingGroupInterval)
        
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
        overlaps = checkBySQL(sql.checkMemberTitleDuplicates, checkdict)
        if overlaps:
            errors.append( interface.Invalid(_(u"This persons allready has the title %s") % overlaps, "start_date" ))
    if data['end_date'] is not None:
        checkdict['date'] = data['end_date']                             
        overlaps = checkBySQL(sql.checkMemberTitleDuplicates, checkdict)
        if overlaps:
            errors.append( interface.Invalid(_(u"This persons allready has the title %s") % overlaps, "end_date" ))     
    checkdict = { 'title_name_id' : data['title_name_id'] , 
                  'group_id' : context.__parent__.group_id }
    if data['start_date'] is not None:
        checkdict['date'] = data['start_date']               
        overlaps = checkBySQL(sql.checkMemberTitleUnique, checkdict)
        if overlaps:        
            errors.append( interface.Invalid(_(u"A person with the title %s allready exists") % overlaps, "start_date" ))        
    if data['end_date'] is not None:
        checkdict['date'] = data['end_date'] 
        overlaps=checkBySQL(sql.checkMemberTitleUnique, checkdict)
        if overlaps:     
            errors.append( interface.Invalid(_(u"A person with the title %s allready exists") % overlaps, "end_date" ))                          
                       
    return errors





#Parliament

def CheckParliamentDatesEdit( self, context, data ):
    """
    Parliaments must not overlap
    """       
    errors = checkStartEndDatesInInterval(context.parliament_id, data, sql.checkMyParliamentInterval)
    #for parliaments we have to check election date as well
    overlaps = checkDateInInterval(context.parliament_id, data['election_date'], sql.checkMyParliamentInterval)
    if overlaps is not None:
        errors.append(interface.Invalid(_("The election date overlaps with (%s)") % overlaps, "election_date" ))   
    overlaps = checkDateInInterval(context.parliament_id, data['election_date'], sql.checkForMyOpenParliamentInterval )   
    if overlaps is not None:
        errors.append(interface.Invalid(_("Another parliament is not yet dissolved (%s)") % overlaps , "election_date" ))                        
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
        overlaps = checkBySQL(sql.checkMyMemberTitleDuplicates, checkdict)
        if overlaps:
            errors.append( interface.Invalid(_(u"This persons allready has the title %s") % overlaps, "start_date" ))
    if data['end_date'] is not None:
        checkdict['date'] = data['end_date']                             
        overlaps = checkBySQL(sql.checkMyMemberTitleDuplicates, checkdict)
        if overlaps:
            errors.append( interface.Invalid(_(u"This persons allready has the title %s") % overlaps, "end_date" ))     
    checkdict = { 'title_name_id' : data['title_name_id'] , 
                  'role_title_id' : context.role_title_id ,   
                  'group_id' : context.__parent__.__parent__.group_id }
    if data['start_date'] is not None:
        checkdict['date'] = data['start_date']               
        overlaps = checkBySQL(sql.checkMyMemberTitleUnique, checkdict)
        if overlaps:        
            errors.append( interface.Invalid(_(u"A person with the title %s allready exists") % overlaps, "start_date" ))        
    if data['end_date'] is not None:
        checkdict['date'] = data['end_date'] 
        overlaps=checkBySQL(sql.checkMyMemberTitleUnique, checkdict)
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
        
