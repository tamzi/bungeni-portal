# -*- coding: utf-8 -*-
#
# File: MemberOfParliament.py
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
from Products.AuditTrail.interfaces.IAuditable import IAuditable
from Products.Bungeni.interfaces.IMemberOfParliament import IMemberOfParliament
from Products.Relations.field import RelationField
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

    RelationField(
        name='constituencys',
        widget=ReferenceWidget(
            label='Constituencys',
            label_msgid='Bungeni_label_constituencys',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='memberofparliament_constituency'
    ),

    RelationField(
        name='portfolios',
        widget=ReferenceWidget(
            label='Portfolios',
            label_msgid='Bungeni_label_portfolios',
            i18n_domain='Bungeni',
        ),
        multiValued=1,
        relationship='notminister_portfolio'
    ),

    RelationField(
        name='portfolios',
        widget=ReferenceWidget(
            label='Portfolios',
            label_msgid='Bungeni_label_portfolios',
            i18n_domain='Bungeni',
        ),
        multiValued=1,
        relationship='notassistantminister_portfolio'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

MemberOfParliament_schema = BaseSchema.copy() + \
    getattr(BungeniMember, 'schema', Schema(())).copy() + \
    BaseMember.schema.copy() + \
    ExtensibleMetadata.schema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
# Just to fix the order of the fields.
MemberOfParliament_schema = MemberOfParliament_schema + BungeniMember.schema.copy()
##/code-section after-schema

class MemberOfParliament(BaseMember, BungeniMember, BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseMember,'__implements__',()),) + (getattr(BungeniMember,'__implements__',()),) + (getattr(BaseContent,'__implements__',()),)
    # zope3 interfaces
    interface.implements(IAuditable, IMemberOfParliament)

    # This name appears in the 'add' box
    archetype_name = 'MemberOfParliament'

    meta_type = 'MemberOfParliament'
    portal_type = 'MemberOfParliament'
    allowed_content_types = [] + list(getattr(BungeniMember, 'allowed_content_types', []))
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'MemberOfParliament.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "MemberOfParliament"
    typeDescMsgId = 'description_edit_memberofparliament'

    _at_rename_after_creation = True

    schema = MemberOfParliament_schema

    base_archetype = BaseContent

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # A member's __call__ should not render itself, this causes recursion
    def __call__(self, *args, **kwargs):
        return self.getId()
        

    # Methods


registerType(MemberOfParliament, PROJECTNAME)
# end of class MemberOfParliament

##code-section module-footer #fill in your manual code here
##/code-section module-footer



