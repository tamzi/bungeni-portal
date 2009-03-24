# encoding: utf-8
import datetime
from zope import interface
from zope.schema.interfaces import IContextSourceBinder
from zope.schema import vocabulary
from zope.security.proxy import removeSecurityProxy

from ore.alchemist import Session
from ore.alchemist.container import valueKey
from ore.alchemist.container import stringKey

import bungeni.models.domain as domain
from bungeni.ui.i18n import _
import bungeni.models.schema as db_schema
from sqlalchemy import sql


def execute_sql(sql_statement, **kwargs):
    session = Session()
    connection = session.connection(domain.Parliament)
    query = connection.execute(sql.text(sql_statement), **kwargs)
    return query
     
     
def get_user_id( name ):
    session = Session()
    userq = session.query(domain.User).filter(db_schema.users.c.login == name )
    results = userq.all()
    if results:
        user_id = results[0].user_id
    else:
        user_id = None
    return user_id      


def check_with_sql( sql_statement, **check_dict):
    """
    Run SQL with variables in the dict
    """
    query = execute_sql(sql_statement, **check_dict)
    result = query.fetchone()
    if result is None:
        return result
    else:
        return result[0]            

def check_date_in_interval( pp_key, checkDate, sql_statement):
    """
    Check if the checkDate is inside one of its 'peers'
    the passed sql statement must follow the restrictions:
    date: is the date to check (must be present!)
    parent_key: is usually the parents primary key (can be omitted to check all)
    """
    if (type(checkDate) is datetime.datetime or type(checkDate) is datetime.date):
        checkDict = { 'date': checkDate, 'parent_key': pp_key }
        return check_with_sql( sql_statement, **checkDict)
    else:
        raise TypeError        


def check_start_end_dates_in_interval( pp_key, data, sql_statement):
    """ 
    Check if start and end dates are not overlapping with a prior or later peer
    """
    errors =[]    
    overlaps = check_date_in_interval(pp_key, data['start_date'], sql_statement)
    if overlaps is not None:
        errors.append( interface.Invalid(_("The start date overlaps with (%s)" % overlaps), "start_date" ))
    if data['end_date'] is not None:        
        overlaps = check_date_in_interval(pp_key, data['end_date'], sql_statement)
        if overlaps is not None:
            errors.append( interface.Invalid(_("The end date overlaps with (%s)" % overlaps), "end_date" )) 
    return errors 


def validate_date_in_interval(obj, domain_model, date):
    session = Session()
    query = session.query(domain_model).filter(
            sql.expression.between(date, domain_model.start_date, domain_model.end_date)
            )
    results = query.all() 
    if results:      
        if obj:
            # the object itself can overlap   
            for result in results:
                if stringKey(result) == stringKey(obj):
                    continue
                else:
                    yield result                
        else:
            # all results indicate an error
           for result in results:     
                yield result     

def validate_open_interval(obj, domain_model):
    session = Session()
    query = session.query(domain_model).filter(
            domain_model.end_date == None)
    results = query.all() 
    if results:      
        if obj:
            for result in results:
                if stringKey(result) == stringKey(obj):
                    continue
                else:
                    yield result                
        else:
           for result in results:     
                yield result


def validate_membership_in_interval(obj, domain_model, date, user_id):
    """ validates the start end for a specific user"""
    session = Session()
    query = session.query(domain_model).filter(
            sql.expression.and_(
            sql.expression.between(date, domain_model.start_date, domain_model.end_date),
            domain_model.user_id == user_id)
            )
    results = query.all() 
    if results:      
        if obj:
            for result in results:
                if stringKey(result) == stringKey(obj):
                    continue
                else:
                    yield result                
        else:
           for result in results:     
                yield result    
    
    
def validate_open_membership(obj, domain_model, user_id):
    session = Session()
    query = session.query(domain_model).filter(
            sql.expression.and_(
            domain_model.end_date == None,
            domain_model.user_id == user_id)
            )
    results = query.all() 
    if results:      
        if obj:
            for result in results:
                if stringKey(result) == stringKey(obj):
                    continue
                else:
                    yield result                
        else:
           for result in results:     
                yield result





class SQLQuerySource ( object ):
    """ Call with a SQL Statement and the rows which make up the vocabulary
    note that a % wildcard for sql LIKEs must be escaped as %%
   
    Values passed in the filter dictionary can be either constant strings 
    or they can refer to an attribute of the object. To denote the attribute 
    pass the attributes name with a leading dollar sign i.e: $member_id
     
    The value of the primary key of the *parent(!)* 
    can be accessed with :primary_key
       
    You can call this function without filters on any object, 
    if you need filters the object needs to have a context i.e, 
    you can call it on edit/view for any object. If you want to add an object
    it must be a childobject of something.
    """
    
    interface.implements( IContextSourceBinder )   

        
    def getValueKey(self, context):
        """ Iterate through the parents until you get a valueKey 
        """
        if context.__parent__ is None:
            return None
        else:            
            try:
                value_key = valueKey( context.__parent__.__name__ )[0]
            except:
                value_key = self.getValueKey( context.__parent__)
        return value_key          
    
    def __init__( self, sql_statement, token_field, value_field, filter = {}, title_field=None ):
        self.sql_statement = sql_statement
        self.token_field = token_field
        self.value_field = value_field
        self.title_field = title_field
        self.filter = filter
    
    def constructFilterDict( self, filter_dict, context ):
        """
        replace the variable filtervalues with attribute values of the 
        current context object
        """
        trusted=removeSecurityProxy(context)
        filter = {}
        for key in filter_dict.keys():
            if str(filter_dict[key]).startswith('$'):              
                value =filter_dict[key][1:]
                filter_dict[key] = trusted.__dict__[value]                
        return filter_dict                
        
        
        
    def constructQuery( self, context ):        
        session = Session()            
        if  self.sql_statement.find(':primary_key') > 1:
            #if the keyword primary key is present in the sql 
            #replace it with the parent pk  
            pfk = self.getValueKey(context)
            filter_dict = {'primary_key' : pfk}            
        else:
            filter_dict = {}            
        filter_dict.update(self.filter)
        filter_dict = self.constructFilterDict( filter_dict, context )      
        query = execute_sql(self.sql_statement, **filter_dict)
        return query
        
    def __call__( self, context=None ):
        query = self.constructQuery( context )
        results = query.fetchall()
        
        terms = []
        title_field = self.title_field or self.token_field
        for ob in results:
            terms.append( 
                vocabulary.SimpleTerm( 
                    value = getattr( ob, self.value_field), 
                    token = getattr( ob, self.token_field),
                    title = getattr( ob, title_field) ,
                    ))
                    
        return vocabulary.SimpleVocabulary( terms )
        


