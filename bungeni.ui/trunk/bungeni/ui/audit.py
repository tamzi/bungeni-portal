
from zope.publisher.browser import BrowserView
from zope.security.proxy import removeSecurityProxy
from bungeni.core import audit
from sqlalchemy import orm

import sqlalchemy as rdb

class ChangeBaseView( BrowserView ):
    """
    base view for looking at changes to context
    """
    @property
    def _log_table( self ):
        auditor = audit.getAuditor( self.context )
        return auditor.change_table
        
    def getFeedEntries( self ):
        instance = removeSecurityProxy( self.context )        
        mapper = orm.object_mapper( instance )
        
        query = self._log_table.select().where(
            rdb.and_( self._log_table.c.content_id == rdb.bindparam('content_id') )
            ).limit( 20 )
            

        content_id = mapper.primary_key_from_instance( instance )[0] 
        content_changes = query.execute( content_id = content_id )
        return map( dict, content_changes)

class RSS2( ChangeBaseView ):
    """
    RSS Feed for an object
    """

class ChangeLog( ChangeBaseView ):
    """
    Change Log View for an object
    """
    form_name = "Change Log"