from bungeni.core import interfaces
import common

class UserFormatter( common.AjaxTableFormatter ):
    
    i = interfaces.IUser
    
    fields = [ i['login'], i['first_name'], i['last_name'], i['national_id'], i['email'] ]
    
    def getFields( self ):
        return self.fields
        #return super( UserListing, self).getFields()

class UserListing( common.AjaxContainerListing ):
    formatter_factory = UserFormatter

class Index( object ):
    pass



