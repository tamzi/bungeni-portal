#enconding utf-8

# db specific utilities to retrive values, restriction etc
# from the db implementation
import sqlalchemy.sql.expression as sql
from ore.alchemist import Session

import bungeni.core.domain as domain
import bungeni.core.schema as schema
from bungeni.core.i18n import _

import datetime

def getCurrentParliamentId(date = None):
    """
    returns the current parliament_id for a given date
    or for the current if the date is not given
    """
    def getFilter(date):
        return sql.or_(
            sql.between(date, schema.groups.c.start_date, schema.groups.c.end_date),
            sql.and_( schema.groups.c.start_date <= date, schema.groups.c.end_date == None)
            )
    
    if not date:
        date = datetime.date.today()
    session = Session() 
    query = session.query(domain.Parliament).filter(getFilter(date))   
    result = None
    try:
        result = query.one()
    except:
        pass #XXX raise( _(u"inconsistent data: none or more than one parliament found for this date"))       
    if result:        
        return result.parliament_id
        
def setQuestionParliamentId(question):
    """
    Set the parliament id for a question
    """        
    session = Session()
    question.parliament_id = getCurrentParliamentId()
    session.flush()

def getQuestion(question_id):
    """
    gets the question with id 
    """
    session = Session()
    query = session.query(domain.Question).filter(schema.questions.c.question_id == question_id)
    return query.one()
    
    
    
    
