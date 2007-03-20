# -*- coding: utf-8 -*-
#
# File: Bungeni.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 1.6.0-beta-svn
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

def setupParliamentaryEventWorkflow(self, workflow):
    """Define the ParliamentaryEventWorkflow workflow.
    """
    # Add additional roles to portal
    portal = getToolByName(self,'portal_url').getPortalObject()
    data = list(portal.__ac_roles__)
    for role in ['ReviewerForSpeaker']:
        if not role in data:
            data.append(role)
            # add to portal_role_manager
            # first try to fetch it. if its not there, we probaly have no PAS 
            # or another way to deal with roles was configured.            
            try:
                prm = portal.acl_users.get('portal_role_manager', None)
                if prm is not None:
                    try:
                        prm.addRole(role, role, 
                                    "Added by product 'Bungeni'/workflow 'ParliamentaryEventWorkflow'")
                    except KeyError: # role already exists
                        pass
            except AttributeError:
                pass
    portal.__ac_roles__ = tuple(data)

    workflow.setProperties(title='ParliamentaryEventWorkflow')

    ##code-section create-workflow-setup-method-header #fill in your manual code here
    ##/code-section create-workflow-setup-method-header


    for s in ['pending_edit', 'pending_approval', 'admissable', 'scheduled', 'tabled', 'draft']:
        workflow.states.addState(s)

    for t in ['submit_to_speaker', 'schedule', 'table', 'postpone', 'reject', 'approve', 'submit_to_clerk']:
        workflow.transitions.addTransition(t)

    for v in ['review_history', 'comments', 'time', 'actor', 'action']:
        workflow.variables.addVariable(v)

    workflow.addManagedPermission('Access contents information')
    workflow.addManagedPermission('Change portal events')
    workflow.addManagedPermission('Modify portal content')
    workflow.addManagedPermission('View')
    workflow.addManagedPermission('Review portal content')
    workflow.addManagedPermission('Bungeni: Schedule parliamentary business')
    workflow.addManagedPermission('Change Portal Events')

    for l in ['speaker_admissable_worklist', 'speaker_worklist', 'reviewer_queue']:
        if not l in workflow.worklists.objectValues():
            workflow.worklists.addWorklist(l)

    ## Initial State

    workflow.states.setInitialState('draft')

    ## States initialization

    stateDef = workflow.states['pending_edit']
    stateDef.setProperties(title="""pending_edit""",
                           description="""""",
                           transitions=['submit_to_speaker', 'reject'])
    stateDef.setPermission('Access contents information',
                           1,
                           ['Manager', 'Owner', 'Reviewer'])
    stateDef.setPermission('Change portal events',
                           0,
                           ['Manager', 'Reviewer'])
    stateDef.setPermission('Modify portal content',
                           0,
                           ['Manager', 'Reviewer'])
    stateDef.setPermission('View',
                           0,
                           ['Manager', 'Reviewer', 'Owner'])

    stateDef = workflow.states['pending_approval']
    stateDef.setProperties(title="""pending_approval""",
                           description="""""",
                           transitions=['reject', 'approve'])
    stateDef.setPermission('Access contents information',
                           0,
                           ['Manager', 'Owner', 'ReviewerForSpeaker', 'Reviewer'])
    stateDef.setPermission('Change portal events',
                           0,
                           ['Manager', 'ReviewerForSpeaker'])
    stateDef.setPermission('Modify portal content',
                           0,
                           ['Manager', 'ReviewerForSpeaker'])
    stateDef.setPermission('View',
                           0,
                           ['Manager', 'Owner', 'ReviewerForSpeaker', 'Reviewer'])
    stateDef.setPermission('Review portal content',
                           0,
                           ['Manager', 'ReviewerForSpeaker'])
    stateDef.setPermission('Bungeni: Schedule parliamentary business',
                           0,
                           ['Manager', 'ReviewerForSpeaker'])

    stateDef = workflow.states['admissable']
    stateDef.setProperties(title="""admissable""",
                           description="""""",
                           transitions=['schedule'])
    stateDef.setPermission('Access contents information',
                           0,
                           ['Manager', 'Owner', 'ReviewerForSpeaker', 'Reviewer'])
    stateDef.setPermission('Change portal events',
                           0,
                           ['Manager', 'ReviewerForSpeaker'])
    stateDef.setPermission('Modify portal content',
                           0,
                           ['Manager', 'ReviewerForSpeaker'])
    stateDef.setPermission('View',
                           0,
                           ['Manager', 'Owner', 'ReviewerForSpeaker', 'Reviewer'])
    stateDef.setPermission('Review portal content',
                           0,
                           ['Manager', 'ReviewerForSpeaker'])
    stateDef.setPermission('Bungeni: Schedule parliamentary business',
                           0,
                           ['Manager', 'ReviewerForSpeaker'])

    stateDef = workflow.states['scheduled']
    stateDef.setProperties(title="""scheduled""",
                           description="""""",
                           transitions=['postpone', 'table'])
    stateDef.setPermission('Access contents information',
                           1,
                           ['Anonymous', 'Manager', 'ReviewerForSpeaker'])
    stateDef.setPermission('Change Portal Events',
                           0,
                           ['Manager', 'ReviewerForSpeaker'])
    stateDef.setPermission('Modify portal content',
                           0,
                           ['Manager', 'ReviewerForSpeaker'])
    stateDef.setPermission('View',
                           1,
                           ['Manager', 'ReviewerForSpeaker'])

    stateDef = workflow.states['tabled']
    stateDef.setProperties(title="""tabled""",
                           description="""""",
                           transitions=[])
    stateDef.setPermission('Access contents information',
                           1,
                           ['Anonymous', 'Manager'])
    stateDef.setPermission('Change Portal Events',
                           0,
                           ['Manager'])
    stateDef.setPermission('Modify portal content',
                           0,
                           ['Manager'])
    stateDef.setPermission('View',
                           1,
                           ['Manager'])

    stateDef = workflow.states['draft']
    stateDef.setProperties(title="""draft""",
                           description="""""",
                           transitions=['submit_to_clerk'])
    stateDef.setPermission('Access contents information',
                           0,
                           ['Manager', 'Owner'])
    stateDef.setPermission('Change portal events',
                           0,
                           ['Manager', 'Owner'])
    stateDef.setPermission('Modify portal content',
                           0,
                           ['Manager', 'Owner'])
    stateDef.setPermission('View',
                           0,
                           ['Manager', 'Owner'])

    ## Transitions initialization

    transitionDef = workflow.transitions['submit_to_speaker']
    transitionDef.setProperties(title="""submit_to_speaker""",
                                new_state_id="""pending_approval""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""submit_to_speaker""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_permissions': 'Review portal content'},
                                )

    transitionDef = workflow.transitions['schedule']
    transitionDef.setProperties(title="""schedule""",
                                new_state_id="""scheduled""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""schedule""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_permissions': 'Bungeni: Schedule parliamentary business'},
                                )

    transitionDef = workflow.transitions['table']
    transitionDef.setProperties(title="""table""",
                                new_state_id="""tabled""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""table""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_permissions': 'Bungeni: Schedule parliamentary business'},
                                )

    transitionDef = workflow.transitions['postpone']
    transitionDef.setProperties(title="""postpone""",
                                new_state_id="""admissable""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""postpone""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_permissions': 'Bungeni: Schedule parliamentary business'},
                                )

    transitionDef = workflow.transitions['reject']
    transitionDef.setProperties(title="""reject""",
                                new_state_id="""draft""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""reject""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_permissions': 'Review portal content'},
                                )

    transitionDef = workflow.transitions['approve']
    transitionDef.setProperties(title="""approve""",
                                new_state_id="""admissable""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""approve""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_permissions': 'Bungeni: Schedule parliamentary business'},
                                )

    transitionDef = workflow.transitions['submit_to_clerk']
    transitionDef.setProperties(title="""submit_to_clerk""",
                                new_state_id="""pending_edit""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""submit_to_clerk""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={},
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

    worklistDef = workflow.worklists['speaker_admissable_worklist']
    worklistStates = ['admissable']
    actbox_url = "%(portal_url)s/search?review_state=" + "&review_state=".join(worklistStates)
    worklistDef.setProperties(description="Reviewer tasks",
                              actbox_name="Pending (%(count)d)",
                              actbox_url=actbox_url,
                              actbox_category="global",
                              props={'guard_permissions': 'Review portal content',
                                     'guard_roles': '',
                                     'var_match_review_state': ';'.join(worklistStates)})
    worklistDef = workflow.worklists['speaker_worklist']
    worklistStates = ['pending_approval']
    actbox_url = "%(portal_url)s/search?review_state=" + "&review_state=".join(worklistStates)
    worklistDef.setProperties(description="Reviewer tasks",
                              actbox_name="Pending (%(count)d)",
                              actbox_url=actbox_url,
                              actbox_category="global",
                              props={'guard_permissions': 'Review portal content',
                                     'guard_roles': '',
                                     'var_match_review_state': ';'.join(worklistStates)})
    worklistDef = workflow.worklists['reviewer_queue']
    worklistStates = ['pending_edit']
    actbox_url = "%(portal_url)s/search?review_state=" + "&review_state=".join(worklistStates)
    worklistDef.setProperties(description="Reviewer tasks",
                              actbox_name="Pending (%(count)d)",
                              actbox_url=actbox_url,
                              actbox_category="global",
                              props={'guard_permissions': 'Review portal content',
                                     'guard_roles': '',
                                     'var_match_review_state': ';'.join(worklistStates)})

    # WARNING: below protected section is deprecated.
    # Add a tagged value 'worklist' with the worklist name to your state(s) instead.

    ##code-section create-workflow-setup-method-footer #fill in your manual code here
    ##/code-section create-workflow-setup-method-footer



def createParliamentaryEventWorkflow(self, id):
    """Create the workflow for Bungeni.
    """

    ob = DCWorkflowDefinition(id)
    setupParliamentaryEventWorkflow(self, ob)
    return ob

addWorkflowFactory(createParliamentaryEventWorkflow,
                   id='ParliamentaryEventWorkflow',
                   title='ParliamentaryEventWorkflow')

##code-section create-workflow-module-footer #fill in your manual code here
##/code-section create-workflow-module-footer

