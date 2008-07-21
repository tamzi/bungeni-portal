"""
xapian indexing adapters
"""
from zope import interface, schema
from zope.dottedname import resolve
import xappy, os, os.path as path

from ore.alchemist import container
from sqlalchemy.orm.session import Session
from ore.xapian import queue, search, interfaces as iindex

import logging
import domain
import interfaces

log = logging.getLogger('bungeni.index')

# we store indexes in buildout/parts/index
# 
def setupStorageDirectory( ):
    # we start in buildout/src/bungeni.core/bungeni/core
    # we end in buildout/parts/index    
    store_dir = __file__
    x = 0
    while x < 5:
        x += 1
        store_dir = path.split( store_dir )[0]
    store_dir = path.join( store_dir, 'parts', 'index')
    if path.exists( store_dir ):
        assert path.isdir( store_dir )
    else:
        os.mkdir( store_dir )
    
    return store_dir

class ContentResolver( object ):

    interface.implements( iindex.IResolver )
    scheme = '' # u'bungeni'
    
    def id( self, object ): 
        return "%s.%s-%s"%( object.__class__.__module__,
                            object.__class__.__name__,
                            container.stringKey( object ) )
        
    def resolve( self, id ): 
        class_path, oid = id.split('-', 1)
        domain_class = resolve.resolve( class_path )
        session = Session()
        value_key = container.valueKey( oid )
        return session.query( domain_class ).get( value_key )
        
# content indexer
class ContentIndexer( object ):
    
    interface.implements( iindex.IIndexer )
    
    def __init__( self, context ):
        self.context = context

    def document( self, connection ):
        """
        return a xapian index document from the context.

        we can introspect the connection to discover relevant fields available.
        """
        doc = xappy.UnprocessedDocument()        
        
        # object type
        doc.fields.append( 
             xappy.Field( "object_type", self.context.__class__.__name__ )
             )

        if interfaces.ENABLE_LOGGING:
            log.warning("Indexing Document %r"%self.context )
            
        # object kind
        doc.fields.append( 
             xappy.Field( "object_kind", domain.object_hierarchy_type( self.context ) )
             )        

        # schema fields one by one
        for iface in interface.providedBy( self.context ):
            for field in schema.getFields( iface ).values():
                #log.warning("  processing %s %r"%( field.__name__, field) )
                if not isinstance( field, ( schema.Text, schema.ASCII ) ):
                    continue
                value = field.query( self.context, '' )
                if value is None:
                    value = u''
                #if interfaces.ENABLE_LOGGING:
                #    log.warning("  field %s %r %r"%( field.__name__, field, value ) )
                    
                if not isinstance( value, (str, unicode)):
                    value = unicode( value )
                doc.fields.append(  xappy.Field(field.__name__, value ) )

        return doc

    def fields( self, indexer ):
        self.specified_fields( indexer )
        action_fields = ('resolver', 'object_type', 'object_kind', 'status', 'path', 'title')
        
        for iface in interface.providedBy( self.context ):
            for field in schema.getFields( iface ).values():
                if field.__name__ in action_fields:
                    continue
                if not isinstance( field, ( schema.Text, schema.ASCII ) ):
                    continue
                indexer.add_field_action( field.__name__, xappy.FieldActions.INDEX_FREETEXT, language='en' )


    def specified_fields( self, indexer ):
        pass
        
        
####################
## Field Definitions
#

def setupFieldDefinitions(indexer):
    # resolution utility type
    indexer.add_field_action('resolver', xappy.FieldActions.INDEX_EXACT )
    indexer.add_field_action('resolver', xappy.FieldActions.STORE_CONTENT )

    # content type / object class
    indexer.add_field_action('object_type', xappy.FieldActions.INDEX_EXACT )
    indexer.add_field_action('object_type', xappy.FieldActions.STORE_CONTENT )
    indexer.add_field_action('object_type', xappy.FieldActions.FACET, type='string')

    # object class hierarchy (user, group, etc)
    indexer.add_field_action('object_kind', xappy.FieldActions.INDEX_EXACT )
    indexer.add_field_action('object_kind', xappy.FieldActions.STORE_CONTENT )
    
    # workflow status
    indexer.add_field_action('status', xappy.FieldActions.INDEX_EXACT )
    indexer.add_field_action('status', xappy.FieldActions.STORE_CONTENT )
    indexer.add_field_action('status', xappy.FieldActions.FACET, type='string')

    # site relative path
    indexer.add_field_action('path', xappy.FieldActions.STORE_CONTENT )

    # fields for parliamentary items
    # XXX xapian stores language codes at the field level, need to
    # find a solution for this
    indexer.add_field_action('title', xappy.FieldActions.INDEX_FREETEXT, weight=5, language='en', spell=True )
    indexer.add_field_action('title', xappy.FieldActions.STORE_CONTENT )

    ContentIndexer( domain.Bill()  ).fields( indexer )
    ContentIndexer( domain.Motion()  ).fields( indexer )
    ContentIndexer( domain.Question()  ).fields( indexer )        
    ContentIndexer( domain.User()  ).fields( indexer )
    ContentIndexer( domain.Group()  ).fields( indexer )
    ContentIndexer( domain.Committee()  ).fields( indexer )            
    ContentIndexer( domain.Parliament()  ).fields( indexer )        
    ContentIndexer( domain.ParliamentMember()  ).fields( indexer )
    ContentIndexer( domain.HansardReporter()  ).fields( indexer )            
    

# storage directory
store_dir = setupStorageDirectory() 

# search connection hub
searcher = search.IndexSearch( store_dir )

# async indexer 
indexer = xappy.IndexerConnection( store_dir )

# field definitions
setupFieldDefinitions(indexer)
