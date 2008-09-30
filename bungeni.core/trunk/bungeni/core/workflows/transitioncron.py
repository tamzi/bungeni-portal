# encoding: utf-8
#Automatically transition Questions 
#The system needs to provide a settable time-frame beyond which “Admissible” 
#questions which are available for scheduling - change status to “Deferred”
import sys
import datetime
import sqlalchemy.sql.expression as sql

from ore.alchemist import Session

import bungeni.core.domain as domain
import bungeni.core.schema as schema

import bungeni.core.workflows.question as question_workflow
import bungeni.core.globalsettings as prefs

from ore.workflow.interfaces import IWorkflowInfo

##############################
# imports for main
from zope import component
from sqlalchemy import create_engine
from ore.alchemist.interfaces import IDatabaseEngine
import ore.workflow.workflow
import bungeni.core.interfaces
import bungeni.core.workflows.question
from bungeni import core as model

#import pdb

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
    admissibleQuestions = _getQuestionsBefore(date, status)
    #session = Session()
    for question in admissibleQuestions:
        IWorkflowInfo(question).fireTransition('defer')   
    #pdb.set_trace()             
    #session.flush()

def deferAdmissibleQuestions():
    """
    get the timeframe and defer all questions 
    before the current date - timeframe
    """
    timedelta = prefs.getDaysToDeferAdmissibleQuestions()
    deferDate = datetime.date.today() - timedelta
    _deferAdmissibleQuestionsBefore(deferDate)
    
def main(argv=None):
    """
    run this as a cron job and execute all
    time based transitions
    """
    db = create_engine('postgres://localhost/bungeni', echo=False)
    component.provideUtility( db, IDatabaseEngine, 'bungeni-db' )
    model.metadata.bind = db
    session = Session()    
    component.provideAdapter(
      bungeni.core.workflows.WorkflowState,
      (bungeni.core.interfaces.IBungeniContent,))

    component.provideAdapter(
      bungeni.core.workflows.question.QuestionWorkflowAdapter,
      (domain.Question,))

    component.provideAdapter(
      ore.workflow.workflow.WorkflowInfo,
      (domain.Question,))

    component.provideHandler(
      bungeni.core.workflows.question.workflowTransitionEventDispatcher)  
# add autitor for time based transitions     
#    component.provideAdapter(
#        bungeni.core.interfaces.IAuditable,
#        (domain.Question))        
    
    deferAdmissibleQuestions() 
    session.flush()
    session.commit()
    
if __name__ == "__main__":
    sys.exit(main())


