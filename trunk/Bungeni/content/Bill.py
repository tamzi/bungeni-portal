# -*- coding: utf-8 -*-
#
# File: Bill.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 1.5.1-svn
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

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.PloneHelpCenter.content.ReferenceManual import HelpCenterReferenceManual
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Bill_schema = BaseFolderSchema.copy() + \
    getattr(HelpCenterReferenceManual, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Bill(BaseFolder, HelpCenterReferenceManual):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseFolder,'__implements__',()),) + (getattr(HelpCenterReferenceManual,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Bill'

    meta_type = 'Bill'
    portal_type = 'Bill'
    allowed_content_types = ['BillSection', 'ATFile'] + list(getattr(HelpCenterReferenceManual, 'allowed_content_types', []))
    filter_content_types = 1
    global_allow = 0
    #content_icon = 'Bill.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Bill"
    typeDescMsgId = 'description_edit_bill'

    _at_rename_after_creation = True

    schema = Bill_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(Bill, PROJECTNAME)
# end of class Bill

##code-section module-footer #fill in your manual code here
##/code-section module-footer



