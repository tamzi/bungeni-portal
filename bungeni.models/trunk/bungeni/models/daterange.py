from sqlalchemy import sql
import domain

def between(column):
    return sql.and_(
        sql.or_(
            column >= sql.bindparam("start_date"),
            sql.bindparam("start_date") == None),
        sql.or_(
            column <= sql.bindparam("end_date"),
            sql.bindparam("end_date") == None),
        )

def bill_filter(): 
    return sql.or_(
    between(domain.Bill.submission_date),
    between(domain.Bill.publication_date)
    )

def motion_filter():
    return sql.or_(
    between(domain.Motion.submission_date),
    between(domain.Motion.notice_date),
    between(domain.Motion.approval_date),
    )

def question_filter():
    return sql.or_(
    between(domain.Question.submission_date),
    between(domain.Question.ministry_submit_date),
    between(domain.Question.approval_date),
    )

def group_filter():
    return sql.or_(
    domain.Group.start_date.between(
                sql.bindparam("start_date"), sql.bindparam("end_date")),
    domain.Group.end_date.between(
                sql.bindparam("start_date"), sql.bindparam("end_date")),
    sql.between(sql.bindparam("start_date"), 
                domain.Group.start_date, domain.Group.end_date),
    sql.between(sql.bindparam("end_date"),
                domain.Group.start_date, domain.Group.end_date),                
    sql.and_(
        domain.Group.start_date <= sql.bindparam("end_date"),
        domain.Group.end_date == None),
    )    
            
    
def group_membership_filter():
    return sql.or_(
    domain.GroupMembership.start_date.between(
            sql.bindparam("start_date"), sql.bindparam("end_date")),
    domain.GroupMembership.end_date.between(
            sql.bindparam("start_date"), sql.bindparam("end_date")),
    sql.between(sql.bindparam("start_date"), 
                domain.GroupMembership.start_date, 
                domain.GroupMembership.end_date),
    sql.between(sql.bindparam("end_date"),
                domain.GroupMembership.start_date, 
                domain.GroupMembership.end_date),            
    sql.and_(
        domain.GroupMembership.start_date <= sql.bindparam("end_date"),
        domain.GroupMembership.end_date == None),
    )     
    
    
def session_filter():
    return sql.or_(
    domain.ParliamentSession.start_date.between(
                sql.bindparam("start_date"), sql.bindparam("end_date")),
    domain.ParliamentSession.end_date.between(
                sql.bindparam("start_date"), sql.bindparam("end_date")),
    sql.between(sql.bindparam("start_date"), 
                domain.ParliamentSession.start_date, domain.ParliamentSession.end_date),
    sql.between(sql.bindparam("end_date"),
                domain.ParliamentSession.start_date, domain.ParliamentSession.end_date),                
    sql.and_(
        domain.ParliamentSession.start_date <= sql.bindparam("end_date"),
        domain.ParliamentSession.end_date == None),
    )       
    
    
def sitting_filter():
    return sql.or_(
    domain.GroupSitting.start_date.between(
                sql.bindparam("start_date"), sql.bindparam("end_date")),
    domain.GroupSitting.end_date.between(
                sql.bindparam("start_date"), sql.bindparam("end_date")),
    sql.between(sql.bindparam("start_date"), 
                domain.GroupSitting.start_date, domain.GroupSitting.end_date),
    sql.between(sql.bindparam("end_date"),
                domain.GroupSitting.start_date, domain.GroupSitting.end_date),                
    sql.and_(
        domain.GroupSitting.start_date <= sql.bindparam("end_date"),
        domain.GroupSitting.end_date == None),
    )           
    
    
    
