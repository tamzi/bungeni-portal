# -*- coding: utf-8 -*-
#
# File: Motion.py
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
from zope import interface
from zope.interface import implements
import interfaces
from Products.Bungeni.events.ParliamentaryEvent import ParliamentaryEvent
from Products.AuditTrail.interfaces.IAuditable import IAuditable
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Relations.field import RelationField
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    RelationField(
        name='secondedBy',
        widget=ReferenceWidget(
            label='Secondedby',
            label_msgid='Bungeni_label_secondedBy',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='Motion_MemberOfParliament'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Motion_schema = BaseFolderSchema.copy() + \
    getattr(ParliamentaryEvent, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Motion(BrowserDefaultMixin, BaseFolder, ParliamentaryEvent):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IMotion, IAuditable)

    meta_type = 'Motion'
    _at_rename_after_creation = True

    schema = Motion_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(Motion, PROJECTNAME)
# end of class Motion

##code-section module-footer #fill in your manual code here
##/code-section module-footer



