#!/usr/bin/env python
# encoding: utf-8
"""
global settings
"""

#XXX For the time being for test purposes everything is hardcoded here.
#this is to be moved into the DB

import sqlalchemy.sql.expression as sql
from ore.alchemist import Session

import bungeni.core.domain as domain
import bungeni.core.schema as schema
from bungeni.core.i18n import _

import datetime

def getCurrentParliamentId(date = None):
    """
    returns the current parliament_id for a given date
    or for the current if the date is not given
    """
    def getFilter(date):
        return sql.or_(
            sql.between(date, schema.groups.c.start_date, schema.groups.c.end_date),
            sql.and_( schema.groups.c.start_date <= date, schema.groups.c.end_date == None)
            )
    
    if not date:
        date = datetime.date.today()
    session = Session() 
    query = session.query(domain.Parliament).filter(getFilter(date))   
    result = None
    try:
        result = query.one()
    except:
        pass #XXX raise( _(u"inconsistent data: none or more than one parliament found for this date"))       
    if result:        
        return result.parliament_id
        

    
def getSpeakersOfficeEmail():
    """
    return the official email address 
    of the speakers office
    """
    return "speakers.office@parliament.gov.ke"
    
def getSpeakersOfficeRecieveNotification():
    """
    returns true if the Speakers office wants to be alerted by mail
    whenever a bill, motion, question is submitted 
    """
    return True   
            
def getClerksOfficeEmail():        
    """
    return the official email address 
    of the clerks office
    """
    return "clerks.office@parliament.gov.ke"
    
def getClerksOfficeRecieveNotification():
    """
    returns true if the clerks office wants to be alerted by mail
    whenever a bill, motion, question is submitted 
    """
    return True                
    
    
def getAdministratorsEmail():
    """
    email of the site admin
    """
    return "webmaster@parliament.gov.ke"        
        
        
