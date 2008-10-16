#enconding utf-8

# db specific utilities to retrive values, restriction etc
# from the db implementation
import sqlalchemy as rdb
from sqlalchemy.orm import mapper
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
    return session.query(domain.Question).get(question_id)

    
def setQuestionMinistryId(question):
    if question.supplement_parent_id:
        sq = getQuestion(question.supplement_parent_id)
        question.ministry_id = sq.ministry_id
        
            
    
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

class _Minister(object):
    pass         
def getMinsiteryEmails(ministry):
    """
    returns the emails of all persons who are members of that ministry
    """    
    session = Session()
    ministers = rdb.join(schema.groups,schema.user_group_memberships, 
                         schema.groups.c.group_id == schema.user_group_memberships.c.group_id
                        ).join(
                          schema.users,
                          schema.user_group_memberships.c.user_id == schema.users.c.user_id)
    mapper(_Minister, ministers)                       
    query = session.query(_Minister).filter(_Minister.group_id == ministry.group_id)
    results = query.all()
    addresses = []
    for result in results:
        address = '"%s %s" <%s>' % (result.first_name, result.last_name, result.email)
        addresses.append(address)
    return ' ,'.join(addresses)
        
    
