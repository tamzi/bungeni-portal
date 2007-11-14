# -*- coding: utf-8 -*-
#
# File: ParliamentaryEvent.py
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
from Products.ATContentTypes.content.event import ATEvent
from Products.Bungeni.events.ParliamentaryDocument import ParliamentaryDocument
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

copied_fields = {}
copied_fields['startDate'] = ATEvent.schema['startDate'].copy()
copied_fields['startDate'].widget.visible = False
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

    copied_fields['startDate'],

    copied_fields['endDate'],

    copied_fields['location'],

    copied_fields['attendees'],

    ComputedField(
        name='eventType',
        widget=ComputedField._properties['widget'](
            label="Event Type",
            visible=False,
            label_msgid='Bungeni_label_eventType',
            i18n_domain='Bungeni',
        )
    ),

    copied_fields['eventUrl'],

    copied_fields['contactName'],

    copied_fields['contactEmail'],

    copied_fields['contactPhone'],

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

ParliamentaryEvent_schema = getattr(ATEvent, 'schema', Schema(())).copy() + \
    getattr(ParliamentaryDocument, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class ParliamentaryEvent(ATEvent, ParliamentaryDocument, BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IParliamentaryEvent)

    _at_rename_after_creation = True

    schema = ParliamentaryEvent_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getEventType')
    def getEventType(self):
        """
        """
        # XXX is there a better way to get the name of a type??
        return self.portal_type

    security.declarePublic('setEventType')
    def setEventType(self,value,alreadySet,**kw):
        """ Override ATEvent.setEventType: don't try and set me, I'm
        computed now.
        """
        # TODO This needs a sanity check
        value = self.getEventType()
        self.setSubject(value, alreadySet=True, **kw)

# end of class ParliamentaryEvent

##code-section module-footer #fill in your manual code here
##/code-section module-footer



