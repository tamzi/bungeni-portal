# Bungeni Parliamentary Information System - http://www.bungeni.org/
# Copyright (C) 2010 - Africa i-Parliaments - http://www.parliaments.info/
# Licensed under GNU GPL v2 - http://www.gnu.org/licenses/gpl-2.0.txt

"""Misc utilities for the UI

recommended usage:
from bungeni.ui.utils import common

$Id$
"""
log = __import__("logging").getLogger("bungeni.ui.utils.common")
#log.setLevel(10) # debug

import zope


from ore.wsgiapp.interfaces import IApplication
def get_application():
    return zope.component.getUtility(IApplication)


from zope.app.appsetup.appsetup import getConfigContext
def has_feature(feature_name):
    """Whether the application had been setup with the feature or not.
    
    (feature_name:str) -> bool
    Example of a feature_name: devmode:bool
    """
    # via zope.configuration.config.ConfigurationMachine.hasFeature(name)
    return getConfigContext().hasFeature(feature_name)

