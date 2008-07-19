# -*- coding: utf-8 -*-
#
# File: AgendaItem.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 2.0-beta5
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Jean Jordaan <jean.jordaan@gmail.com>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.Bungeni.events.ParliamentaryEvent import ParliamentaryEvent
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

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

class AgendaItem(BrowserDefaultMixin, BaseContent, ParliamentaryEvent):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IAgendaItem)

    meta_type = 'AgendaItem'
    _at_rename_after_creation = True

    schema = AgendaItem_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(AgendaItem, PROJECTNAME)
# end of class AgendaItem

##code-section module-footer #fill in your manual code here
##/code-section module-footer



