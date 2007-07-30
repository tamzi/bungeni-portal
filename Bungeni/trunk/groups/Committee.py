# -*- coding: utf-8 -*-
#
# File: Committee.py
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
            label='Maxmembers',
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
        name='memberofparliaments',
        widget=ReferenceWidget(
            label='Memberofparliaments',
            label_msgid='Bungeni_label_memberofparliaments',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='chairperson'
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
        name='memberofparliaments',
        widget=ReferenceWidget(
            label='Memberofparliaments',
            label_msgid='Bungeni_label_memberofparliaments',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='secretary'
    ),

    RelationField(
        name='memberofparliaments',
        widget=ReferenceWidget(
            label='Memberofparliaments',
            label_msgid='Bungeni_label_memberofparliaments',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='deputy_chairperson'
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

Committee_schema = BaseSchema.copy() + \
    getattr(BungeniTeam, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Committee(BungeniTeam):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BungeniTeam,'__implements__',()),)
    # zope3 interfaces
    interface.implements(IAuditable)

    # This name appears in the 'add' box
    archetype_name = 'Committee'

    meta_type = 'Committee'
    portal_type = 'Committee'
    allowed_content_types = [] + list(getattr(BungeniTeam, 'allowed_content_types', []))
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'Committee.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Committee"
    typeDescMsgId = 'description_edit_committee'

    _at_rename_after_creation = True

    schema = Committee_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(Committee, PROJECTNAME)
# end of class Committee

##code-section module-footer #fill in your manual code here
##/code-section module-footer



