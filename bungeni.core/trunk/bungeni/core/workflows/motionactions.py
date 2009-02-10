# encoding: utf-8

import zope.securitypolicy.interfaces
import bungeni.core.workflows.utils as utils


def denyAllWrites(motion):
    """
    remove all rights to change the question from all involved roles
    """
#    rpm = zope.securitypolicy.interfaces.IRolePermissionMap( motion )
#    rpm.denyPermissionToRole( 'bungeni.motion.edit', u'bungeni.Owner' )
#    rpm.denyPermissionToRole( 'bungeni.motion.edit', u'bungeni.Clerk' )
#    rpm.denyPermissionToRole( 'bungeni.motion.edit', u'bungeni.Speaker' )
#    rpm.denyPermissionToRole( 'bungeni.motion.edit', u'bungeni.MP' )
#    rpm.denyPermissionToRole( 'bungeni.motion.delete', u'bungeni.Owner' )
#    rpm.denyPermissionToRole( 'bungeni.motion.delete', u'bungeni.Clerk' )
#    rpm.denyPermissionToRole( 'bungeni.motion.delete', u'bungeni.Speaker' )
#    rpm.denyPermissionToRole( 'bungeni.motion.delete', u'bungeni.MP' )    


def postpone(info,context):
    utils.setMotionHistory(info,context)

def create( info, context ):
    user_id = utils.getUserId()
    if not user_id:
        user_id ='-'
    zope.securitypolicy.interfaces.IPrincipalRoleMap( context ).assignRoleToPrincipal( u'bungeni.Owner', user_id)   
    utils.setParliamentId(info, context)

def submit( info, context ):
    utils.setSubmissionDate(info, context)
#    motion = removeSecurityProxy(context)
#    rpm = zope.securitypolicy.interfaces.IRolePermissionMap( motion )
#    rpm.grantPermissionToRole( 'bungeni.motion.view', u'bungeni.Clerk' )
#    rpm.denyPermissionToRole( 'bungeni.motion.edit', u'bungeni.Owner' )
#    rpm.denyPermissionToRole( 'bungeni.motion.delete', u'bungeni.Owner' )
    
def recieved_by_clerk( info, context ):
    utils.createVersion(info, context)   
#    motion = removeSecurityProxy(context)     
#    zope.securitypolicy.interfaces.IRolePermissionMap( motion ).grantPermissionToRole( 'bungeni.motion.edit', u'bungeni.Clerk' )
    
def require_edit_by_mp( info, context ):
    utils.createVersion(info,context)
#    motion = removeSecurityProxy(context)
#    rpm = zope.securitypolicy.interfaces.IRolePermissionMap( motion )
#    rpm.grantPermissionToRole( 'bungeni.motion.edit', u'bungeni.Owner' )
#    rpm.denyPermissionToRole( 'bungeni.motion.edit', u'bungeni.Clerk' )   
    
def complete( info, context ):
    utils.createVersion(info,context)
#    motion = removeSecurityProxy(context)
#    rpm = zope.securitypolicy.interfaces.IRolePermissionMap( motion )
#    rpm.grantPermissionToRole( 'bungeni.motion.view', u'bungeni.Speaker' )
#    rpm.denyPermissionToRole( 'bungeni.motion.edit', u'bungeni.Clerk' )     

def approve( info, context ):
    #motion = removeSecurityProxy(context)
    #rpm = zope.securitypolicy.interfaces.IRolePermissionMap( motion )    
    #rpm.grantPermissionToRole( 'bungeni.motion.edit', u'bungeni.Speaker' )
    #rpm.grantPermissionToRole( 'zope.View', u'zope.Anybody')
    #rpm.grantPermissionToRole( 'bungeni.motion.view', u'zope.Everybody')
    utils.setApprovalDate(info,context)
    
    
def reject( info, context ):
    #motion = removeSecurityProxy(context)
    #denyAllWrites(motion)
    pass
    
def require_amendment( info, context ):
    utils.createVersion(info,context)
    #motion = removeSecurityProxy(context)
    #rpm = zope.securitypolicy.interfaces.IRolePermissionMap( motion )
    #rpm.grantPermissionToRole( 'bungeni.motion.edit', u'bungeni.Clerk' )
    #rpm.denyPermissionToRole( 'bungeni.motion.edit', u'bungeni.Speaker' ) 
    
def complete_clarify( info, context ):
    utils.createVersion(info,context)
    #motion = removeSecurityProxy(context)
    #rpm = zope.securitypolicy.interfaces.IRolePermissionMap( motion )
    #rpm.grantPermissionToRole( 'bungeni.motion.view', u'bungeni.Speaker' )
    #rpm.denyPermissionToRole( 'bungeni.motion.edit', u'bungeni.Clerk' ) 
    
def mp_clarify( info, context ):
    utils.createVersion(info,context)
    #motion = removeSecurityProxy(context)
    #rpm = zope.securitypolicy.interfaces.IRolePermissionMap( motion )
    #rpm.grantPermissionToRole( 'bungeni.motion.edit', u'bungeni.Owner' )
    #rpm.denyPermissionToRole( 'bungeni.motion.edit', u'bungeni.Clerk' )   
        
def schedule( info, context ):
    pass
def defer( info, context):
    pass
def elapse( info, context ):
    pass
def schedule( info, context ):
    pass
def debate( info, context ):
    pass
    
def withdraw( info, context ):
    #motion = removeSecurityProxy(context)
    #denyAllWrites(motion)    
    pass
    

