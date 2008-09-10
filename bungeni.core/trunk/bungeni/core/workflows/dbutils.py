#enconding utf-8

# db specific utilities to retrive values, restriction etc
# from the db implementation
import sqlalchemy.sql.expression as sql
from ore.alchemist import Session

from bungeni.core.domain import Parliament
from bungeni.core.schema import groups
from bungeni.core.i18n import _

import datetime

def getCurrentParliamentId(date = None):
    """
    returns the current parliament_id for a given date
    """
    def getFilter(date):
        return sql.or_(
            sql.between(date, groups.c.start_date, groups.c.end_date),
            sql.and_( groups.c.start_date <= date, groups.c.end_date == None)
            )
    
    if not date:
        date = datetime.date.today()
    session = Session() 
    query = session.query(Parliament).filter(getFilter(date))   
    result = None
    try:
        result = query.one()
    except:
        pass #raise( _(u"inconsistent data: none or more than one parliament found for this date"))       
    if result:        
        return result.parliament_id
        
def setQuestionParliamentId(question):
    """
    Set the parliament id for a question
    """        
    session = Session()
    question.parliament_id = getCurrentParliamentId()
    session.flush()
    
