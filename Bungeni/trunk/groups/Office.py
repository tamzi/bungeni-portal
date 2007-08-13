# -*- coding: utf-8 -*-
#
# File: Office.py
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
from Products.Bungeni.groups.BungeniTeam import BungeniTeam
from Products.Relations.field import RelationField
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    ComputedField(
        name='ChiefClerk',
        widget=ComputedField._properties['widget'](
            label='Chiefclerk',
            label_msgid='Bungeni_label_ChiefClerk',
            i18n_domain='Bungeni',
        )
    ),

    ComputedField(
        name='DeputyClerk',
        widget=ComputedField._properties['widget'](
            label='Deputyclerk',
            label_msgid='Bungeni_label_DeputyClerk',
            i18n_domain='Bungeni',
        )
    ),

    ComputedField(
        name='ChiefEditor',
        widget=ComputedField._properties['widget'](
            label='Chiefeditor',
            label_msgid='Bungeni_label_ChiefEditor',
            i18n_domain='Bungeni',
        )
    ),

    ComputedField(
        name='DeputyChiefEditor',
        widget=ComputedField._properties['widget'](
            label='Deputychiefeditor',
            label_msgid='Bungeni_label_DeputyChiefEditor',
            i18n_domain='Bungeni',
        )
    ),

    ComputedField(
        name='Editor',
        widget=ComputedField._properties['widget'](
            label='Editor',
            label_msgid='Bungeni_label_Editor',
            i18n_domain='Bungeni',
        )
    ),

    ComputedField(
        name='Reporter',
        widget=ComputedField._properties['widget'](
            label='Reporter',
            label_msgid='Bungeni_label_Reporter',
            i18n_domain='Bungeni',
        )
    ),

    RelationField(
        name='staffs',
        widget=ReferenceWidget(
            label='Staffs',
            label_msgid='Bungeni_label_staffs',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='clerk'
    ),

    RelationField(
        name='staffs',
        widget=ReferenceWidget(
            label='Staffs',
            label_msgid='Bungeni_label_staffs',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='deputy_clerk'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Office_schema = BaseSchema.copy() + \
    getattr(BungeniTeam, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Office(BungeniTeam):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BungeniTeam,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Office'

    meta_type = 'Office'
    portal_type = 'Office'
    allowed_content_types = [] + list(getattr(BungeniTeam, 'allowed_content_types', []))
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'Office.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Office"
    typeDescMsgId = 'description_edit_office'

    _at_rename_after_creation = True

    schema = Office_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getChiefClerk')
    def getChiefClerk(self):
        # TODO query for allowedRolesAndUsers
        pass

registerType(Office, PROJECTNAME)
# end of class Office

##code-section module-footer #fill in your manual code here
##/code-section module-footer



