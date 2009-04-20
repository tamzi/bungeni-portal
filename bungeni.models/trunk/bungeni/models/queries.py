from ore.alchemist import Session
from bungeni.models import domain
from sqlalchemy import desc

def get_current_parliament(context):
    session = Session()
    return session.query(domain.Parliament).order_by(
        desc(domain.Parliament.election_date)).first()
