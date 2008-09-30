#enconding utf-8

# db specific utilities to retrive values, restriction etc
# from the db implementation

from ore.alchemist import Session
import bungeni.core.domain as domain
import bungeni.core.schema as schema
import bungeni.core.globalsettings as prefs


def setQuestionParliamentId(question):
    if not question.parliament_id:
        question.parliament_id = prefs.getCurrentParliamentId()
        
        
def getQuestion(question_id):
    """
    gets the question with id 
    """
    session = Session()
    query = session.query(domain.Question).filter(schema.questions.c.question_id == question_id)
    return query.one()
    
def insertQuestionScheduleHistory(question_id, sitting_id):
    """
    inserts question and sitting when a question was postponed
    """
    session = Session() 
    question_schedule = domain.QuestionSchedule()
    question_schedule.question_id = question_id
    question_schedule.sitting_id = sitting_id
    session.save(question_schedule)
    session.flush()
         
    
    
