from ore.alchemist import Session
from bungeni.models import domain
from bungeni.models import schema
from sqlalchemy import desc
from sqlalchemy import sql

def container_getter(getter, name):
    def func(context):
        obj = getter(context)
        return getattr(obj, name)
    func.__name__ = "get_%s_container" % name
    return func

def get_current_parliament(context):
    session = Session()
    return session.query(domain.Parliament).order_by(
        desc(domain.Parliament.election_date)).first()

def get_parliament_by_date_range(context, start_date, end_date):
    session = Session()
    return session.query(domain.Parliament).filter(
        (domain.Parliament.start_date < start_date) & \
        ((domain.Parliament.end_date == None) | \
         (domain.Parliament.end_date > end_date))).\
        order_by(desc(domain.Parliament.election_date)).first()

def get_session_by_date_range(context, start_date, end_date):
    session = Session()
    return session.query(domain.ParliamentSession).filter(
        (domain.ParliamentSession.start_date < start_date) & \
        ((domain.ParliamentSession.end_date == None) | \
         (domain.ParliamentSession.end_date > end_date))).first()

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

