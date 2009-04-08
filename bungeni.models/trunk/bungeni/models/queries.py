from ore.alchemist import Session
from bungeni.models import domain

def get_current_parliament(context):
    session = Session()
    return session.query(domain.Parliament).order_by(
        'election_date').first()
