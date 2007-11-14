# -*- coding: utf-8 -*-
#
# File: ParliamentaryDocument.py
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

    StringField(
        name='URI',
        widget=StringWidget(
            label='Uri',
            label_msgid='Bungeni_label_URI',
            i18n_domain='Bungeni',
        )
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

ParliamentaryDocument_schema = schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class ParliamentaryDocument(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IParliamentaryDocument)

    _at_rename_after_creation = True

    schema = ParliamentaryDocument_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

# end of class ParliamentaryDocument

##code-section module-footer #fill in your manual code here
##/code-section module-footer



