"""
$Id: $
"""
from zope import interface, schema, event

from sqlalchemy import orm
from ore.alchemist import container, model, Session
from zope.security.proxy import removeSecurityProxy

from i18n import _

from bungeni.models import domain

import interfaces


class Versioned( container.PartialContainer ):
    
    interface.implements( interfaces.IVersioned )
    
    def _copyFields( self, source, dest, iface ):
        for field in schema.getFields( iface ).values():
            value = field.query( source ) 
            if value is None:
                continue
            field.set( dest, value )
            
    def create( self, message, manual = False ):
        """
        store the existing state of the adapted context as a new version
        """
        version = self.domain_model()
        trusted_ctx = removeSecurityProxy( self.__parent__ )
        ctx_class = trusted_ctx.__class__
        
        # set values on version from context
        self._copyFields(  trusted_ctx, version,
                           model.queryModelInterface( ctx_class ) )
        
        # content domain ids are typically not in the interfaces
        # manually inspect and look for one, by hand to save on the new version
        mapper = orm.object_mapper( trusted_ctx )
        version.content_id = mapper.primary_key_from_instance( trusted_ctx )[0]
        
        version.manual = manual
        
        # we rely on change handler to attach the change object to the version
        event.notify( interfaces.VersionCreated( self.__parent__, self, version, message  ) )
        
        # save our new version to the db
        session = Session()
        session.add( version )
        
    def revert( self, version, message ):
        """
        revert the current state of the adapted object to the values specified
        in version, and create a new version with reverted state. 
        """
        trusted_ctx = removeSecurityProxy( self.__parent__ )
        ctx_class = trusted_ctx.__class__        
        has_wf_status = getattr(trusted_ctx,'status',None)
        if has_wf_status:
            wf_status = trusted_ctx.status
        # set values on version from context
        self._copyFields(  version, self.__parent__,
                           model.queryModelInterface( ctx_class ) )                  
        if has_wf_status:
            trusted_ctx.status = wf_status                                       
        msg = (_(u"reverted to previous version %s") %(version.version_id)) + u" - " + message        
        event.notify( interfaces.VersionReverted( self.__parent__, self, version, msg  ) )
        self.create( message=msg )

class ContentVersionsFactory( object ):

    def __call__( self, context ):
        content_version_class = getattr( domain, context.__class__.__name__ + "Version" )
        versions = Versioned()
        versions._class = content_version_class 
        trusted_ctx = removeSecurityProxy( context )
        mapper = orm.object_mapper( trusted_ctx )
        pk_value = mapper.primary_key_from_instance( trusted_ctx )[0]
        versions.setQueryModifier( content_version_class.c[ "content_id" ] == pk_value )
        versions.__parent__ = context
        versions.__name__ = 'versions'
        return versions

ContextVersioned = ContentVersionsFactory()

