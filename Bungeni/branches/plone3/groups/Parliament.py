# -*- coding: utf-8 -*-
#
# File: Parliament.py
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
from Products.Bungeni.groups.BungeniTeam import BungeniTeam
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='number',
        widget=StringWidget(
            label='Number',
            label_msgid='Bungeni_label_number',
            i18n_domain='Bungeni',
        )
    ),

    DateTimeField(
        name='dateElected',
        widget=CalendarWidget(
            label='Dateelected',
            label_msgid='Bungeni_label_dateElected',
            i18n_domain='Bungeni',
        )
    ),

    DateTimeField(
        name='dateInaugurated',
        widget=CalendarWidget(
            label='Dateinaugurated',
            label_msgid='Bungeni_label_dateInaugurated',
            i18n_domain='Bungeni',
        )
    ),

    DateTimeField(
        name='dateDissolved',
        widget=CalendarWidget(
            label='Datedissolved',
            label_msgid='Bungeni_label_dateDissolved',
            i18n_domain='Bungeni',
        )
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Parliament_schema = BaseSchema.copy() + \
    getattr(BungeniTeam, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Parliament(BungeniTeam, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IParliament)

    meta_type = 'Parliament'
    _at_rename_after_creation = True

    schema = Parliament_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('setDateDissolved')
    def setDateDissolved(self, date):
        """
        """
        pass


registerType(Parliament, PROJECTNAME)
# end of class Parliament

##code-section module-footer #fill in your manual code here
##/code-section module-footer



