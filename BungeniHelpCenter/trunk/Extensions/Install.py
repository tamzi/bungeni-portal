# -*- coding: utf-8 -*-
#
# File: Install.py
import os.path
import sys
from StringIO import StringIO
from sets import Set
from App.Common import package_home
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import manage_addTool
from Products.ExternalMethod.ExternalMethod import ExternalMethod
from zExceptions import NotFound, BadRequest

from Products.Archetypes.Extensions.utils import installTypes
from Products.Archetypes.Extensions.utils import install_subskin
from Products.Archetypes.config import TOOL_NAME as ARCHETYPETOOLNAME
from Products.Archetypes.atapi import listTypes
from Products.BungeniHelpCenter.config import PROJECTNAME, \
    RESOURCES_CSS, RESOURCES_JS, TYPE_PARAMS
from Products.BungeniHelpCenter.config import product_globals as GLOBALS

def install(self, reinstall=False):
    """ External Method to install BungeniHelpCenter """
    out = StringIO()
    print >> out, "Installation log of %s:" % PROJECTNAME
    portal = getToolByName(self,'portal_url').getPortalObject()

    from Products.ResourceRegistries.config import CSSTOOLNAME, JSTOOLNAME

    expr = 'python:getattr(here, \'portal_type\', None) in [\'%s\',\'%s\']'%('BungeniReferenceManualPage', 'BungeniTutorialPage') 

    csstool = getToolByName(portal, CSSTOOLNAME)
    for (id, media) in RESOURCES_CSS.iteritems():
        csstool.manage_removeStylesheet(id=id)
        csstool.manage_addStylesheet(id=id, media=media,\
                                     rel='stylesheet', enabled=True, cookable=True, expression=expr)
        print >> out, 'Registered CSS resource:', id

    jstool = getToolByName(portal, JSTOOLNAME)
    for id in RESOURCES_JS:
        jstool.manage_removeScript(id=id)
        jstool.manage_addScript(id=id,
                                enabled=True, cookable=True, compression='none', expression=expr)
        print >> out, 'Registered JS resource:', id

    # If the config contains a list of dependencies, try to install them
    from Products.BungeniHelpCenter.config import DEPENDENCIES
    quickinstaller = portal.portal_quickinstaller
    for dependency in DEPENDENCIES:
        print >> out, "Installing dependency %s:" % dependency
        quickinstaller.installProduct(dependency)
        import transaction
        transaction.savepoint(optimistic=True)

    types = getToolByName(self,'portal_types')
    tutorial_folder = types['HelpCenterTutorialFolder']
    tutorial_folder.allowed_content_types = ('BungeniHelpCenterTutorial',)

    tutorial_folder = types['HelpCenterReferenceManualFolder']
    tutorial_folder.allowed_content_types = ('BungeniHelpCenterReferenceManual',)

    classes = listTypes(PROJECTNAME)
    installTypes(self, out,
                 classes,
                 PROJECTNAME)
    install_subskin(self, out, GLOBALS)

    # autoinstall tools
    portal = getToolByName(self,'portal_url').getPortalObject()

    print >>out, 'Installed'
    return out.getvalue()

def uninstall(self, reinstall=False):
    out = StringIO()
    from Products.ResourceRegistries.config import CSSTOOLNAME, JSTOOLNAME
    
    csstool = getToolByName(portal, CSSTOOLNAME)
    for id in RESOURCES_CSS.iterkeys():
        csstool.manage_removeStylesheet(id=id)
        print >> out, 'Unregistered CSS resource:', id

    jstool = getToolByName(portal, JSTOOLNAME)
    for id in RESOURCES_JS:
        jstool.manage_removeScript(id=id)
        print >> out, 'Unregistered JS resource:', id

    print >>out,'Uninstalled'

    return out.getvalue()

