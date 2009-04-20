from ore.alchemist import Session
from bungeni.models import domain
from sqlalchemy import desc

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
