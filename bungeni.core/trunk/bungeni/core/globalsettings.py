#!/usr/bin/env python
# encoding: utf-8
"""
global settings
"""

#XXX For the time being for test purposes everything is hardcoded here.
#this is to be moved into the DB


    
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
        
        
