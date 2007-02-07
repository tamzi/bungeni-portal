# -*- coding: utf-8 -*-
#
# File: BungeniMember.py
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

__author__ = """Jean Jordaan <jean.jordaan@gmail.com>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
import zope
from Products.Bungeni.interfaces.IBungeniMember import IBungeniMember
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

BungeniMember_schema = schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class BungeniMember(BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)
    # zope3 interfaces
    zope.interface.implements(IBungeniMember)

    allowed_content_types = []
    _at_rename_after_creation = True

    schema = BungeniMember_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('isAuto')
    def isAuto(self):
        """ Are we in an auto-approved workflow?
        """
        # XXX: This is pretty hacky (peering at the workflow name), but
        # we need some way of knowing whether our workflow is auto or
        # approval.
        wft = getToolByName(self, 'portal_workflow')
        workflow_names = wft.getChainForPortalType(self.portal_type)
        auto = False
        for workflow_name in workflow_names:
            auto = 'auto' in workflow_name.lower()
            if auto: break
        return auto

# end of class BungeniMember

##code-section module-footer #fill in your manual code here
##/code-section module-footer



