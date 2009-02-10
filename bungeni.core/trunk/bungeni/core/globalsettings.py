#!/usr/bin/env python
# encoding: utf-8
"""
global settings
"""


# the schema for the settings is in interfaces

import datetime

import sqlalchemy.sql.expression as sql
from ore.alchemist import Session

from bungeni.core.i18n import _
from bungeni.core.app import BungeniApp

from bungeni.models import domain
from bungeni.models import schema
from bungeni.models import settings
from bungeni.models.interfaces import IBungeniSettings
from bungeni.models.settings import GlobalSettingFactory

app = BungeniApp()                


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
    email = settings.BungeniSettings(app).speakers_office_email
    return email
    
def getSpeakersOfficeRecieveNotification():
    """
    returns true if the Speakers office wants to be alerted by mail
    whenever a bill, motion, question is submitted 
    """
    return settings.BungeniSettings(app).speakers_office_notification
            
def getClerksOfficeEmail():        
    """
    return the official email address 
    of the clerks office
    """
    return settings.BungeniSettings(app).clerks_office_email
    
def getClerksOfficeRecieveNotification():
    """
    returns true if the clerks office wants to be alerted by mail
    whenever a bill, motion, question is submitted 
    """
    return settings.BungeniSettings(app).clerks_office_notification             
    
    
def getAdministratorsEmail():
    """
    email of the site admin
    """
    return settings.BungeniSettings(app).administrators_email    
        
        
def getDaysToDeferAdmissibleQuestions():
    """
    time after which admissible questions are automatically deferred
    """       
     
    return datetime.timedelta(settings.BungeniSettings(app).days_to_defer_question)    
    
def getDaysToNotifyMinistriesQuestionsPendingResponse():
    """
    timeframe after which the clerksoffice and the ministry is alerted that
    questions that are pending response are not yet answered
    """    
    
    return datetime.timedelta(settings.BungeniSettings(app).days_to_notify_ministry_unanswered)  
  
def getQuestionSubmissionAllowed():
    return settings.BungeniSettings(app).question_submission_allowed
    
def getMaxQuestionsPerSitting():
    return settings.BungeniSettings(app).max_questions_sitting
        
def getMaxQuestionsByMpPerSitting():
    return settings.BungeniSettings(app).max_mp_questions_sitting
    
def getNoOfDaysBeforeQuestionSchedule():
    return settings.BungeniSettings(app).days_before_question_schedule
    
    
def getNoOfDaysBeforeBillSchedule():
    """
    Parameter  : Elapsed days from date of publication for placement of bill	
    Configurable numeric value describing number of days after date of publication 
    of bill after which bill can be placed before the house
    """
    return settings.BungeniSettings(app).days_before_bill_schedule
        
def getWeekendDays():
    """
    (0 is Monday, 6 is Sunday)
    """
    return [5,6]

def getFirstDayOfWeek():
    """
    (0 is Monday, 6 is Sunday)
    """
    return 0        

def getPloneMenuUrl():
    """
    URL at which the plone menu is returned as a json string
    """

    raise NotImplementedError(
        "This method should not be used.")    

BungeniSettings = GlobalSettingFactory(IBungeniSettings)
