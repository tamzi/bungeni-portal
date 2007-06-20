# -*- coding: utf-8 -*-
#
# File: BillSection.py
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
from Products.PloneHelpCenter.content.ReferenceManualSection import HelpCenterReferenceManualSection
from Products.AuditTrail.interfaces.IAuditable import IAuditable
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

BillSection_schema = BaseFolderSchema.copy() + \
    getattr(HelpCenterReferenceManualSection, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class BillSection(BaseFolder, HelpCenterReferenceManualSection):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseFolder,'__implements__',()),) + (getattr(HelpCenterReferenceManualSection,'__implements__',()),)
    # zope3 interfaces
    interface.implements(IAuditable)

    # This name appears in the 'add' box
    archetype_name = 'BillSection'

    meta_type = 'BillSection'
    portal_type = 'BillSection'
    allowed_content_types = ['BillPage', 'Amendment', 'BillSection']
    filter_content_types = 1
    global_allow = 0
    #content_icon = 'BillSection.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "A bill section can contain pages and subsections."
    typeDescMsgId = 'description_edit_billsection'

    _at_rename_after_creation = True

    schema = BillSection_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(BillSection, PROJECTNAME)
# end of class BillSection

##code-section module-footer #fill in your manual code here
##/code-section module-footer



