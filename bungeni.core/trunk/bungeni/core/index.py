"""
xapian indexing adapters
"""
from zope import interface
from zope.dottedname import resolve
import xappy, os, os.path as path

from ore.alchemist import container, Session
from ore.alchemist.interfaces import IModelDescriptor
from ore.xapian import queue, search, interfaces as iindex

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
    scheme = u'bungeni'
    
    def id( self, object ): 
        return "%s.%s-%s"%( object.__class__.__module,
                            object.__class__.__name__,
                            container.stringKey( object ) )
        
    def resolve( self, id ): 
        class_path, oid = id.split('-')
        domain_class = resolve.resolve( class_path )
        session = Session()
        return session.query( domain_class ).get( oid )


store_dir = setupStorageDirectory() 

# search connection hub
searcher = search.IndexSearch( store_dir )

# async indexer
indexer = xappy.IndexerConnection( store_dir )
indexer.add_field_action('resolver', xappy.FieldActions.INDEX_EXACT )
indexer.add_field_action('resolver', xappy.FieldActions.STORE_CONTENT )

# fields for parliamentary items
indexer.add_field_action('title', xappy.FieldActions.INDEX_FREETEXT )
indexer.add_field_action('title', xappy.FieldActions.STORE_CONTENT )
indexer.add_field_action('description', xappy.FieldActions.INDEX_FREETEXT )

# start the processing thread
queue.QueueProcessor.start( indexer )



