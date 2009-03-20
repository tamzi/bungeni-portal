#
import datetime
from zope import component

from alchemist.security import schema as security
from ore.alchemist.interfaces import IDatabaseEngine
from sqlalchemy import create_engine
from bungeni import models as model

# common date expressions
today = datetime.date.today()
yesterday = today - datetime.timedelta(1)
tomorrow = today + datetime.timedelta(1)
dayat = today + datetime.timedelta(2)

def setup_db():
    db = create_engine('postgres://localhost/bungeni-test', echo=False)
    component.provideUtility( db, IDatabaseEngine, 'bungeni-db' )
    model.metadata.bind = db 
    model.metadata.drop_all()     
    model.metadata.create_all()
    model.schema.QuestionSequence.create(db) 
    model.schema.MotionSequence.create(db)     
    security.metadata.bind = db
    security.metadata.drop_all()     
    security.metadata.create_all()  
    return db






