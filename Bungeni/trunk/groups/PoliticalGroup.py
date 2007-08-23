# -*- coding: utf-8 -*-
#
# File: PoliticalGroup.py
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
from Products.AuditTrail.interfaces.IAuditable import IAuditable
from Products.Relations.field import RelationField
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
from Products.TeamSpace.permissions import *
##/code-section module-header

schema = Schema((

    StringField(
        name='shortTitle',
        widget=StringWidget(
            label='Shorttitle',
            label_msgid='Bungeni_label_shortTitle',
            i18n_domain='Bungeni',
        )
    ),

    DateTimeField(
        name='registrationDate',
        widget=CalendarWidget(
            label='Registrationdate',
            label_msgid='Bungeni_label_registrationDate',
            i18n_domain='Bungeni',
        )
    ),

    DateTimeField(
        name='cessationDate',
        widget=CalendarWidget(
            label='Cessationdate',
            label_msgid='Bungeni_label_cessationDate',
            i18n_domain='Bungeni',
        )
    ),

    RelationField(
        name='Leader',
        vocabulary='getMembershipVocab',
        widget=ReferenceWidget(
            label='Leader',
            label_msgid='Bungeni_label_Leader',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='politicalgroup_leader'
    ),

    RelationField(
        name='DeputyLeader',
        vocabulary='getMembershipVocab',
        widget=ReferenceWidget(
            label='Deputyleader',
            label_msgid='Bungeni_label_DeputyLeader',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='politicalgroup_deputyleader'
    ),

    RelationField(
        name='Spokesperson',
        vocabulary='getMembershipVocab',
        widget=ReferenceWidget(
            label='Spokesperson',
            label_msgid='Bungeni_label_Spokesperson',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='politicalgroup_spokesperson'
    ),

    RelationField(
        name='Secretary',
        vocabulary='getMembershipVocab',
        widget=ReferenceWidget(
            label='Secretary',
            label_msgid='Bungeni_label_Secretary',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='politicalgroup_secretary'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

PoliticalGroup_schema = BaseSchema.copy() + \
    getattr(BungeniTeam, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class PoliticalGroup(BungeniTeam):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BungeniTeam,'__implements__',()),)
    # zope3 interfaces
    interface.implements(IAuditable)

    # This name appears in the 'add' box
    archetype_name = 'PoliticalGroup'

    meta_type = 'PoliticalGroup'
    portal_type = 'PoliticalGroup'
    allowed_content_types = [] + list(getattr(BungeniTeam, 'allowed_content_types', []))
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'PoliticalGroup.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "PoliticalGroup"
    typeDescMsgId = 'description_edit_politicalgroup'

    _at_rename_after_creation = True

    schema = PoliticalGroup_schema

    ##code-section class-header #fill in your manual code here
    actions = BungeniTeam.actions
    ##/code-section class-header

    # Methods

    security.declarePublic('setLeader')
    def setLeader(self,value,**kw):
        """
        """
        # Team:
        if value:
            member_roles = self._get_member_roles_from_UIDs(
                    value, ['Leader'])
            self.manage_updateRoles(member_roles)
        # Field:
        field = self.Schema()['Leader']
        return field.set(self, value, **kw)

    security.declarePublic('setDeputyLeader')
    def setDeputyLeader(self,value,**kw):
        """
        """
        # Team:
        if value:
            member_roles = self._get_member_roles_from_UIDs(
                    value, ['DeputyLeader'])
            self.manage_updateRoles(member_roles)
        # Field:
        field = self.Schema()['DeputyLeader']
        return field.set(self, value, **kw)

    security.declarePublic('setSpokesperson')
    def setSpokesperson(self,value,**kw):
        """
        """
        # Team:
        if value:
            member_roles = self._get_member_roles_from_UIDs(
                    value, ['Spokesperson'])
            self.manage_updateRoles(member_roles)
        # Field:
        field = self.Schema()['Spokesperson']
        return field.set(self, value, **kw)

    security.declarePublic('setSecretary')
    def setSecretary(self,value,**kw):
        """
        """
        # Team:
        if value:
            member_roles = self._get_member_roles_from_UIDs(
                    value, ['Secretary'])
            self.manage_updateRoles(member_roles)
        # Field:
        field = self.Schema()['Secretary']
        return field.set(self, value, **kw)

    security.declareProtected(ManageTeam, 'manage_updateRoles')
    def manage_updateRoles(self,member_roles,REQUEST):
        """ Constrain some roles
        """
        constrained_roles = {
                'Leader': 1,
                'DeputyLeader': 1,
                'Spokesperson': 1,
                'Secretary': 1,
                }
        self._constrainMembershipRoles(constrained_roles, member_roles)
        # Delegate to super
        BungeniTeam.manage_updateRoles(self,member_roles,REQUEST=None)


registerType(PoliticalGroup, PROJECTNAME)
# end of class PoliticalGroup

##code-section module-footer #fill in your manual code here
##/code-section module-footer



