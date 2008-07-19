# -*- coding: utf-8 -*-
#
# File: Sitting.py
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

from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

copied_fields = {}
copied_fields['startDate'] = ParliamentaryEvent.schema['startDate'].copy()
copied_fields['startDate'].widget.visible = True
copied_fields['endDate'] = ParliamentaryEvent.schema['endDate'].copy()
copied_fields['endDate'].widget.visible = True
schema = Schema((

    StringField(
        name='attendees',
        widget=SelectionWidget(
            label='Attendees',
            label_msgid='Bungeni_label_attendees',
            i18n_domain='Bungeni',
        ),
        multiValued=True,
        vocabulary='getAttendeesVocab'
    ),

    StringField(
        name='sittingType',
        widget=SelectionWidget(
            label='Sittingtype',
            label_msgid='Bungeni_label_sittingType',
            i18n_domain='Bungeni',
        ),
        vocabulary=['morning', 'afternoon', 'extraordinary']
    ),

    copied_fields['startDate'],

    copied_fields['endDate'],

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Sitting_schema = BaseFolderSchema.copy() + \
    getattr(ParliamentaryEvent, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Sitting(BrowserDefaultMixin, BaseFolder, ParliamentaryEvent):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ISitting)

    meta_type = 'Sitting'
    _at_rename_after_creation = True

    schema = Sitting_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getAttendeesVocab')
    def getAttendeesVocab(self):
        """ Active members may be attendees of a sitting.
        """
        # TODO: this currently allows us to add active members to a
        # sitting. That means we can't add members to sittings of past
        # parliaments. Is this OK?
        parliament = self.aq_parent.aq_parent
        teams = parliament.getTeams()
        members = []
        for team in teams:
            members.extend(team.getActiveMembers())
        return DisplayList([(m.UID(), m.getFullname()) for m in members if m])


registerType(Sitting, PROJECTNAME)
# end of class Sitting

##code-section module-footer #fill in your manual code here
##/code-section module-footer



