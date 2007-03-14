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
from Products.TeamSpace.team import Team
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
        )
    ),

    StringField(
        name='category',
        widget=SelectionWidget(
            label='Category',
            label_msgid='Bungeni_label_category',
            i18n_domain='Bungeni',
        )
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

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Committee_schema = BaseSchema.copy() + \
    getattr(Team, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Committee(BaseContent, Team):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),) + (getattr(Team,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Committee'

    meta_type = 'Committee'
    portal_type = 'Committee'
    allowed_content_types = [] + list(getattr(Team, 'allowed_content_types', []))
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



