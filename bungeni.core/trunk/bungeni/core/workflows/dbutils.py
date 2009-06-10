#enconding utf-8

# db specific utilities to retrive values, restriction etc
# from the db implementation
import sqlalchemy as rdb
from sqlalchemy.orm import mapper
from ore.alchemist import Session
import bungeni.models.domain as domain
import bungeni.models.schema as schema
import bungeni.models.interfaces as interfaces
import bungeni.core.globalsettings as prefs

def get_user_login(user_id):
    if user_id:
        session=Session()
        user = session.query(domain.User).get(user_id)
        return user.login


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
    if (len(results) == 1):
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

def isItemScheduled(item_id):
    session = Session()
    active_question_filter = rdb.and_( schema.items_schedule.c.item_id == item_id,
                                       schema.items_schedule.c.active == True)
    item_schedule = session.query(domain.ItemSchedule).filter(active_question_filter)
    results = item_schedule.all()
    return (len(results) >= 1)
    
    
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
        
def deactivateGroupMembers(group):
    """ upon dissolution of a group all group members
    are deactivated and get the end date of the group"""
    session = Session()
    group_id = group.group_id
    end_date = group.end_date
    assert(end_date != None)    
    connection = session.connection(domain.Group)
    connection.execute(schema.user_group_memberships.update().where(
        rdb.and_(
            schema.user_group_memberships.c.group_id == group_id,
            schema.user_group_memberships.c.active_p == True)
            ).values(active_p = False)
        )
    connection.execute(schema.user_group_memberships.update().where(
        rdb.and_(
            schema.user_group_memberships.c.group_id == group_id,
            schema.user_group_memberships.c.end_date == None)
            ).values(end_date = end_date)
        )

def endChildGroups(group):
    """ upon dissolution of a parliament for all committees,
    offices and political groups of this parliament the end date is 
    set 
    or upon dissolution of a government for all ministries 
    of this government the end date is set
    (in order to be able to dissolve those groups)"""
    def _end_parliament_group(group_class, parent_id, end_date):
        groups = session.query(group_class).filter(
            rdb.and_(group_class.status == 'active',
                group_class.parliament_id == parliament_id)).all()          
        for group in groups:
            if group.end_date == None:
                group.end_date = end_date   
        return groups                              
    
    session = Session()
    end_date = group.end_date   
    assert(end_date != None)
    if interfaces.IParliament.providedBy(group):
        parliament_id = group.parliament_id
        committees = _end_parliament_group(domain.Committees, 
                    parliament_id,
                    end_date)
        yield committees
        offices = _end_parliament_group(domain.Office,  
                    parliament_id,
                    end_date)                         
        yield offices
        political_groups =  _end_parliament_group(domain.PoliticalParty,
                    parliament_id,
                    end_date)          
        yield political_groups                                     
    elif interfaces.IGovernment.providedBy(group):
        government_id = group.government_id
        ministries = session.query(domain.Ministry).filter(
            rdb.and_(domain.Ministry.status == 'active',
                domain.Ministry.government_id == government_id)
                ).all()
        for ministry in ministries:
            if ministry.end_date == None:
                ministry.end_date = end_date
            yield ministry
            
         

    
