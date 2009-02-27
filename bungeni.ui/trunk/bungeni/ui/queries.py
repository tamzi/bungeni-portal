from ore.alchemist import Session

import bungeni.models.domain as domain
import bungeni.models.schema as db_schema

def get_user_id( name ):
    session = Session()
    userq = session.query(domain.User).filter(db_schema.users.c.login == name )
    results = userq.all()
    if results:
        user_id = results[0].user_id
    else:
        user_id = None
    return user_id                
