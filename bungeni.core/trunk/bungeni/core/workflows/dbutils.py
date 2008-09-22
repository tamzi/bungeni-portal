#enconding utf-8

# db specific utilities to retrive values, restriction etc
# from the db implementation

from ore.alchemist import Session
import bungeni.core.domain as domain
import bungeni.core.schema as schema

        
def getQuestion(question_id):
    """
    gets the question with id 
    """
    session = Session()
    query = session.query(domain.Question).filter(schema.questions.c.question_id == question_id)
    return query.one()
    
    
    
    
