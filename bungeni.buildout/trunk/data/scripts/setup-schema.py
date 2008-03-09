"""
some database value population scripts
"""

import transaction

from bungeni import core
from ore.alchemist import Session
from alchemist import security
from sqlalchemy import create_engine

core.metadata.bind = db = create_engine('postgres://localhost/bungeni')
core.metadata.drop_all()
core.metadata.create_all()

security.metadata.bind = db
security.metadata.drop_all() 
security.metadata.create_all() 

db.dispose()

