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
        

def removeQuestionFromItemSchedule(question_id):
    """
    when a question gets postponed the previous schedules of that
    question are invalidated so the do not show up in the schedule 
    calendar any more
    """            
    session = Session()
    active_question_filter = rdb.and_( schema.items_schedule.c.item_id == question_id,
                                       schema.items_schedule.c.active == True)
    item_schedule = session.query(domain.ItemSchedule).filter(active_question_filter)
    results = item_schedule.all()
    assert (len(results) == 1)
    results[0].active = False
    
    
def removeMotionFromItemSchedule(motion_id):
    """
    when a motion gets postponed the previous schedules of that
    motion are invalidated so the do not show up in the schedule 
    calendar any more
    """            
    session = Session()
    active_motion_filter = rdb.and_( schema.items_schedule.c.item_id == motion_id,
                                       schema.items_schedule.c.active == True)
    item_schedule = session.query(domain.ItemSchedule).filter(active_motion_filter)
    results = item_schedule.all()
    assert (len(results) == 1)
    results[0].active = False    
    
def setQuestionSerialNumber(question):
    """
     Approved questions are given a serial number enabling the clerks office
     to record the order in which questions are recieved and hence enforce 
     a first come first served policy in placing the questions on the order
     paper. The serial number is re-initialized at the start of each session
    """    
    session = Session()
    connection = session.connection(domain.Question)
    sequence = rdb.Sequence('question_number_sequence')
    question.question_number = connection.execute(sequence)

def isQuestionScheduled(question_id):
    session = Session()
    active_question_filter = rdb.and_( schema.items_schedule.c.item_id == question_id,
                                       schema.items_schedule.c.active == True)
    item_schedule = session.query(domain.ItemSchedule).filter(active_question_filter)
    results = item_schedule.all()
    return (len(results) == 1)
    
def setMotionSerialNumber(motion):    
    """
     Number that indicate the order in which motions have been approved 
     by the Speaker. The Number is reset at the start of each new session
     with the first motion assigned the number 1    
    """
    session = Session()
    connection = session.connection(domain.Motion)
    sequence = rdb.Sequence('motion_number_sequence')
    motion.motion_number = connection.execute(sequence)    


    
#def insertQuestionScheduleHistory(question_id, sitting_id):
#    """
#    inserts question and sitting when a question was postponed
#    """
#    session = Session() 
#    question_schedule = domain.QuestionSchedule()
#    question_schedule.question_id = question_id
#    question_schedule.sitting_id = sitting_id
#    session.save(question_schedule)
#    session.flush()

class _Minister(object):
    pass     

ministers = rdb.join(schema.groups,schema.user_group_memberships, 
                         schema.groups.c.group_id == schema.user_group_memberships.c.group_id
                        ).join(
                          schema.users,
                          schema.user_group_memberships.c.user_id == schema.users.c.user_id)

mapper(_Minister, ministers)     
        
def getMinsiteryEmails(ministry):
    """
    returns the emails of all persons who are members of that ministry
    """    
    session = Session()                      
    query = session.query(_Minister).filter(_Minister.group_id == ministry.group_id)
    results = query.all()
    addresses = []
    for result in results:
        address = '"%s %s" <%s>' % (result.first_name, result.last_name, result.email)
        addresses.append(address)
    return ' ,'.join(addresses)
        
    
