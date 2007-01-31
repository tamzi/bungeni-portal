# -*- coding: utf-8 -*-
#
# File: Bungeni.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 1.5.1-svn
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """Jean Jordaan <jean.jordaan@gmail.com>"""
__docformat__ = 'plaintext'


from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowTool import addWorkflowFactory
from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition
from Products.ExternalMethod.ExternalMethod import ExternalMethod
from Products.Bungeni.config import *

##code-section create-workflow-module-header #fill in your manual code here
##/code-section create-workflow-module-header


productname = 'Bungeni'

def setupMemberApprovalWorkflow(self, workflow):
    """Define the MemberApprovalWorkflow workflow.
    """

    workflow.setProperties(title='MemberApprovalWorkflow')

    ##code-section create-workflow-setup-method-header #fill in your manual code here
    ##/code-section create-workflow-setup-method-header


    for s in ['pending', 'disabled', 'private', 'public', 'new']:
        workflow.states.addState(s)

    for t in ['enable_private', 'make_private', 'auto_submit', 'make_public', 'register_public', 'enable_pending', 'enable_public', 'trigger', 'register_private', 'disable']:
        workflow.transitions.addTransition(t)

    for v in ['review_history', 'comments', 'time', 'actor', 'action']:
        workflow.variables.addVariable(v)

    workflow.addManagedPermission('Copy or Move')
    workflow.addManagedPermission('Mail forgotten password')
    workflow.addManagedPermission('Manage users')
    workflow.addManagedPermission('Modify portal content')
    workflow.addManagedPermission('Set own password')
    workflow.addManagedPermission('Set own properties')
    workflow.addManagedPermission('View')
    workflow.addManagedPermission('membrane: Edit member id')
    workflow.addManagedPermission('membrane: Register member')
    workflow.addManagedPermission('Access contents information')

    for l in []:
        if not l in workflow.worklists.objectValues():
            workflow.worklists.addWorklist(l)

    ## Initial State

    workflow.states.setInitialState('new')

    ## States initialization

    stateDef = workflow.states['pending']
    stateDef.setProperties(title="""Awaiting registration""",
                           description="""""",
                           transitions=['disable', 'register_private', 'register_public'])
    stateDef.setPermission('Copy or Move',
                           0,
                           ['Manager'])
    stateDef.setPermission('Mail forgotten password',
                           0,
                           ['Manager'])
    stateDef.setPermission('Manage users',
                           0,
                           ['Manager'])
    stateDef.setPermission('Modify portal content',
                           0,
                           ['Manager'])
    stateDef.setPermission('Set own password',
                           0,
                           ['Manager'])
    stateDef.setPermission('Set own properties',
                           0,
                           ['Manager'])
    stateDef.setPermission('View',
                           0,
                           ['Manager'])
    stateDef.setPermission('membrane: Edit member id',
                           0,
                           ['Manager'])
    stateDef.setPermission('membrane: Register member',
                           0,
                           ['Manager'])
    stateDef.setPermission('Access contents information',
                           0,
                           ['Manager'])

    stateDef = workflow.states['disabled']
    stateDef.setProperties(title="""Disabled""",
                           description="""""",
                           transitions=['enable_pending', 'enable_public', 'enable_private'])
    stateDef.setPermission('Copy or Move',
                           0,
                           ['Manager'])
    stateDef.setPermission('Mail forgotten password',
                           0,
                           ['Manager'])
    stateDef.setPermission('Manage users',
                           0,
                           ['Manager'])
    stateDef.setPermission('Modify portal content',
                           0,
                           ['Manager'])
    stateDef.setPermission('Set own password',
                           0,
                           ['Manager'])
    stateDef.setPermission('Set own properties',
                           0,
                           ['Manager'])
    stateDef.setPermission('View',
                           0,
                           ['Manager'])
    stateDef.setPermission('membrane: Edit member id',
                           0,
                           ['Manager'])
    stateDef.setPermission('membrane: Register member',
                           0,
                           ['Manager'])
    stateDef.setPermission('Access contents information',
                           0,
                           ['Manager'])

    stateDef = workflow.states['private']
    stateDef.setProperties(title="""Registered user, private profile""",
                           description="""""",
                           transitions=['make_public', 'disable'])
    stateDef.setPermission('Copy or Move',
                           0,
                           ['Manager'])
    stateDef.setPermission('Mail forgotten password',
                           0,
                           ['Anonymous', 'Manager', 'Owner'])
    stateDef.setPermission('Manage users',
                           0,
                           ['Manager'])
    stateDef.setPermission('Modify portal content',
                           0,
                           ['Manager', 'Owner'])
    stateDef.setPermission('Set own password',
                           0,
                           ['Manager', 'Owner'])
    stateDef.setPermission('Set own properties',
                           0,
                           ['Manager', 'Owner'])
    stateDef.setPermission('View',
                           0,
                           ['Manager', 'Owner'])
    stateDef.setPermission('membrane: Edit member id',
                           0,
                           ['Manager'])
    stateDef.setPermission('membrane: Register member',
                           0,
                           ['Manager'])
    stateDef.setPermission('Access contents information',
                           0,
                           ['Manager', 'Owner'])

    stateDef = workflow.states['public']
    stateDef.setProperties(title="""Registered user, public profile""",
                           description="""""",
                           transitions=['make_private', 'disable'])
    stateDef.setPermission('Copy or Move',
                           0,
                           ['Manager'])
    stateDef.setPermission('Mail forgotten password',
                           0,
                           ['Anonymous', 'Manager', 'Owner'])
    stateDef.setPermission('Manage users',
                           0,
                           ['Manager'])
    stateDef.setPermission('Modify portal content',
                           0,
                           ['Manager', 'Owner'])
    stateDef.setPermission('Set own password',
                           0,
                           ['Manager', 'Owner'])
    stateDef.setPermission('Set own properties',
                           0,
                           ['Manager', 'Owner'])
    stateDef.setPermission('View',
                           0,
                           ['Anonymous', 'Authenticated', 'Manager', 'Member', 'Owner'])
    stateDef.setPermission('membrane: Edit member id',
                           0,
                           ['Manager'])
    stateDef.setPermission('membrane: Register member',
                           0,
                           ['Manager'])
    stateDef.setPermission('Access contents information',
                           0,
                           ['Anonymous', 'Authenticated', 'Manager', 'Member', 'Owner'])

    stateDef = workflow.states['new']
    stateDef.setProperties(title="""Newly created member""",
                           description="""""",
                           transitions=['trigger', 'auto_submit'])
    stateDef.setPermission('Copy or Move',
                           0,
                           ['Manager'])
    stateDef.setPermission('Mail forgotten password',
                           0,
                           ['Manager'])
    stateDef.setPermission('Manage users',
                           0,
                           ['Manager'])
    stateDef.setPermission('Modify portal content',
                           0,
                           ['Anonymous', 'Manager'])
    stateDef.setPermission('Set own password',
                           0,
                           ['Anonymous', 'Manager'])
    stateDef.setPermission('Set own properties',
                           0,
                           ['Anonymous', 'Manager'])
    stateDef.setPermission('View',
                           0,
                           ['Anonymous', 'Manager'])
    stateDef.setPermission('membrane: Edit member id',
                           0,
                           ['Anonymous', 'Manager'])
    stateDef.setPermission('membrane: Register member',
                           0,
                           ['Manager'])
    stateDef.setPermission('Access contents information',
                           0,
                           ['Anonymous', 'Manager'])

    ## Transitions initialization

    ## Creation of workflow scripts
    for wf_scriptname in ['enable']:
        if not wf_scriptname in workflow.scripts.objectIds():
            workflow.scripts._setObject(wf_scriptname,
                ExternalMethod(wf_scriptname, wf_scriptname,
                productname + '.MemberApprovalWorkflow_scripts',
                wf_scriptname))

    transitionDef = workflow.transitions['enable_private']
    transitionDef.setProperties(title="""Re-enable member""",
                                new_state_id="""private""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""enable""",
                                actbox_name="""Re-enable member""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_expr': "python:getattr(here,'old_state',None) == 'private'", 'guard_permissions': 'Manage users'},
                                )

    transitionDef = workflow.transitions['make_private']
    transitionDef.setProperties(title="""Make member profile private""",
                                new_state_id="""private""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""Make member profile private""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_roles': 'Owner; Manager'},
                                )

    transitionDef = workflow.transitions['auto_submit']
    transitionDef.setProperties(title="""Automatically submit member""",
                                new_state_id="""pending""",
                                trigger_type=0,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""Automatically submit member""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_expr': 'here/isValid', 'guard_permissions': 'Request review'},
                                )

    transitionDef = workflow.transitions['make_public']
    transitionDef.setProperties(title="""make_public""",
                                new_state_id="""public""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""make_public""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={},
                                )

    ## Creation of workflow scripts
    for wf_scriptname in ['register']:
        if not wf_scriptname in workflow.scripts.objectIds():
            workflow.scripts._setObject(wf_scriptname,
                ExternalMethod(wf_scriptname, wf_scriptname,
                productname + '.MemberApprovalWorkflow_scripts',
                wf_scriptname))

    transitionDef = workflow.transitions['register_public']
    transitionDef.setProperties(title="""Approve member, make profile public""",
                                new_state_id="""public""",
                                trigger_type=1,
                                script_name="""register""",
                                after_script_name="""""",
                                actbox_name="""Approve member, make profile public""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_permissions': 'membrane: Register member'},
                                )

    ## Creation of workflow scripts
    for wf_scriptname in ['enable']:
        if not wf_scriptname in workflow.scripts.objectIds():
            workflow.scripts._setObject(wf_scriptname,
                ExternalMethod(wf_scriptname, wf_scriptname,
                productname + '.MemberApprovalWorkflow_scripts',
                wf_scriptname))

    transitionDef = workflow.transitions['enable_pending']
    transitionDef.setProperties(title="""Re-enable member""",
                                new_state_id="""pending""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""enable""",
                                actbox_name="""Re-enable member""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_expr': "python:getattr(here,'old_state',None) == 'pending'", 'guard_permissions': 'Manage users'},
                                )

    transitionDef = workflow.transitions['enable_public']
    transitionDef.setProperties(title="""enable_public""",
                                new_state_id="""public""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""enable_public""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={},
                                )

    transitionDef = workflow.transitions['trigger']
    transitionDef.setProperties(title="""Trigger automatic transitions""",
                                new_state_id="""new""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""Trigger automatic transitions""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={},
                                )

    ## Creation of workflow scripts
    for wf_scriptname in ['register']:
        if not wf_scriptname in workflow.scripts.objectIds():
            workflow.scripts._setObject(wf_scriptname,
                ExternalMethod(wf_scriptname, wf_scriptname,
                productname + '.MemberApprovalWorkflow_scripts',
                wf_scriptname))

    transitionDef = workflow.transitions['register_private']
    transitionDef.setProperties(title="""Approve member, make profile private""",
                                new_state_id="""private""",
                                trigger_type=1,
                                script_name="""register""",
                                after_script_name="""""",
                                actbox_name="""Approve member, make profile private""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_permissions': 'membrane: Register member'},
                                )

    ## Creation of workflow scripts
    for wf_scriptname in ['disable']:
        if not wf_scriptname in workflow.scripts.objectIds():
            workflow.scripts._setObject(wf_scriptname,
                ExternalMethod(wf_scriptname, wf_scriptname,
                productname + '.MemberApprovalWorkflow_scripts',
                wf_scriptname))

    transitionDef = workflow.transitions['disable']
    transitionDef.setProperties(title="""Disable member""",
                                new_state_id="""disabled""",
                                trigger_type=1,
                                script_name="""disable""",
                                after_script_name="""""",
                                actbox_name="""Disable member""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_permissions': 'Manage users'},
                                )

    ## State Variable
    workflow.variables.setStateVar('review_state')

    ## Variables initialization
    variableDef = workflow.variables['review_history']
    variableDef.setProperties(description="""Provides access to workflow history""",
                              default_value="""""",
                              default_expr="""state_change/getHistory""",
                              for_catalog=0,
                              for_status=0,
                              update_always=0,
                              props={'guard_permissions': 'Request review; Review portal content'})

    variableDef = workflow.variables['comments']
    variableDef.setProperties(description="""Comments about the last transition""",
                              default_value="""""",
                              default_expr="""python:state_change.kwargs.get('comment', '')""",
                              for_catalog=0,
                              for_status=1,
                              update_always=1,
                              props=None)

    variableDef = workflow.variables['time']
    variableDef.setProperties(description="""Time of the last transition""",
                              default_value="""""",
                              default_expr="""state_change/getDateTime""",
                              for_catalog=0,
                              for_status=1,
                              update_always=1,
                              props=None)

    variableDef = workflow.variables['actor']
    variableDef.setProperties(description="""The ID of the user who performed the last transition""",
                              default_value="""""",
                              default_expr="""user/getId""",
                              for_catalog=0,
                              for_status=1,
                              update_always=1,
                              props=None)

    variableDef = workflow.variables['action']
    variableDef.setProperties(description="""The last transition""",
                              default_value="""""",
                              default_expr="""transition/getId|nothing""",
                              for_catalog=0,
                              for_status=1,
                              update_always=1,
                              props=None)

    ## Worklists Initialization


    # WARNING: below protected section is deprecated.
    # Add a tagged value 'worklist' with the worklist name to your state(s) instead.

    ##code-section create-workflow-setup-method-footer #fill in your manual code here
    ##/code-section create-workflow-setup-method-footer



def createMemberApprovalWorkflow(self, id):
    """Create the workflow for Bungeni.
    """

    ob = DCWorkflowDefinition(id)
    setupMemberApprovalWorkflow(self, ob)
    return ob

addWorkflowFactory(createMemberApprovalWorkflow,
                   id='MemberApprovalWorkflow',
                   title='MemberApprovalWorkflow')

##code-section create-workflow-module-footer #fill in your manual code here
##/code-section create-workflow-module-footer

