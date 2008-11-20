"""
need workflow viewlet for current transition, and current state?
"""
from ore.workflow import workflow
from ore.workflow import interfaces as iworkflow
from bungeni.core.i18n import _
import bungeni.core.workflows.utils as utils

class states:

    draft = "draft_bill"
    #member_draft = "member_draft"
    
    submitted = "bill_published_in_gazette"
    first_reading = "first_reading"
    first_reading_postponed = "first_reading_postponed"
    first_committee = "first_committee"

    # after a committee, there is an option to
    # present the finding directly to the house.
    # report_reading_1 = "report_reading_1"
    
    # to be scheduled for 2nd reading
    second_pending = "second_pending"
    second_reading = "second_reading"
    second_reading_postponed = "second_reading_postponed"

    # to be scheduled for whole house
    house_pending = "house_pending"
    whole_house ="whole_house"
    whole_house_postponed ="whole_house_postponed"

    second_committee = "second_committee"

    # to be scheduled for report reading
    report_reading_pending = "report_reading_pending"
    report_reading = "report_reading"
    report_reading_postponed = "report_reading_postponed"


    # is there a third pending state for a bill
    third_pending = "third_pending"
    third_reading = "third_reading"
    third_reading_postponed = "third_reading_postponed"

    withdrawn ="bill_withdrawn"

    approved = "approved"
    rejected = "rejected"
    
def create(info,context):
    utils.setBillSubmissionDate( info, context )

def submit( info,context ):
    utils.setBillPublicationDate( info, context )
    
def withdraw(info,context):
    pass
    
def schedule_first( info,context ):    
    pass
    
def postpone_first( info,context ):
    pass
        

def create_bill_workflow( ):

    transitions = []

    add = transitions.append

    add( workflow.Transition(
        transition_id = 'create-bill',
        title=_('Create'),
        trigger = iworkflow.AUTOMATIC,
        source = None,        
        action = create,       
        destination = states.draft,
        #permission = "bungeni.question.Create",
        ) )
        


    add( workflow.Transition(
        transition_id = 'submit-bill',
        title=_(u"Submit"),
        source = states.draft,
        action = submit,
        destination = states.submitted,
        permission = "bungeni.bill.Submit"
        ) )


    add( workflow.Transition(
        transition_id = 'schedule-first',
        title=_(u"Schedule First Reading"),
        trigger = iworkflow.MANUAL,
        source = states.submitted,
        action = schedule_first,
        destination = states.first_reading,
        permission = "bungeni.bill.Schedule",
        ) )

    add( workflow.Transition(
        transition_id = 'postpone-first',
        title=_(u"Postpone First Reading"),
        trigger = iworkflow.MANUAL,
        source = states.first_reading,
        action = postpone_first,
        destination = states.first_reading_postponed,
        permission = "bungeni.bill.Schedule",
        ) )

    add( workflow.Transition(
        transition_id = 'reschedule-first',
        title=_(u"Reschedule First Reading"),
        trigger = iworkflow.MANUAL,
        source = states.first_reading_postponed,
        action = schedule_first,
        destination = states.first_reading,
        permission = "bungeni.bill.Schedule",
        ) )




    add( workflow.Transition(
        transition_id = 'select-first-committee',
        title=_(u"Send to Committee"),
        trigger = iworkflow.MANUAL,
        source = states.first_reading,
        destination = states.first_committee,
        permission = "bungeni.bill.SelectCommittee",
        ) )

          
    add( workflow.Transition(
        transition_id = 'schedule-second-from-first-committee',
        title = _(u"Second Reading schedule"),
        trigger = iworkflow.MANUAL,
        source = states.first_committee,
        destination = states.second_pending,
        permission = "bungeni.bill.Schedule"
        ))    
        
    add( workflow.Transition(
        transition_id = 'schedule-second',
        title = _(u"Schedule Second Reading"),
        trigger = iworkflow.MANUAL,
        source = states.second_pending,
        destination = states.second_reading,
        permission = "bungeni.bill.Schedule"
        ))            

    add( workflow.Transition(
        transition_id = 'ma-schedule-second',
        title=_(u"Schedule Second Reading"),
        trigger = iworkflow.MANUAL,
        source = states.first_reading,
        destination = states.second_pending,
        permission = "bungeni.bill.Schedule",
        ) )
        

    add( workflow.Transition(
        transition_id = 'postpone-second',
        title=_(u"Postpone Second Reading"),
        trigger = iworkflow.MANUAL,
        source = states.second_reading,
        destination = states.second_reading_postponed,
        permission = "bungeni.bill.Schedule",
        ) )


    add( workflow.Transition(
        transition_id = 'reschedule-second',
        title=_(u"Reschedule Second Reading"),
        trigger = iworkflow.MANUAL,
        source = states.second_reading_postponed,
        destination = states.second_reading,
        permission = "bungeni.bill.Schedule",
        ) )


    add( workflow.Transition(
        transition_id = 'schedule-whole-house',
        title=_(u"Schedule Whole House Committee"),
        trigger = iworkflow.MANUAL,
        source = states.second_reading,
        destination = states.house_pending,
        permission = "bungeni.bill.Schedule",
        ) )
        
    add( workflow.Transition(
        transition_id = 'schedule-whole-house',
        title=_(u"Do Schedule Whole House Committee"),
        trigger = iworkflow.MANUAL,
        source = states.house_pending,
        destination = states.whole_house,
        permission = "bungeni.bill.Schedule",
        ) )        
        
    add( workflow.Transition(
        transition_id = 'postpone-whole-house',
        title=_(u"Postpone Whole House Committee"),
        trigger = iworkflow.MANUAL,
        source = states.whole_house,
        destination = states.whole_house_postponed,
        permission = "bungeni.bill.Schedule",
        ) )        
        
    add( workflow.Transition(
        transition_id = 'reschedule-whole-house',
        title=_(u"Reschedule Whole House Committee"),
        trigger = iworkflow.MANUAL,
        source = states.whole_house_postponed,
        destination = states.whole_house,
        permission = "bungeni.bill.Schedule",
        ) )       
        
        
    add( workflow.Transition(
        transition_id = 'postpone-second-reading-and-whole-house',
        title=_(u"Postpone Second Reading and Whole House Committee"),
        trigger = iworkflow.MANUAL,
        source = states.whole_house,
        destination = states.second_reading_postponed,
        permission = "bungeni.bill.Schedule",
        ) )   
   
        
    add( workflow.Transition(
        transition_id = 'select-second-committee',
        title=_(u"Send to Committee"),
        trigger = iworkflow.MANUAL,
        source = states.whole_house,
        destination = states.second_committee,
        permission = "bungeni.bill.SelectCommittee",
        ) )
        
    add( workflow.Transition(
        transition_id = 'ma-schedule-second-report-reading',
        title=_(u"Schedule Report Reading"),
        trigger = iworkflow.MANUAL,
        source = states.second_committee,
        destination = states.report_reading_pending,
        permission = "bungeni.bill.SelectCommittee",
        ) )        
        
    add( workflow.Transition(
        transition_id = 'schedule-second-report-reading',
        title=_(u"Schedule Report Reading"),
        trigger = iworkflow.MANUAL,
        source = states.report_reading_pending,
        destination = states.report_reading,
        permission = "bungeni.bill.SelectCommittee",
        ) )                

    add( workflow.Transition(
        transition_id = 'postpone-second-report-reading',
        title=_(u"Postpone Report Reading"),
        trigger = iworkflow.MANUAL,
        source = states.report_reading,
        destination = states.report_reading_postponed,
        permission = "bungeni.bill.SelectCommittee",
        ) )       

    add( workflow.Transition(
        transition_id = 'reschedule-second-report-reading',
        title=_(u"Reschedule Report Reading"),
        trigger = iworkflow.MANUAL,
        source = states.report_reading_postponed,
        destination = states.report_reading,
        permission = "bungeni.bill.SelectCommittee",
        ) )       

        



    add( workflow.Transition(
        transition_id = 'ma-second-committee-schedule-third-reading',
        title=_(u"Schedule Third Reading"),
        trigger = iworkflow.MANUAL,
        source = states.report_reading,
        destination = states.third_pending,
        permission = "bungeni.bill.Schedule",
        ) )  

    add( workflow.Transition(
        transition_id = 'second-committee-schedule-third-reading',
        title=_(u"Schedule Third Reading"),
        trigger = iworkflow.MANUAL,
        source = states.third_pending,
        destination = states.third_reading,
        permission = "bungeni.bill.Schedule",
        ) )  


    add( workflow.Transition(
        transition_id = 'recommit-second-committee',
        title=_(u"Recommit to 2nd Committee"),
        trigger = iworkflow.MANUAL,
        source = states.report_reading,
        destination = states.second_committee,
        permission = "bungeni.bill.SelectCommittee",
        ) )  



        

##     add( workflow.Transition(
##         transition_id = 'recommital',
##         title=_(u"Recommit Bill"),
##         source = states.second_reading,
##         destination = states.whole_house,
##         permission = "bungeni.bill.Recommit",
##         ) )

    add( workflow.Transition(
        transition_id = 'ma-schedule-third-reading',
        title=_(u"Schedule Third Reading"),
        trigger = iworkflow.MANUAL,
        source = states.whole_house,
        destination = states.third_pending,
        permission = "bungeni.bill.Schedule",
        ) )

        
    add( workflow.Transition(
        transition_id = 'postpone-third-reading',
        title=_(u"Postpone Third Reading"),
        trigger = iworkflow.MANUAL,
        source = states.third_reading,
        destination = states.third_reading_postponed,
        permission = "bungeni.bill.Schedule",
        ) )        

    add( workflow.Transition(
        transition_id = 'reschedule-third-reading',
        title=_(u"Postpone Third Reading"),
        trigger = iworkflow.MANUAL,
        source = states.third_reading_postponed,
        destination = states.third_reading,
        permission = "bungeni.bill.Schedule",
        ) )        


    add( workflow.Transition(
        transition_id = 'reject',
        title=_(u"Rejected"),
        trigger = iworkflow.MANUAL,
        source = states.third_reading,
        destination = states.rejected,
        permission = "bungeni.bill.ChangeStatus",
        ) )

    add( workflow.Transition(
        transition_id = 'approve',
        title=_(u"Approved"),
        trigger = iworkflow.MANUAL,
        source = states.third_reading,
        destination = states.approved,
        permission = "bungeni.bill.ChangeStatus",
        ) )    

    # Withdrawal of a bill 
    # The Member in Charge of a bill may withdraw the same at any stage without prior notice.

    add( workflow.Transition(
        transition_id = 'withdraw-submitted',
        title=_(u'Withdraw'),
        source = states.submitted,
        trigger = iworkflow.MANUAL,         
        action = withdraw,       
        destination = states.withdrawn,
        permission = 'bungeni.bill.Withdraw',        
        ) )   
        
    add( workflow.Transition(
        transition_id = 'withdraw-first-reading',
        title=_(u'Withdraw'),
        source = states.first_reading,
        trigger = iworkflow.MANUAL,         
        action = withdraw,       
        destination = states.withdrawn,
        permission = 'bungeni.bill.Withdraw',        
        ) )          
    
    add( workflow.Transition(
        transition_id = 'withdraw-first-committee',
        title=_(u'Withdraw'),
        source = states.first_committee,
        trigger = iworkflow.MANUAL,         
        action = withdraw,       
        destination = states.withdrawn,
        permission = 'bungeni.bill.Withdraw',        
        ) )    
        
        
    add( workflow.Transition(
        transition_id = 'withdraw-second-reading',
        title=_(u'Withdraw'),
        source = states.second_reading,
        trigger = iworkflow.MANUAL,         
        action = withdraw,       
        destination = states.withdrawn,
        permission = 'bungeni.bill.Withdraw',        
        ) )    
        
        
    add( workflow.Transition(
        transition_id = 'withdraw-whole-house',
        title=_(u'Withdraw'),
        source = states.whole_house,
        trigger = iworkflow.MANUAL,         
        action = withdraw,       
        destination = states.withdrawn,
        permission = 'bungeni.bill.Withdraw',        
        ) )    
        
        
    add( workflow.Transition(
        transition_id = 'withdraw-second-committee',
        title=_(u'Withdraw'),
        source = states.second_committee,
        trigger = iworkflow.MANUAL,         
        action = withdraw,       
        destination = states.withdrawn,
        permission = 'bungeni.bill.Withdraw',        
        ) )    
        
    add( workflow.Transition(
        transition_id = 'withdraw-report-reading',
        title=_(u'Withdraw'),
        source = states.report_reading,
        trigger = iworkflow.MANUAL,         
        action = withdraw,       
        destination = states.withdrawn,
        permission = 'bungeni.bill.Withdraw',        
        ) )    
        
    add( workflow.Transition(
        transition_id = 'withdraw-third-reading',
        title=_(u'Withdraw'),
        source = states.third_reading,
        trigger = iworkflow.MANUAL,         
        action = withdraw,       
        destination = states.withdrawn,
        permission = 'bungeni.bill.Withdraw',        
        ) )                                                
    
    
    
    
    return transitions
 
class BillWorkflow( workflow.Workflow ):

    def __init__( self ):
        super( BillWorkflow, self ).__init__( create_bill_workflow() )

BillWorkflowAdapter = workflow.AdaptedWorkflow( BillWorkflow() )

if __name__ == '__main__':
    wf = BillWorkflow()
    print wf.dot()
    
         
        
