# -*- coding: utf-8 -*-
#
# File: HelpFolder.py
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

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope import interface
from Products.ATContentTypes.content.folder import ATFolder
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

class HelpFolder(BaseFolder, ATFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseFolder,'__implements__',()),) + (getattr(ATFolder,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'HelpFolder'

    meta_type = 'HelpFolder'
    portal_type = 'HelpFolder'
    allowed_content_types = ['HelpCenterFAQFolder', 'HelpCenterGlossary', 'Document'] + list(getattr(ATFolder, 'allowed_content_types', []))
    filter_content_types = 1
    global_allow = 1
    #content_icon = 'HelpFolder.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "HelpFolder"
    typeDescMsgId = 'description_edit_helpfolder'

    _at_rename_after_creation = True

    schema = HelpFolder_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(HelpFolder, PROJECTNAME)
# end of class HelpFolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



