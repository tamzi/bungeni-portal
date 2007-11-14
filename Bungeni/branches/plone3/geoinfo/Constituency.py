# -*- coding: utf-8 -*-
#
# File: Constituency.py
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

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Relations.field import RelationField
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    IntegerField(
        name='NumberOfVoters',
        widget=IntegerField._properties['widget'](
            label='Numberofvoters',
            label_msgid='Bungeni_label_NumberOfVoters',
            i18n_domain='Bungeni',
        )
    ),

    ComputedField(
        name='Province',
        widget=ComputedField._properties['widget'](
            label='Province',
            label_msgid='Bungeni_label_Province',
            i18n_domain='Bungeni',
        )
    ),

    ComputedField(
        name='Region',
        widget=ComputedField._properties['widget'](
            label='Region',
            label_msgid='Bungeni_label_Region',
            i18n_domain='Bungeni',
        )
    ),

    DateTimeField(
        name='CreatedDate',
        widget=CalendarWidget(
            label='Createddate',
            label_msgid='Bungeni_label_CreatedDate',
            i18n_domain='Bungeni',
        )
    ),

    RelationField(
        name='memberofparliaments',
        widget=ReferenceWidget(
            label='Memberofparliaments',
            label_msgid='Bungeni_label_memberofparliaments',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='constituency'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Constituency_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Constituency(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IConstituency)

    meta_type = 'Constituency'
    _at_rename_after_creation = True

    schema = Constituency_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getProvince')
    def getProvince(self):
        """
        """
        pass

    security.declarePublic('getRegion')
    def getRegion(self):
        """
        """
        pass


registerType(Constituency, PROJECTNAME)
# end of class Constituency

##code-section module-footer #fill in your manual code here
##/code-section module-footer



