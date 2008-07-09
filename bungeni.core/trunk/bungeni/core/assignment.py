"""
$Id: $
"""

from zope import interface
from ore.alchemist import Session
from zope.security.proxy import removeSecurityProxy
from zope.dottedname.resolve import resolve
from sqlalchemy import orm

import interfaces, schema
    
class GroupContextAssignments( object ):
    
    interface.implements( interfaces.IContextAssignments )
    
    def __init__( self, context ):
        self.context = context
        
    def __iter__( self ):
        for i in Session().query( GroupAssignment ).filter_by( group_id = self.context.group_id ):
            yield i
            
class ContentAssignments( object ):
    
    interface.implements( interfaces.IContentAssignments )

    def __init__( self, context):
        self.context = context
        
    def __iter__( self ):
        unwrapped = removeSecurityProxy( self.context )
        mapper = orm.object_mapper( unwrapped )
        primary_key = mapper.primary_key_from_instance( unwrapped )[0]
        
        for i in Session().query( GroupAssignment ).filter_by( 
                object_id = primary_key,
                object_type = unwrapped.__class__.__name__ ):
                yield i
    
class GroupAssignment( object ):

    interface.implements( interfaces.IAssignment )

    @property
    def context( self ):
        return self.group

    @property
    def content( self ):
        content_class = resolve( self.object_type )
        content = Session().query( content_class ).get( self.object_id )
        self.content = content
        return content

orm.mapper( GroupAssignment, schema.group_item_assignments )
            


