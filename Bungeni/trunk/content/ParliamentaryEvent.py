# -*- coding: utf-8 -*-
#
# File: ParliamentaryEvent.py
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
from Products.ATContentTypes.content.event import ATEvent
from Products.AuditTrail.interfaces.IAuditable import IAuditable
from Products.Relations.field import RelationField
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

copied_fields = {}
copied_fields['tabledDate'] = ATEvent.schema['startDate'].copy(name='tabledDate')
copied_fields['tabledDate'].mutator = "setTabledDate"
copied_fields['tabledDate'].accessor = "getTabledDate"
copied_fields['tabledDate'].read_permission = "Bungeni: Schedule parliamentary business"
copied_fields['tabledDate'].write_permission = "Bungeni: Schedule parliamentary business"
copied_fields['tabledDate'].edit_accessor = "getRawTabledDate"
copied_fields['tabledDate'].widget.label = "Scheduled date"
copied_fields['startDate'] = ATEvent.schema['startDate'].copy()
copied_fields['startDate'].widget.label = "Scheduled date"
copied_fields['endDate'] = ATEvent.schema['endDate'].copy()
copied_fields['endDate'].widget.visible = False
copied_fields['location'] = ATEvent.schema['location'].copy()
copied_fields['location'].widget.visible = False
copied_fields['attendees'] = ATEvent.schema['attendees'].copy()
copied_fields['attendees'].widget.visible = False
copied_fields['eventUrl'] = ATEvent.schema['eventUrl'].copy()
copied_fields['eventUrl'].widget.visible = False
copied_fields['contactName'] = ATEvent.schema['contactName'].copy()
copied_fields['contactName'].widget.visible = False
copied_fields['contactEmail'] = ATEvent.schema['contactEmail'].copy()
copied_fields['contactEmail'].widget.visible = False
copied_fields['contactPhone'] = ATEvent.schema['contactPhone'].copy()
copied_fields['contactPhone'].widget.visible = False
schema = Schema((

    copied_fields['tabledDate'],

    copied_fields['startDate'],

    copied_fields['endDate'],

    copied_fields['location'],

    copied_fields['attendees'],

    ComputedField(
        name='eventType',
        widget=ComputedField._properties['widget'](
            visible=False,
            label='Eventtype',
            label_msgid='Bungeni_label_eventType',
            i18n_domain='Bungeni',
        ),
        label="Event Type"
    ),

    copied_fields['eventUrl'],

    copied_fields['contactName'],

    copied_fields['contactEmail'],

    copied_fields['contactPhone'],

    RelationField(
        name='otherSignatories',
        widget=ReferenceWidget(
            label="Other signatories",
            label_msgid='Bungeni_label_otherSignatories',
            i18n_domain='Bungeni',
        ),
        multiValued=1,
        relationship='ParliamentaryEvent_MemberOfParliament'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

ParliamentaryEvent_schema = getattr(ATEvent, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class ParliamentaryEvent(BaseContent, ATEvent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),) + (getattr(ATEvent,'__implements__',()),)
    # zope3 interfaces
    interface.implements(IAuditable)

    allowed_content_types = [] + list(getattr(ATEvent, 'allowed_content_types', []))
    _at_rename_after_creation = True

    schema = ParliamentaryEvent_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('start')
    def start(self):
        """
        """
        pass

    security.declarePublic('end')
    def end(self):
        """ Alias for tabledDate, to satisfy calendar interface
        """
        return self.start()+1

    security.declarePublic('getEventType')
    def getEventType(self):
        """
        """
        # XXX is there a better way to get the name of a type??
        return self.portal_type

    security.declarePublic('setEventType')
    def setEventType(self, value, alreadySet=False, **kw):
        """ Override ATEvent.setEventType: don't try and set me, I'm
        computed now.
        """
        value = self.getEventType()
        self.setSubject(value, alreadySet=True, **kw)

# end of class ParliamentaryEvent

##code-section module-footer #fill in your manual code here
##/code-section module-footer



