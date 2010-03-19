#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bungeni - http://www.bungeni.org/
# Parliamentary and Legislative Information System
# Copyright (C) 2010 UN/DESA - http://www.un.org/esa/desa/
# Licensed under GNU GPL v2 - http://www.gnu.org/licenses/gpl-2.0.txt

'''Utilities to help with queries on the domain model

$Id$
'''

from ore.alchemist import Session
from bungeni.models import domain
from bungeni.models import schema
from sqlalchemy import desc
from sqlalchemy import sql

def container_getter(getter, name, query_modifier=None):
    def func(context):
        obj = getter(context)
        try: 
            c = getattr(obj, name)
        except AttributeError:
            # the container we need is not there, data may be missing in the db
            from zope.publisher.interfaces import NotFound
            raise NotFound(context, name)
        c.setQueryModifier(sql.and_(c.getQueryModifier(), query_modifier))
        return c
    func.__name__ = "get_%s_container" % name
    return func

def get_current_parliament(context):
    session = Session()
    parliament = session.query(domain.Parliament).order_by(
        desc(domain.Parliament.election_date)).first()
    #session.close()
    return parliament


def get_parliament_by_date_range(context, start_date, end_date):
    session = Session()
    parliament = session.query(domain.Parliament).filter(
        (domain.Parliament.start_date < start_date) & \
        ((domain.Parliament.end_date == None) | \
         (domain.Parliament.end_date > end_date))).\
        order_by(desc(domain.Parliament.election_date)).first()
    #session.close()            
    return parliament         

def get_session_by_date_range(context, start_date, end_date):
    session = Session()
    ps = session.query(domain.ParliamentSession).filter(
        (domain.ParliamentSession.start_date < start_date) & \
        ((domain.ParliamentSession.end_date == None) | \
         (domain.ParliamentSession.end_date > end_date))).first()
    #session.close()            
    return ps 


def get_sittings_between(sittings, start, end):
    modifier = sittings.getQueryModifier()
    sittings.setQueryModifier(
        sql.and_(
            modifier,
            sql.or_( 
                sql.between(schema.sittings.c.start_date, start, end), 
                sql.between(schema.sittings.c.end_date, start, end),
                sql.between(start, schema.sittings.c.start_date, 
                            schema.sittings.c.end_date),
                sql.between(end, schema.sittings.c.start_date, 
                            schema.sittings.c.end_date)
                ),
            ))

    query = sittings._query
    sittings.setQueryModifier(modifier)
    return query

