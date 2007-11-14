# -*- coding: utf-8 -*-
#
# File: Session.py
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
        name='sessionType',
        widget=SelectionWidget(
            label='Sessiontype',
            label_msgid='Bungeni_label_sessionType',
            i18n_domain='Bungeni',
        ),
        vocabulary=['First Session', 'Second Session', 'Third Session']
    ),

    copied_fields['startDate'],

    copied_fields['endDate'],

    TextField(
        name='notes',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label='Notes',
            label_msgid='Bungeni_label_notes',
            i18n_domain='Bungeni',
        ),
        default_output_type='text/html'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Session_schema = BaseFolderSchema.copy() + \
    getattr(ParliamentaryEvent, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Session(BrowserDefaultMixin, BaseFolder, ParliamentaryEvent):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ISession)

    meta_type = 'Session'
    _at_rename_after_creation = True

    schema = Session_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(Session, PROJECTNAME)
# end of class Session

##code-section module-footer #fill in your manual code here
##/code-section module-footer



