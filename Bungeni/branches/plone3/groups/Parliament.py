# -*- coding: utf-8 -*-
#
# File: Parliament.py
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



