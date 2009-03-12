# encoding: utf-8

import bungeni.core.workflows.utils as utils
import zope.securitypolicy.interfaces

class actions:
    @staticmethod
    def create( info, context ):
        """
        on creation the owner is given edit and view rights
        """
        user_id = utils.getUserId()
        if not user_id:
            user_id ='-'    
        zope.securitypolicy.interfaces.IPrincipalRoleMap( context ).assignRoleToPrincipal( u'bungeni.Owner', user_id)     


    @staticmethod
    def submit( info, context ):   
        """
        the response is submitted to the clerks office for review
        the clerks offic can edit the response, the owner looses
        his edit rights.
        """
        utils.submitResponse(info,context)


    @staticmethod
    def complete( info, context ):
        """
        the response was reviewed and finalized by the clerks 
        office, it is now published.    
        """
        utils.publishResponse(info,context)


