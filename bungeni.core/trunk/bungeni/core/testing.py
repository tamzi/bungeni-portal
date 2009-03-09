import index
import zope.interface
import zope.publisher.interfaces
import zope.security.testing
from alchemist.security.schema import metadata  
from ore.alchemist.interfaces import IDatabaseEngine
from sqlalchemy import create_engine
from zope import component
from bungeni import models as model

def setup_indexer():
    store_dir = index.setupStorageDirectory() + '-test'

    # search connection hub
    searcher = index.search.IndexSearch(store_dir)

    # async indexer 
    indexer = index.xappy.IndexerConnection(store_dir)

    # field definitions
    index.setupFieldDefinitions(indexer)

def create_principal(id='manager', title="Manager", groups=()):
    return zope.security.testing.Principal(id, title, groups)

def create_participation(principal=None):
    if principal is None:
        principal = create_principal()
    participation = zope.security.testing.Participation(principal)
    
    zope.interface.alsoProvides(
        participation, zope.publisher.interfaces.IRequest)

    return participation
    
def setup_db():
    db = create_engine('postgres://localhost/bungeni-test', echo=False)
    component.provideUtility( db, IDatabaseEngine, 'bungeni-db' )
    model.metadata.bind = db 
    model.metadata.drop_all()     
    model.metadata.create_all()
    model.schema.QuestionSequence.create(db) 
    model.schema.MotionSequence.create(db)     
    metadata.bind = db
    metadata.drop_all()     
    metadata.create_all()  

        
    
