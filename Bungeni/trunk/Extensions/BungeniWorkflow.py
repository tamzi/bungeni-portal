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

def setupBungeniWorkflow(self, workflow):
    """Define the BungeniWorkflow workflow.
    """
    # Add additional roles to portal
    portal = getToolByName(self,'portal_url').getPortalObject()
    data = list(portal.__ac_roles__)
    for role in ['CurrentMP']:
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
                                    "Added by product 'Bungeni'/workflow 'BungeniWorkflow'")
                    except KeyError: # role already exists
                        pass
            except AttributeError:
                pass
    portal.__ac_roles__ = tuple(data)

    workflow.setProperties(title='BungeniWorkflow')

    ##code-section create-workflow-setup-method-header #fill in your manual code here
    ##/code-section create-workflow-setup-method-header


    for s in ['private', 'pending', 'published', 'draft']:
        workflow.states.addState(s)

    for t in ['hide', 'submit', 'reject', 'retract', 'show', 'publish']:
        workflow.transitions.addTransition(t)

    for v in ['review_history', 'comments', 'time', 'actor', 'action']:
        workflow.variables.addVariable(v)

    workflow.addManagedPermission('Access contents information')
    workflow.addManagedPermission('Change portal events')
    workflow.addManagedPermission('Modify portal content')
    workflow.addManagedPermission('View')

    for l in ['reviewer_queue']:
        if not l in workflow.worklists.objectValues():
            workflow.worklists.addWorklist(l)

    ## Initial State

    workflow.states.setInitialState('draft')

    ## States initialization

    stateDef = workflow.states['private']
    stateDef.setProperties(title="""private""",
                           description="""""",
                           transitions=['show'])
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

    stateDef = workflow.states['pending']
    stateDef.setProperties(title="""pending""",
                           description="""""",
                           transitions=['publish', 'hide', 'reject', 'retract'])
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
                           1,
                           ['Manager', 'Owner', 'Reviewer'])

    stateDef = workflow.states['published']
    stateDef.setProperties(title="""published""",
                           description="""""",
                           transitions=['reject', 'retract'])
    stateDef.setPermission('Access contents information',
                           1,
                           ['Anonymous', 'Manager'])
    stateDef.setPermission('Change portal events',
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
                           transitions=['hide', 'submit', 'publish'])
    stateDef.setPermission('Access contents information',
                           0,
                           ['Authenticated', 'Manager', 'Reviewer'])
    stateDef.setPermission('Change portal events',
                           0,
                           ['Manager', 'Owner'])
    stateDef.setPermission('Modify portal content',
                           0,
                           ['Manager', 'Owner'])
    stateDef.setPermission('View',
                           0,
                           ['Authenticated', 'Manager', 'Reviewer'])
    stateDef.setPermission('Bungeni: Add Amendment',
                           0,
                           ['Manager', 'CurrentMP'])
    stateDef.setPermission('Bungeni: Add Question',
                           0,
                           ['Manager', 'CurrentMP'])
    stateDef.setPermission('Bungeni: Add HansardFolder',
                           0,
                           ['Manager'])
    stateDef.setPermission('Bungeni: Add HelpFolder',
                           0,
                           ['Manager'])
    stateDef.setPermission('Bungeni: Add LegislationFolder',
                           0,
                           ['Manager'])

    ## Transitions initialization

    transitionDef = workflow.transitions['hide']
    transitionDef.setProperties(title="""Make private""",
                                new_state_id="""private""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""Make private""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_roles': 'Owner'},
                                )

    transitionDef = workflow.transitions['submit']
    transitionDef.setProperties(title="""Submit""",
                                new_state_id="""pending""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""Submit""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_permissions': 'Request review'},
                                )

    transitionDef = workflow.transitions['reject']
    transitionDef.setProperties(title="""Reject""",
                                new_state_id="""draft""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""Reject""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_permissions': 'Review portal content'},
                                )

    transitionDef = workflow.transitions['retract']
    transitionDef.setProperties(title="""Retract""",
                                new_state_id="""draft""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""Retract""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_permissions': 'Request review'},
                                )

    transitionDef = workflow.transitions['show']
    transitionDef.setProperties(title="""Make visible""",
                                new_state_id="""draft""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""Make visible""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_roles': 'Owner'},
                                )

    transitionDef = workflow.transitions['publish']
    transitionDef.setProperties(title="""Publish""",
                                new_state_id="""published""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""Publish""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_permissions': 'Review portal content'},
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

    worklistDef = workflow.worklists['reviewer_queue']
    worklistStates = ['pending']
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



def createBungeniWorkflow(self, id):
    """Create the workflow for Bungeni.
    """

    ob = DCWorkflowDefinition(id)
    setupBungeniWorkflow(self, ob)
    return ob

addWorkflowFactory(createBungeniWorkflow,
                   id='BungeniWorkflow',
                   title='BungeniWorkflow')

##code-section create-workflow-module-footer #fill in your manual code here
##/code-section create-workflow-module-footer

