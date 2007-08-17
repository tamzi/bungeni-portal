# -*- coding: utf-8 -*-
#
# File: DebateRecordOffice.py
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
from Products.Bungeni.groups.Office import Office
from Products.Relations.field import RelationField
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
from Products.TeamSpace.permissions import *
##/code-section module-header

schema = Schema((

    RelationField(
        name='ChiefEditor',
        widget=ReferenceWidget(
            label='Chiefeditor',
            label_msgid='Bungeni_label_ChiefEditor',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='debaterecordoffice_chiefeditor'
    ),

    RelationField(
        name='DeputyChiefEditor',
        widget=ReferenceWidget(
            label='Deputychiefeditor',
            label_msgid='Bungeni_label_DeputyChiefEditor',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='debaterecordoffice_deputychiefeditor'
    ),

    RelationField(
        name='Editors',
        widget=ReferenceWidget(
            label='Editors',
            label_msgid='Bungeni_label_Editors',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='debaterecordoffice_editors'
    ),

    RelationField(
        name='Reporters',
        widget=ReferenceWidget(
            label='Reporters',
            label_msgid='Bungeni_label_Reporters',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='debaterecordoffice_reporters'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

DebateRecordOffice_schema = BaseSchema.copy() + \
    getattr(Office, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class DebateRecordOffice(BaseContent, Office):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),) + (getattr(Office,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'DebateRecordOffice'

    meta_type = 'DebateRecordOffice'
    portal_type = 'DebateRecordOffice'
    allowed_content_types = [] + list(getattr(Office, 'allowed_content_types', []))
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'DebateRecordOffice.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "DebateRecordOffice"
    typeDescMsgId = 'description_edit_debaterecordoffice'

    _at_rename_after_creation = True

    schema = DebateRecordOffice_schema

    ##code-section class-header #fill in your manual code here
    actions = Office.actions
    ##/code-section class-header

    # Methods

    security.declarePublic('setChiefEditor')
    def setChiefEditor(self):
        """
        """
        pass

    security.declarePublic('setDeputyChiefEditor')
    def setDeputyChiefEditor(self):
        """
        """
        pass

    security.declarePublic('setEditors')
    def setEditors(self):
        """
        """
        pass

    security.declarePublic('setReporters')
    def setReporters(self):
        """
        """
        pass

    security.declareProtected(ManageTeam, 'manage_updateRoles')
    def manage_updateRoles(self,member_roles,REQUEST=None):
        """
        """
        constrained_roles = {
                'ChiefEditor': 1,
                'DeputyEditor': 1,
                }
        self._constrainMembershipRoles(constrained_roles, member_roles)
        # Delegate to super
        Office.manage_updateRoles(self,member_roles,REQUEST=None)


registerType(DebateRecordOffice, PROJECTNAME)
# end of class DebateRecordOffice

##code-section module-footer #fill in your manual code here
##/code-section module-footer



