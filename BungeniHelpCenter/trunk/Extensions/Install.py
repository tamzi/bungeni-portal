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
from Products.BungeniHelpCenter.config import PROJECTNAME
from Products.BungeniHelpCenter.config import product_globals as GLOBALS

def install(self, reinstall=False):
    """ External Method to install BungeniHelpCenter """
    out = StringIO()
    print >> out, "Installation log of %s:" % PROJECTNAME

    # If the config contains a list of dependencies, try to install them
    from Products.BungeniHelpCenter.config import DEPENDENCIES
    portal = getToolByName(self,'portal_url').getPortalObject()
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

    print >>out,'Uninstalled'

    return out.getvalue()

