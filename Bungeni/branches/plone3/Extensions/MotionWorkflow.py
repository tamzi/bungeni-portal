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

def setupMotionWorkflow(self, workflow):
    """Define the MotionWorkflow workflow.
    """

    workflow.setProperties(title='MotionWorkflow')

    ##code-section create-workflow-setup-method-header #fill in your manual code here
    ##/code-section create-workflow-setup-method-header


    for s in ['submitted', 'admissable', 'scheduled', 'moved', 'draft', 'accepted', 'rejected']:
        workflow.states.addState(s)

    for t in ['admit', 'submit', 'schedule', 'reject', 'amend', 'move', 'accept']:
        workflow.transitions.addTransition(t)

    for v in ['review_history', 'comments', 'time', 'actor', 'action']:
        workflow.variables.addVariable(v)


    for l in []:
        if not l in workflow.worklists.objectValues():
            workflow.worklists.addWorklist(l)

    ## Initial State

    workflow.states.setInitialState('draft')

    ## States initialization

    stateDef = workflow.states['submitted']
    stateDef.setProperties(title="""submitted""",
                           description="""""",
                           transitions=['admit', 'reject', 'amend'])

    stateDef = workflow.states['admissable']
    stateDef.setProperties(title="""admissable""",
                           description="""""",
                           transitions=['schedule'])

    stateDef = workflow.states['scheduled']
    stateDef.setProperties(title="""scheduled""",
                           description="""""",
                           transitions=['move'])

    stateDef = workflow.states['moved']
    stateDef.setProperties(title="""moved""",
                           description="""""",
                           transitions=['accept', 'reject'])

    stateDef = workflow.states['draft']
    stateDef.setProperties(title="""draft""",
                           description="""""",
                           transitions=['submit'])

    stateDef = workflow.states['accepted']
    stateDef.setProperties(title="""accepted""",
                           description="""""",
                           transitions=[])

    stateDef = workflow.states['rejected']
    stateDef.setProperties(title="""rejected""",
                           description="""""",
                           transitions=[])

    ## Transitions initialization

    transitionDef = workflow.transitions['admit']
    transitionDef.setProperties(title="""admit""",
                                new_state_id="""admissable""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""admit""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={},
                                )

    transitionDef = workflow.transitions['submit']
    transitionDef.setProperties(title="""submit""",
                                new_state_id="""submitted""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""submit""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={},
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
                                props={},
                                )

    transitionDef = workflow.transitions['reject']
    transitionDef.setProperties(title="""reject""",
                                new_state_id="""rejected""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""reject""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={},
                                )

    transitionDef = workflow.transitions['amend']
    transitionDef.setProperties(title="""amend""",
                                new_state_id="""draft""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""amend""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={},
                                )

    transitionDef = workflow.transitions['move']
    transitionDef.setProperties(title="""move""",
                                new_state_id="""moved""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""move""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={},
                                )

    transitionDef = workflow.transitions['accept']
    transitionDef.setProperties(title="""accept""",
                                new_state_id="""accepted""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""accept""",
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


    # WARNING: below protected section is deprecated.
    # Add a tagged value 'worklist' with the worklist name to your state(s) instead.

    ##code-section create-workflow-setup-method-footer #fill in your manual code here
    ##/code-section create-workflow-setup-method-footer



def createMotionWorkflow(self, id):
    """Create the workflow for Bungeni.
    """

    ob = DCWorkflowDefinition(id)
    setupMotionWorkflow(self, ob)
    return ob

addWorkflowFactory(createMotionWorkflow,
                   id='MotionWorkflow',
                   title='MotionWorkflow')

##code-section create-workflow-module-footer #fill in your manual code here
##/code-section create-workflow-module-footer

