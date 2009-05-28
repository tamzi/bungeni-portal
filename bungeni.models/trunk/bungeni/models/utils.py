#!/usr/bin/env python
# encoding: utf-8

from zope.security.management import getInteraction
from zope.publisher.interfaces import IRequest
from ore.alchemist import Session

import domain

def getUserId( ):
    interaction = getInteraction()
    for participation in interaction.participations:
        if IRequest.providedBy(participation):
            return participation.principal.id

def get_db_user_id():
    userId = getUserId()
    session = Session()
    query = session.query(domain.User).filter(
                    domain.User.login == userId)
    results = query.all()
    if len(results) == 1:
        return results[0].user_id                    


                    
