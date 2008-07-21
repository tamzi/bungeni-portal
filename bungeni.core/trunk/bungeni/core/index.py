"""
xapian indexing adapters
"""
from zope import interface, schema
from zope.dottedname import resolve
import xappy, os, os.path as path

from ore.alchemist import container
from sqlalchemy.orm.session import Session
from ore.xapian import queue, search, interfaces as iindex

import domain

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

        # object kind
        doc.fields.append( 
             xappy.Field( "object_kind", domain.object_hierarchy_type( self.context ) )
             )        

        # schema fields one by one
        for iface in interface.providedBy( self.context ):
            for field in schema.getFields( iface ).values():
                if not isinstance( field, ( schema.Text, schema.ASCII ) ):
                    continue
                value = field.query( self.context, '' )
                if value is None:
                    value = u''
                if not isinstance( value, (str, unicode)):
                    value = unicode( value )
                doc.fields.append(  xappy.Field(field.__name__, value ) )

        return doc


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

# storage directory
store_dir = setupStorageDirectory() 

# search connection hub
searcher = search.IndexSearch( store_dir )

# async indexer 
indexer = xappy.IndexerConnection( store_dir )

# field definitions
setupFieldDefinitions(indexer)
