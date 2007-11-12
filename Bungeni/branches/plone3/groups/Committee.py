# -*- coding: utf-8 -*-
#
# File: Committee.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 2.0-beta4
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
from zope.interface import implements
import interfaces
from Products.Bungeni.groups.BungeniTeam import BungeniTeam
from Products.AuditTrail.interfaces.IAuditable import IAuditable
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Relations.field import RelationField
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='type',
        widget=SelectionWidget(
            label='Type',
            label_msgid='Bungeni_label_type',
            i18n_domain='Bungeni',
        ),
        vocabulary=['Permanent', 'Temporary']
    ),

    StringField(
        name='category',
        widget=SelectionWidget(
            label='Category',
            label_msgid='Bungeni_label_category',
            i18n_domain='Bungeni',
        ),
        vocabulary=['housekeeping', 'ad hoc', 'departmental', 'watchdog']
    ),

    TextField(
        name='functions',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label='Functions',
            label_msgid='Bungeni_label_functions',
            i18n_domain='Bungeni',
        ),
        default_output_type='text/html'
    ),

    IntegerField(
        name='maxMembers',
        widget=IntegerField._properties['widget'](
            label="Maximum number of members",
            label_msgid='Bungeni_label_maxMembers',
            i18n_domain='Bungeni',
        )
    ),

    BooleanField(
        name='proportionalRepresentation',
        widget=BooleanField._properties['widget'](
            label='Proportionalrepresentation',
            label_msgid='Bungeni_label_proportionalRepresentation',
            i18n_domain='Bungeni',
        )
    ),

    BooleanField(
        name='substitutionAllowed',
        widget=BooleanField._properties['widget'](
            label='Substitutionallowed',
            label_msgid='Bungeni_label_substitutionAllowed',
            i18n_domain='Bungeni',
        )
    ),

    StringField(
        name='presidencyInternal',
        widget=StringWidget(
            label='Presidencyinternal',
            label_msgid='Bungeni_label_presidencyInternal',
            i18n_domain='Bungeni',
        )
    ),

    IntegerField(
        name='maxChairs',
        widget=IntegerField._properties['widget'](
            label='Maxchairs',
            label_msgid='Bungeni_label_maxChairs',
            i18n_domain='Bungeni',
        )
    ),

    IntegerField(
        name='maxSecretaries',
        widget=IntegerField._properties['widget'](
            label='Maxsecretaries',
            label_msgid='Bungeni_label_maxSecretaries',
            i18n_domain='Bungeni',
        )
    ),

    IntegerField(
        name='minAttendance',
        widget=IntegerField._properties['widget'](
            label='Minattendance',
            label_msgid='Bungeni_label_minAttendance',
            i18n_domain='Bungeni',
        )
    ),

    DateTimeField(
        name='dissolutionDate',
        widget=CalendarWidget(
            label='Dissolutiondate',
            label_msgid='Bungeni_label_dissolutionDate',
            i18n_domain='Bungeni',
        )
    ),

    StringField(
        name='duration',
        widget=SelectionWidget(
            label='Duration',
            label_msgid='Bungeni_label_duration',
            i18n_domain='Bungeni',
        ),
        vocabulary=['parliament', 'annual']
    ),

    RelationField(
        name='DeputyChairperson',
        vocabulary='getMembershipVocab',
        widget=ReferenceWidget(
            label='Deputychairperson',
            label_msgid='Bungeni_label_DeputyChairperson',
            i18n_domain='Bungeni',
        ),
        allowed_types=['MemberOfParliament', 'Staff'],
        multiValued=1,
        relationship='committee_deputychairperson'
    ),

    RelationField(
        name='Secretary',
        vocabulary='getMembershipVocab',
        widget=ReferenceWidget(
            label='Secretary',
            label_msgid='Bungeni_label_Secretary',
            i18n_domain='Bungeni',
        ),
        allowed_types=['MemberOfParliament', 'Staff'],
        multiValued=1,
        relationship='committee_secretary'
    ),

    RelationField(
        name='Chairperson',
        vocabulary='getMembershipVocab',
        widget=ReferenceWidget(
            label='Chairperson',
            label_msgid='Bungeni_label_Chairperson',
            i18n_domain='Bungeni',
        ),
        allowed_types=['MemberOfParliament', 'Staff'],
        multiValued=1,
        relationship='committee_chairperson'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Committee_schema = BaseSchema.copy() + \
    getattr(BungeniTeam, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Committee(BungeniTeam, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ICommittee, IAuditable)

    meta_type = 'Committee'
    _at_rename_after_creation = True

    schema = Committee_schema

    ##code-section class-header #fill in your manual code here
    actions = BungeniTeam.actions
    ##/code-section class-header

    # Methods

    security.declarePublic('setChairperson')
    def setChairperson(self, value, **kw_args):
        """
        """
        # Team:
        if value:
            member_roles = self._get_member_roles_from_UIDs(
                    value, ['Chairperson'])
            self.manage_updateRoles(member_roles)
        # Field:
        field = self.schema['Chairperson']
        return field.set(self, value, **kw_args)

    security.declarePublic('setSecretary')
    def setSecretary(self, value, **kw_args):
        """
        """
        # Team:
        if value:
            member_roles = self._get_member_roles_from_UIDs(
                    value, ['Secretary'])
            self.manage_updateRoles(member_roles)
        # Field:
        field = self.schema['Secretary']
        return field.set(self, value, **kw_args)

    security.declarePublic('setDeputyChairperson')
    def setDeputyChairperson(self, value, **kw_args):
        """
        """
        # Team:
        if value:
            member_roles = self._get_member_roles_from_UIDs(
                    value, ['DeputyChairperson'])
            self.manage_updateRoles(member_roles)
        # Field:
        field = self.schema['DeputyChairperson']
        return field.set(self, value, **kw_args)

    security.declarePublic('manage_updateRoles')
    def manage_updateRoles(self,member_roles,REQUEST=None):
        """
        """
        constrained_roles = {
                'Chairperson': self.getMaxChairs(),
                'DeputyChairperson': 1, # TODO: verify
                'Secretary': self.getMaxSecretaries(),
                }
        self._constrainMembershipRoles(constrained_roles, member_roles)
        # Delegate to super
        return BungeniTeam.manage_updateRoles(self,member_roles,REQUEST=None)


registerType(Committee, PROJECTNAME)
# end of class Committee

##code-section module-footer #fill in your manual code here
##/code-section module-footer



