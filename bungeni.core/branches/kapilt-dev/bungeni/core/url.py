from ore.alchemist.interfaces import IAlchemistContainer, IAlchemistContent
from ore.alchemist import container 
from zope.location.interfaces import ILocation
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.security.proxy import removeSecurityProxy
import urllib

_safe = '@+' # Characters that we don't want to have quoted


class AbsoluteURL( object ):
    
    def __init__( self, context, container, request ):
        self.context = context
        self.container = container
        self.request = request
        
    def __str__( self ):
        url = self.request.getApplicationURL()
        path_fragment = self.resolveContainerURL()
        obj_fragment  = container.stringKey( self.context )
        return url + path_fragment + "/" + obj_fragment
    
    __call__ = __str__
        
    def breadcrumbs( self ):
        return ()

    def resolveContainerURL( self ):
        # should make this defer to attach absolute url adapters
        # on container like zope.traversing.browser.absoluteurl does
        # 
        ob = self.container
        root = self.request.getVirtualHostRoot()
        steps = []
        while (ob is not root) and (ob is not None):
            ob = ILocation( ob )
            if not ob:
                break
            name = ob.__name__
            if not name:
                break
            name = urllib.quote(name.encode('utf-8'), _safe)
            steps.insert( 0, name )
            ob = ob.__parent__
            
        return "/".join( steps )
        
class AbsoluteURLFactory( object ):
    """
    uses containenment urls to dereference objects to their canonical urls
    """
    def __init__( self, app):   
        self.class_container_map = {}        
        def wire( ):
            for k,v in app.items():
                if IAlchemistContainer.providedBy( v ):
                    self.class_container_map[ v.domain_model ] = v
        wire()
        
    def __call__( self, context, request ):
        trusted_ctx = removeSecurityProxy( context )
        container = self.class_container_map.get( trusted_ctx.__class__ )
        if container is None:
            assert IAlchemistContent.providedBy( trusted_ctx ), "invalid canonical url candidate"
            raise SyntaxError("invalid class map for %r"%(trusted_ctx.__class__) )
        url = AbsoluteURL( context, container, request )

