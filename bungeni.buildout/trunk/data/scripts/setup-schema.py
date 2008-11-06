"""
some database value population scripts
"""

import transaction

from bungeni import core
from bungeni.core import schema
from ore.alchemist import Session
from alchemist import security
from marginalia import schema as marginalia_schema
from sqlalchemy import create_engine

core.metadata.bind = db = create_engine('postgres://localhost/bungeni')
core.metadata.drop_all()
core.metadata.create_all()
# the unbound sequences wont get created so we have to
# create them maunually
schema.QuestionSequence.create(db)
schema.MotionSequence.create(db)

security.metadata.bind = db
security.metadata.drop_all() 
security.metadata.create_all() 

marginalia_schema.metadata.bind = db
marginalia_schema.metadata.drop_all()
marginalia_schema.metadata.create_all() 

db.dispose()

