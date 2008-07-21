import time

from zope import schema
from zope.publisher.browser import BrowserView
from bungeni.core import domain, interfaces

import common, search

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
    fields = [i['short_name'], i['start_date'], i['end_date'], 
              schema.TextLine(title=u"Type", __name__='type' )]
    def getFields( self ):
        return self.fields

class UserQueryJSON( search.ConstraintQueryJSON ):
    def getConstraintQuery( self ):
        return self.searcher.query_field("object_kind", domain.Group.__name__ )

class Index( BrowserView ):
    pass



