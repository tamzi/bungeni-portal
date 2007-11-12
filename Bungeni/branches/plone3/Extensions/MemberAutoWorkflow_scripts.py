# -*- coding: utf-8 -*-
#
# File: Bungeni.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 2.0-beta4
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


# Workflow Scripts for: MemberAutoWorkflow

##code-section workflow-script-header #fill in your manual code here
##/code-section workflow-script-header


def enable(self, state_change, **kw):
    # From remember/Extensions/workflow.py
    obj=state_change.object
    try:
        if hasattr(obj, 'old_state'):
            delattr(obj, 'old_state')
    except:
        # write tracebacks because otherwise workflow will swallow exceptions
        log_exc()
        raise



def register(self, state_change, **kw):
    # From remember/Extensions/workflow.py
    obj = state_change.object
    return obj.register()



def disable(self, state_change, **kw):
    # From remember/Extensions/workflow.py
    obj=state_change.object
    try:
        workflow_tool = getToolByName(obj, 'portal_workflow')
        obj.old_state = workflow_tool.getInfoFor(obj, 'review_state', '')
    except:
         # write tracebacks because otherwise workflow will swallow exceptions
        log_exc()
        raise


