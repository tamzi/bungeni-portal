# Bungeni Parliamentary Information System - http://www.bungeni.org/
# Copyright (C) 2010 - Africa i-Parliaments - http://www.parliaments.info/
# Licensed under GNU GPL v2 - http://www.gnu.org/licenses/gpl-2.0.txt

"""Loading of workflows and and set-up and registering of associated adapters.

$Id$
"""
log = __import__("logging").getLogger("bungeni.core.workflows")

from lxml import etree
from zope import component
from zope.interface import classImplements
import zope.securitypolicy.interfaces
from bungeni.models import interfaces
from bungeni.core.workflow import xmlimport
from bungeni.core.workflow.interfaces import IWorkflow, IWorkflowed, \
    IStateController, IWorkflowController
from bungeni.core.workflow.states import StateController, WorkflowController, \
    Workflow, get_object_state_rpm, get_head_object_state_rpm
import bungeni.core.audit
from bungeni.alchemist import utils
from bungeni.utils import naming, misc
from bungeni.utils.capi import capi, bungeni_custom_errors


def register_specific_workflow_adapter(ti):
    # Specific adapter on specific iface per workflow.
    # Workflows are also the factory of own AdaptedWorkflows
    assert ti.workflow, ti
    assert ti.interface, ti
    # component.provideAdapter(factory, adapts=None, provides=None, name="")
    component.provideAdapter(ti.workflow, (ti.interface,), IWorkflow)


def load_workflow(type_key, workflow_key,
        path_custom_workflows=capi.get_path_for("workflows")
    ):
    """Setup (once) and return the Workflow instance, from XML definition, 
    for named workflow.
    """
    # retrieve / load
    try:
        wf = Workflow.get_singleton(workflow_key)
        log.warn("Already Loaded WORKFLOW : %s %s" % (workflow_key, wf))
    except KeyError:
        wf = xmlimport.load(type_key, workflow_key, path_custom_workflows)
        log.debug("Loading WORKFLOW: %s %s" % (workflow_key, wf))
        # debug info
        for state_key, state in wf.states.items():
            log.debug("   STATE: %s %s" % (state_key, state))
            for p in state.permissions:
                log.debug("          %s" % (p,))
    return wf

def apply_customization_workflow(type_key, ti):
    """Apply customizations, features as per configuration from a workflow. 
    Must (currently) be run after db setup.
    """
    domain_model = ti.domain_model
    # We "mark" the domain class with IWorkflowed, to be able to 
    # register/lookup adapters generically on this single interface.
    #assert not IWorkflowed.implementedBy(domain_model), domain_model
    if not IWorkflowed.implementedBy(domain_model):
        classImplements(domain_model, IWorkflowed)
    
    # dynamic features from workflow
    wf = ti.workflow
    # decorate/modify domain/schema/mapping as needed
    from bungeni.models import domain, orm
    domain_model = domain.configurable_domain(domain_model, wf)
    orm.configurable_mappings(domain_model)
    
    # !+ following should be part of the domain.feature_audit(domain_model) logic
    if wf.has_feature("audit"):
        # create/set module-level dedicated auditor singleton for auditable domain_model
        bungeni.core.audit.set_auditor(domain_model)


def get_domain_model(type_key):
    """Infer and retrieve the target domain model class from the type key.
    Raise Attribute error if not defined on domain.
    """
    from bungeni.models import domain
    return getattr(domain, naming.model_name(type_key))

def load_workflows(type_info_iterator):
    # workflow instances (+ adapter *factories*)
    for type_key, ti in type_info_iterator:
        # get the domain class, and associate with type
        utils.inisetattr(ti, "domain_model", get_domain_model(type_key))
        # load/get workflow instance (if any) and associate with type
        if ti.workflow_key is not None:
            ti.workflow = load_workflow(type_key, ti.workflow_key)
            # adjust domain_model as per workflow, register/associate domain_model
            apply_customization_workflow(type_key, ti)
            register_specific_workflow_adapter(ti)


def register_generic_workflow_adapters():
    """Register general and specific worklfow-related adapters.
    
    Note: as the registry is cleared when placelessetup.tearDown() is called,
    this needs to be called independently on each doctest.
    """
    # General adapters on generic IWorkflowed (once for all workflows).
    
    # IRolePermissionMap adapter for IWorkflowed objects
    component.provideAdapter(get_object_state_rpm, 
        (IWorkflowed,),
        zope.securitypolicy.interfaces.IRolePermissionMap)
    # NOTE: the rpm instance returned by IRolePermissionMap(workflowed) is
    # different for different values of workflowed.status
    
    # IRolePermissionMap adapter for a change of an IWorkflowed object
    component.provideAdapter(get_head_object_state_rpm, 
        (interfaces.IChange,),
        zope.securitypolicy.interfaces.IRolePermissionMap)
    # NOTE: the rpm instance returned by IRolePermissionMap(change) is
    # different for different values of change.head.status
    
    # !+IPrincipalRoleMap(mr, aug-2011) also migrate principal_role_map from 
    # db to be dynamic and based on workflow definitions. Would need to infer
    # the Roles of a user with respect to the context e.g.owner, or signatory
    # and then check against the permissions required by the current object's
    # state. 
    
    # IStateController
    component.provideAdapter(
        StateController, (IWorkflowed,), IStateController)
    # IWorkflowController
    component.provideAdapter(
        WorkflowController, (IWorkflowed,), IWorkflowController)

    
@bungeni_custom_errors
def register_custom_types():
    """Extend TYPE_REGISTRY with the declarations from bungeni_custom/types.xml.
    """
    from zope.dottedname.resolve import resolve
    from bungeni.alchemist.type_info import TYPE_REGISTRY, TI
    def register_type(elem):
        if not misc.xml_attr_bool(elem, "enabled", default=True):
            # not enabled, ignore
            return
        type_key = misc.xml_attr_str(elem, "name")
        workflow_key = misc.xml_attr_str(elem, "workflow", default=type_key)
        interface = resolve("bungeni.models.interfaces.%s" % (
                naming.model_interface_name(type_key)))
        ti = TI(workflow_key, interface)
        ti.custom = True
        TYPE_REGISTRY.append((type_key, ti))
        log.info("Registering custom type [%s]: %s" % (elem.tag, type_key))
    
    # load XML file
    etypes = etree.fromstring(misc.read_file(capi.get_path_for("types.xml")))
    # register types
    for edoc in etypes.iterchildren("doc"):
        register_type(edoc)
    # group/member types
    for egroup in etypes.iterchildren("group"):
        register_type(egroup)
        for emember in egroup.iterchildren("member"):
            register_type(emember)


def _setup_all():
    """Do all workflow related setup.
    """
    log.info("adapters._setup_all() ------------------------------------------")
    # cleared by each call to zope.app.testing.placelesssetup.tearDown()
    register_generic_workflow_adapters()
    
    # load workflows for system/registered types
    load_workflows(capi.iter_type_info())
    
    # extend type registry with custom types
    register_custom_types()
    load_workflows(capi.iter_type_info(scope="custom"))
    
    # !+zcml_check_regenerate(mr, sep-2011) should be only done *once* and 
    # when *all* workflows are loaded.
    # check/regenerate zcml directives for workflows
    xmlimport.zcml_check_regenerate()

# do it (when this module is loaded)
_setup_all()

#

