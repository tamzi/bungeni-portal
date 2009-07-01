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

bill_filter = sql.or_(
    between(domain.Bill.submission_date),
    between(domain.Bill.publication_date)
    )

motion_filter = sql.or_(
    between(domain.Motion.submission_date),
    between(domain.Motion.notice_date),
    between(domain.Motion.approval_date),
    )

question_filter = sql.or_(
    between(domain.Question.submission_date),
    between(domain.Question.ministry_submit_date),
    between(domain.Question.approval_date),
    )

group_filter = sql.or_(
    domain.Group.start_date.between(sql.bindparam("start_date"), sql.bindparam("end_date")),
    domain.Group.end_date.between(sql.bindparam("start_date"), sql.bindparam("end_date")),
    sql.and_(
        domain.Group.start_date <= sql.bindparam("end_date"),
        domain.Group.start_date >= sql.bindparam("start_date"),
        domain.Group.end_date == None),
    )    
