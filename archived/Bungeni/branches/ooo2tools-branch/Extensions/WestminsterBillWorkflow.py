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

def setupWestminsterBillWorkflow(self, workflow):
    """Define the WestminsterBillWorkflow workflow.
    """

    workflow.setProperties(title='WestminsterBillWorkflow')

    ##code-section create-workflow-setup-method-header #fill in your manual code here
    ##/code-section create-workflow-setup-method-header


    for s in ['PresentedToParliament', 'CommittedToCommittee', 'DebateBillTitle', 'DebateBill', 'ReportOnBillProgress', 'ThirdReadingDone', 'Approved', 'Rejected', 'SubmittedToAttorneyGeneral', 'SignedIntoLaw', 'Withdrawn', 'presented']:
        workflow.states.addState(s)

    for t in ['withdraw', 'recommit', 'submit', 'third_reading', 'second_reading', 'request_report', 'first_reading', 'reject', 'commit', 'sign', 'approve', 'reintroduce']:
        workflow.transitions.addTransition(t)

    for v in ['review_history', 'comments', 'time', 'actor', 'action']:
        workflow.variables.addVariable(v)


    for l in []:
        if not l in workflow.worklists.objectValues():
            workflow.worklists.addWorklist(l)

    ## Initial State

    workflow.states.setInitialState('presented')

    ## States initialization

    stateDef = workflow.states['PresentedToParliament']
    stateDef.setProperties(title="""PresentedToParliament""",
                           description="""""",
                           transitions=['commit'])

    stateDef = workflow.states['CommittedToCommittee']
    stateDef.setProperties(title="""CommittedToCommittee""",
                           description="""""",
                           transitions=['second_reading', 'withdraw'])

    stateDef = workflow.states['DebateBillTitle']
    stateDef.setProperties(title="""DebateBillTitle""",
                           description="""""",
                           transitions=['commit', 'commit', 'reject', 'withdraw'])

    stateDef = workflow.states['DebateBill']
    stateDef.setProperties(title="""DebateBill""",
                           description="""""",
                           transitions=['request_report', 'withdraw'])

    stateDef = workflow.states['ReportOnBillProgress']
    stateDef.setProperties(title="""ReportOnBillProgress""",
                           description="""""",
                           transitions=['recommit', 'third_reading', 'withdraw'])

    stateDef = workflow.states['ThirdReadingDone']
    stateDef.setProperties(title="""ThirdReadingDone""",
                           description="""""",
                           transitions=['approve', 'reject', 'withdraw'])

    stateDef = workflow.states['Approved']
    stateDef.setProperties(title="""Approved""",
                           description="""""",
                           transitions=['submit'])

    stateDef = workflow.states['Rejected']
    stateDef.setProperties(title="""Rejected""",
                           description="""""",
                           transitions=['reintroduce'])

    stateDef = workflow.states['SubmittedToAttorneyGeneral']
    stateDef.setProperties(title="""SubmittedToAttorneyGeneral""",
                           description="""""",
                           transitions=['sign'])

    stateDef = workflow.states['SignedIntoLaw']
    stateDef.setProperties(title="""SignedIntoLaw""",
                           description="""""",
                           transitions=[])

    stateDef = workflow.states['Withdrawn']
    stateDef.setProperties(title="""Withdrawn""",
                           description="""""",
                           transitions=[])

    stateDef = workflow.states['presented']
    stateDef.setProperties(title="""presented""",
                           description="""""",
                           transitions=['first_reading'])

    ## Transitions initialization

    transitionDef = workflow.transitions['withdraw']
    transitionDef.setProperties(title="""withdraw""",
                                new_state_id="""Withdrawn""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""withdraw""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={},
                                )

    transitionDef = workflow.transitions['recommit']
    transitionDef.setProperties(title="""recommit""",
                                new_state_id="""DebateBill""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""recommit""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={},
                                )

    transitionDef = workflow.transitions['submit']
    transitionDef.setProperties(title="""submit""",
                                new_state_id="""SubmittedToAttorneyGeneral""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""submit""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={},
                                )

    transitionDef = workflow.transitions['third_reading']
    transitionDef.setProperties(title="""third_reading""",
                                new_state_id="""ThirdReadingDone""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""third_reading""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={},
                                )

    transitionDef = workflow.transitions['second_reading']
    transitionDef.setProperties(title="""second_reading""",
                                new_state_id="""DebateBillTitle""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""second_reading""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={},
                                )

    transitionDef = workflow.transitions['request_report']
    transitionDef.setProperties(title="""request_report""",
                                new_state_id="""ReportOnBillProgress""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""request_report""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={},
                                )

    transitionDef = workflow.transitions['first_reading']
    transitionDef.setProperties(title="""first_reading""",
                                new_state_id="""PresentedToParliament""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""first_reading""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={},
                                )

    transitionDef = workflow.transitions['reject']
    transitionDef.setProperties(title="""reject""",
                                new_state_id="""Rejected""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""reject""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={},
                                )

    transitionDef = workflow.transitions['commit']
    transitionDef.setProperties(title="""commit""",
                                new_state_id="""CommittedToCommittee""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""commit""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={},
                                )

    ## Creation of workflow scripts
    for wf_scriptname in ['publishChildren']:
        if not wf_scriptname in workflow.scripts.objectIds():
            workflow.scripts._setObject(wf_scriptname,
                ExternalMethod(wf_scriptname, wf_scriptname,
                productname + '.WestminsterBillWorkflow_scripts',
                wf_scriptname))

    transitionDef = workflow.transitions['sign']
    transitionDef.setProperties(title="""sign""",
                                new_state_id="""SignedIntoLaw""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""publishChildren""",
                                actbox_name="""sign""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={},
                                )

    ## Creation of workflow scripts
    for wf_scriptname in ['approveChildren']:
        if not wf_scriptname in workflow.scripts.objectIds():
            workflow.scripts._setObject(wf_scriptname,
                ExternalMethod(wf_scriptname, wf_scriptname,
                productname + '.WestminsterBillWorkflow_scripts',
                wf_scriptname))

    transitionDef = workflow.transitions['approve']
    transitionDef.setProperties(title="""approve""",
                                new_state_id="""Approved""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""approveChildren""",
                                actbox_name="""approve""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={},
                                )

    transitionDef = workflow.transitions['reintroduce']
    transitionDef.setProperties(title="""reintroduce""",
                                new_state_id="""presented""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""reintroduce""",
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



def createWestminsterBillWorkflow(self, id):
    """Create the workflow for Bungeni.
    """

    ob = DCWorkflowDefinition(id)
    setupWestminsterBillWorkflow(self, ob)
    return ob

addWorkflowFactory(createWestminsterBillWorkflow,
                   id='WestminsterBillWorkflow',
                   title='WestminsterBillWorkflow')

##code-section create-workflow-module-footer #fill in your manual code here
##/code-section create-workflow-module-footer

