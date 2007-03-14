# -*- coding: utf-8 -*-
#
# File: Clerk.py
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
from Products.Bungeni.membership.BungeniMember import BungeniMember
from Products.Bungeni.interfaces.IClerk import IClerk
from Products.AuditTrail.interfaces.IAuditable import IAuditable
# imports needed by remember
from Products.remember.content.member import BaseMember
from Products.remember.permissions import \
        VIEW_PUBLIC_PERMISSION, EDIT_ID_PERMISSION, \
        EDIT_PROPERTIES_PERMISSION, VIEW_OTHER_PERMISSION,  \
        VIEW_SECURITY_PERMISSION, EDIT_PASSWORD_PERMISSION, \
        EDIT_SECURITY_PERMISSION, MAIL_PASSWORD_PERMISSION, \
        ADD_MEMBER_PERMISSION
from AccessControl import ModuleSecurityInfo
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Clerk_schema = BaseSchema.copy() + \
    getattr(BungeniMember, 'schema', Schema(())).copy() + \
    BaseMember.schema.copy() + \
    ExtensibleMetadata.schema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Clerk(BaseMember, BaseContent, BungeniMember):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseMember,'__implements__',()),) + (getattr(BaseContent,'__implements__',()),) + (getattr(BungeniMember,'__implements__',()),)
    # zope3 interfaces
    interface.implements(IClerk, IAuditable)

    # This name appears in the 'add' box
    archetype_name = 'Clerk'

    meta_type = 'Clerk'
    portal_type = 'Clerk'
    allowed_content_types = [] + list(getattr(BungeniMember, 'allowed_content_types', []))
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'Clerk.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Clerk"
    typeDescMsgId = 'description_edit_clerk'

    _at_rename_after_creation = True

    schema = Clerk_schema

    base_archetype = BaseContent

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # A member's __call__ should not render itself, this causes recursion
    def __call__(self, *args, **kwargs):
        return self.getId()
        

    # Methods


registerType(Clerk, PROJECTNAME)
# end of class Clerk

##code-section module-footer #fill in your manual code here
##/code-section module-footer



