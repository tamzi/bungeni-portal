# -*- coding: utf-8 -*-
#
# File: Question.py
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

    BooleanField(
        name='requireWrittenAnswer',
        widget=BooleanField._properties['widget'](
            label="Require written answer?",
            label_msgid='Bungeni_label_requireWrittenAnswer',
            i18n_domain='Bungeni',
        )
    ),

    RelationField(
        name='respondents',
        widget=ReferenceWidget(
            label='Respondents',
            label_msgid='Bungeni_label_respondents',
            i18n_domain='Bungeni',
        ),
        multiValued=1,
        relationship='Question_MemberOfParliament'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Question_schema = BaseFolderSchema.copy() + \
    getattr(ParliamentaryEvent, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Question(BrowserDefaultMixin, BaseFolder, ParliamentaryEvent):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IQuestion, IAuditable)

    meta_type = 'Question'
    _at_rename_after_creation = True

    schema = Question_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(Question, PROJECTNAME)
# end of class Question

##code-section module-footer #fill in your manual code here
##/code-section module-footer



