# -*- coding: utf-8 -*-
#
# File: AgendaItem.py
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
from Products.Bungeni.events.ParliamentaryEvent import ParliamentaryEvent
from Products.Relations.field import RelationField
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

copied_fields = {}
copied_fields['tabledDate'] = ParliamentaryEvent.schema['startDate'].copy(name='tabledDate')
copied_fields['tabledDate'].read_permission = "Bungeni: Schedule parliamentary business"
copied_fields['tabledDate'].mutator = "setTabledDate"
copied_fields['tabledDate'].accessor = "getTabledDate"
copied_fields['tabledDate'].write_permission = "Bungeni: Schedule parliamentary business"
copied_fields['tabledDate'].edit_accessor = "getRawTabledDate"
copied_fields['tabledDate'].widget.label = "Tabled date"
copied_fields['scheduledDate'] = ParliamentaryEvent.schema['startDate'].copy(name='scheduledDate')
copied_fields['scheduledDate'].read_permission = "Bungeni: Schedule parliamentary business"
copied_fields['scheduledDate'].mutator = "setScheduledDate"
copied_fields['scheduledDate'].accessor = "getScheduledDate"
copied_fields['scheduledDate'].write_permission = "Bungeni: Schedule parliamentary business"
copied_fields['scheduledDate'].edit_accessor = "getRawScheduledDate"
copied_fields['scheduledDate'].widget.label = "Scheduled date"
schema = Schema((

    copied_fields['tabledDate'],

    copied_fields['scheduledDate'],

    RelationField(
        name='questions',
        widget=ReferenceWidget(
            label='Questions',
            label_msgid='Bungeni_label_questions',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='agendaitem_question'
    ),

    RelationField(
        name='motions',
        widget=ReferenceWidget(
            label='Motions',
            label_msgid='Bungeni_label_motions',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='agendaitem_motion'
    ),

    RelationField(
        name='bills',
        widget=ReferenceWidget(
            label='Bills',
            label_msgid='Bungeni_label_bills',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='agendaitem_bill'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

AgendaItem_schema = BaseSchema.copy() + \
    getattr(ParliamentaryEvent, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class AgendaItem(BaseContent, ParliamentaryEvent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),) + (getattr(ParliamentaryEvent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'AgendaItem'

    meta_type = 'AgendaItem'
    portal_type = 'AgendaItem'
    allowed_content_types = [] + list(getattr(ParliamentaryEvent, 'allowed_content_types', []))
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'AgendaItem.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "AgendaItem"
    typeDescMsgId = 'description_edit_agendaitem'

    _at_rename_after_creation = True

    schema = AgendaItem_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(AgendaItem, PROJECTNAME)
# end of class AgendaItem

##code-section module-footer #fill in your manual code here
##/code-section module-footer



