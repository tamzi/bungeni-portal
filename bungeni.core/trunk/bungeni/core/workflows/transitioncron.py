# encoding: utf-8
#Automatically transition Questions 
#The system needs to provide a settable time-frame beyond which “Admissible” 
#questions which are available for scheduling - change status to “Deferred”

import datetime
import sqlalchemy.sql.expression as sql

from ore.alchemist import Session

import bungeni.core.domain as domain
import bungeni.core.schema as schema

import bungeni.core.workflows.question as question_workflow
import bungeni.core.globalsettings as prefs

from ore.workflow.interfaces import IWorkflowInfo



def _getQuestionsBefore(date, status):
    """
    get all questions with the workflow status before date
    """
    session = Session()
    qfilter=sql.and_(
                (domain.Question.c.approval_date < date ),
                (domain.Question.c.status == status)
                )
    query = session.query(domain.Question).filter(qfilter)   
    return query.all()
    
    
def _deferAdmissibleQuestionsBefore(date):
    """
    set all admissible Questions before this
    date to defered
    """    
    status = question_workflow.states.admissible
    admissableQuestions = _getQuestionsBefore(date, status)
    for question in admissableQuestions:
        IWorkflowInfo(question).fireTransition('defer')        


def deferAdmissibleQuestions():
    """
    get the timeframe and defer all questions 
    before the current date - timeframe
    """
    timedelta = prefs.getDaysToDeferAdmissibleQuestions()
    deferDate = datetime.date.today() - timedelta
    _deferAdmissibleQuestionsBefore(deferDate)
    


