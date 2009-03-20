import events
import datetime
import zope.component
from ore.workflow.interfaces import IWorkflow, IWorkflowInfo
import ore.workflow.workflow
import bungeni.core.version
from bungeni.models import domain
import bungeni.models.interfaces
import bungeni.core.workflows.adapters
import alchemist.security.permission
import alchemist.security.role
import zope.securitypolicy.interfaces
from ore.alchemist import Session


def provide_transition_events_check(wf):
    event_map = dict(
        ((t.source, t.destination), False) for t in \
        events.get_workflow_transitions(wf) if t.event)

    for states, iface in events.workflow_transition_event_map.items():
        def generate(key):
            def handler(event):
                event_map[key] = True
            return handler
        zope.component.provideHandler(generate(states), adapts=(iface,))

    return event_map
    
    

def transitions(item):
    wf = IWorkflow(item)
    info = IWorkflowInfo(item)
    state = info.state().getState()
    return tuple(transition.transition_id 
               for transition in wf.getTransitions(state))


def permission(item):
    wf = IWorkflow(item)
    info = IWorkflowInfo(item)
    state = info.state().getState()
    return tuple(transition.permission 
                for transition in wf.getTransitions(state))



def setup_adapters():  
    zope.component.provideAdapter(
        bungeni.core.workflows.states.WorkflowState,
        (bungeni.models.interfaces.IBungeniContent,))

    zope.component.provideAdapter(
        bungeni.core.workflows.adapters.QuestionWorkflowAdapter,
        (domain.Question,))

    zope.component.provideAdapter(
        ore.workflow.workflow.WorkflowInfo,
        (domain.Question,))

    zope.component.provideAdapter(
        bungeni.core.workflows.adapters.BillWorkflowAdapter,
        (domain.Bill,))

    zope.component.provideAdapter(
        ore.workflow.workflow.WorkflowInfo,
        (domain.Bill,))

    zope.component.provideAdapter(
        bungeni.core.workflows.adapters.MotionWorkflowAdapter,
        (domain.Motion,))

    zope.component.provideAdapter(
        ore.workflow.workflow.WorkflowInfo,
        (domain.Motion,))

    zope.component.provideAdapter(
        bungeni.core.workflows.adapters.ResponseWorkflowAdapter,
        (domain.Response,))

    zope.component.provideAdapter(
        ore.workflow.workflow.WorkflowInfo,
        (domain.Response,))

    zope.component.provideHandler(
        bungeni.core.workflows.events.workflowTransitionEventDispatcher)


    zope.component.provideAdapter(
        bungeni.core.version.ContextVersioned,
        (bungeni.core.interfaces.IVersionable,),
        bungeni.core.interfaces.IVersioned)

def setup_security_adapters():
    
    gsm =zope.component.getGlobalSiteManager()

    gsm.registerAdapter(
        alchemist.security.role.GlobalPrincipalRoleMap,
         (bungeni.models.interfaces.IBungeniApplication, ),
         zope.securitypolicy.interfaces.IPrincipalRoleMap)

    gsm.registerAdapter(
        alchemist.security.permission.GlobalRolePermissionMap,
         (bungeni.models.interfaces.IBungeniApplication, ),
         zope.securitypolicy.interfaces.IRolePermissionMap)     
      
      
    gsm.registerAdapter(
        alchemist.security.role.LocalPrincipalRoleMap,
         (bungeni.models.interfaces.IBungeniContent, ),
         zope.securitypolicy.interfaces.IPrincipalRoleMap)  
        
    gsm.registerAdapter(
        alchemist.security.permission.LocalRolePermissionMap,
         (bungeni.models.interfaces.IBungeniContent, ),
         zope.securitypolicy.interfaces.IRolePermissionMap) 

def schedule_item(item, sitting):
    session = Session()
    item_schedule = domain.ItemSchedule()
    item_schedule.sitting_id = sitting.sitting_id
    item_schedule.item_id = item.parliamentary_item_id
    session.add(item_schedule)
    session.flush()   
    
def create_sitting():    
    """Sitting to schedule motion/question/bill"""
    session = Session()
    
    st = domain.SittingType()
    st.sitting_type = u"morning"
    st.start_time = datetime.time(8,30)
    st.end_time = datetime.time(12,30)  
    session.add(st)
    session.flush()

    sitting = domain.GroupSitting()
    sitting.start_date = datetime.datetime.now()
    sitting.end_date = datetime.datetime.now()
    sitting.sitting_type_id = st.sitting_type_id
    session.add(sitting)
    session.flush()     
    
    return sitting
    
