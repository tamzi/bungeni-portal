"""
some database value population scripts
"""

import transaction

from bungeni import core
from ore.alchemist import Session
from sqlalchemy import create_engine

core.metadata.bind = db = create_engine('postgres://localhost/bungeni')
core.metadata.drop_all()
core.metadata.create_all()
db.dispose()

