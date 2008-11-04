import time

from zope import schema, component
from zope.publisher.browser import BrowserView
from zope.formlib import form
from bungeni.core import domain, interfaces
from alchemist.ui import content

import common, search
from browser import table

class UserFormatter( common.AjaxTableFormatter ):
    i = interfaces.IUser
    fields = [ i['login'], i['first_name'], i['last_name'],
               i['email'], i['national_id'],
               schema.TextLine(title=u"Type", __name__='type' )
               ]
    def getFields( self ):
        return self.fields

class UserListing( common.AjaxContainerListing ):
    formatter_factory = UserFormatter

class UserQueryJSON( search.ConstraintQueryJSON ):
    def getConstraintQuery( self ):
        return self.searcher.query_field("object_kind", domain.User.__name__ )

class GroupFormatter( common.AjaxTableFormatter ):
    i = interfaces.IGroup
    fields = [i['short_name'],i['full_name'], i['start_date'], i['end_date'], 
              schema.TextLine(title=u"Type", __name__='type' )]
    def getFields( self ):
        return self.fields

class GroupListing( common.AjaxContainerListing ):
    formatter_factory = GroupFormatter

class GroupQueryJSON( search.ConstraintQueryJSON ):
    def getConstraintQuery( self ):
        return self.searcher.query_field("object_kind", domain.Group.__name__ )

class Index( BrowserView ):
    pass

class Settings( content.EditForm ):

    form_fields = form.Fields( interfaces.IBungeniSettings )
        
    def update( self ):
        settings = component.getUtility( interfaces.IBungeniSettings )()
        self.adapters = { interfaces.IBungeniSettings : settings }
        super( Settings, self).update()
        
class UserSettings( content.EditForm ):

    form_fields = form.Fields( interfaces.IBungeniUserSettings, interfaces.IUser )
    form_fields = form_fields.omit( 'user_id', 'login', 'date_of_death','status')
    
    def update( self ):
        settings = interfaces.IBungeniUserSettings( self.request.principal, None )
        if settings is None:
            raise SyntaxError("User Settings Only For Database Users")
        self.adapters = { interfaces.IBungeniUserSettings : settings,
                          interfaces.IUser : self.request.principal }
        
        super( UserSettings, self).update()
    







