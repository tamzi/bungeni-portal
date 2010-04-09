# Bungeni Parliamentary Information System - http://www.bungeni.org/
# Copyright (C) 2010 - Africa i-Parliaments - http://www.parliaments.info/
# Licensed under GNU GPL v2 - http://www.gnu.org/licenses/gpl-2.0.txt

"""Debug utilities

recommended usage:
from bungeni.ui.utils import debug

$Id$
"""
log = __import__("logging").getLogger("bungeni.ui.utils.debug")
log.setLevel(10) # debug

from zope import interface

def interfaces(obj):
    """Dump out list of interfaces for an object..."""
    return "\n".join(["",
        interfaces_implementedBy_class_for(obj),
        interfaces_providedBy(obj),
        interfaces_directlyProvidedBy(obj),
    ])
def interfaces_implementedBy_class_for(obj):
    """Dump out list of interfaces implementedBy an object's class."""
    return """  interfaces implementedBy %s:
    %s""" % (obj.__class__, 
          "\n    ".join(
          [ str(i) for i in interface.implementedBy(obj.__class__)]
          or [ "</>" ] ))
def interfaces_providedBy(obj):
    """Dump out list of interfaces providedBy an object."""
    return """  interfaces providedBy %s:
    %s""" % (obj, 
          "\n    ".join([ str(i) for i in interface.providedBy(obj)]
          or [ "</>" ] ))
def interfaces_directlyProvidedBy(obj):
    """Dump out list of interfaces directlyProvidedBy an object."""
    return """  interfaces directlyProvidedBy %s:
    %s""" % (obj, 
          "\n    ".join([ str(i) for i in interface.directlyProvidedBy(obj)]
          or [ "</>" ] ))


def location_stack(obj):
    """Dump out __parent__ stack for an object."""
    ps = []
    def _ps(ob):
        if ob is not None:
            _ps(ob.__parent__)
            ps.append(str(ob))
    _ps(obj)
    return """  parent stack for %s:
    %s""" % (obj, "\n    ".join(ps))

