# Bungeni Parliamentary Information System - http://www.bungeni.org/
# Copyright (C) 2010 - Africa i-Parliaments - http://www.parliaments.info/
# Licensed under GNU GPL v2 - http://www.gnu.org/licenses/gpl-2.0.txt

"""Misc utilities for the UI

recommended usage:
from bungeni.ui.utils import misc

$Id$
"""

from bungeni.ui.i18n import _
from types import StringTypes, ListType

from ore.workflow import interfaces

import os


# file system 

def pathjoin(basefilepath, filepath):
    return os.path.join(os.path.dirname(basefilepath), filepath)


# workflow 

def get_wf_state(context):
    # return human readable workflow title
    wf = interfaces.IWorkflow(context)
    wf_state = interfaces.IWorkflowState(context).getState()
    return wf.workflow.states[wf_state].title

    
# request 

def is_ajax_request(request):
    return request.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


# list

def makeList(itemIds):
    if type(itemIds) == ListType:
        return itemIds            
    elif type(itemIds) in StringTypes:
        # only one item in this list
        return [itemIds,]
    else:
         raise TypeError( _("Form values must be of type string or list"))


