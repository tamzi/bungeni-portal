# -*- coding: utf-8 -*-
#
# File: HelpFolder.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 2.0-beta5
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Jean Jordaan <jean.jordaan@gmail.com>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.ATContentTypes.content.folder import ATFolder
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
# TODO: Rationalize interface generation.
# The 'from zope import interface' above is because default interfaces
# are z3. However, below we have old-style __implements__ because we
# don't implement any new-style interfaces. Either do it z3-style
# throughout, or don't include z3 cruft if not needed.
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

HelpFolder_schema = BaseFolderSchema.copy() + \
    getattr(ATFolder, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class HelpFolder(BrowserDefaultMixin, BaseFolder, ATFolder):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IHelpFolder)

    meta_type = 'HelpFolder'
    _at_rename_after_creation = True

    schema = HelpFolder_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(HelpFolder, PROJECTNAME)
# end of class HelpFolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



