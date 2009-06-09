from bungeni.core.workflows import utils
from bungeni.core.workflows import dbutils

class conditions:
    @staticmethod
    def has_end_date(info, context):
        return context.end_date != None

    
class actions:
    @staticmethod
    def create(info, context):
        user_id = utils.getUserId()
        if user_id:
            zope.securitypolicy.interfaces.IPrincipalRoleMap( context 
                ).assignRoleToPrincipal( u'bungeni.Owner', user_id) 
                
    @staticmethod
    def activate(info, context):
        pass
    
    @staticmethod
    def dissolve(info, context):                
        pass
