# encoding: utf-8

import bungeni.core.workflows.utils as utils

def create(info,context):
    utils.setBillSubmissionDate( info, context )
    utils.setParliamentId(info, context)

def submit( info,context ):
    utils.setBillPublicationDate( info, context )
    utils.setSubmissionDate(info, context)
    bill = removeSecurityProxy(context)
    #rpm = zope.securitypolicy.interfaces.IRolePermissionMap( bill )
    #rpm.grantPermissionToRole( 'bungeni.bill.view', u'bungeni.Everybody' )
    #rpm.denyPermissionToRole( 'bungeni.motion.edit', u'bungeni.Owner' )
    #rpm.denyPermissionToRole( 'bungeni.motion.delete', u'bungeni.Owner' )
    
def withdraw(info,context):
    pass
    
def schedule_first( info,context ):    
    pass
    
def postpone_first( info,context ):
    pass
    
