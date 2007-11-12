# -*- coding: utf-8 -*-
#
# File: Session.py
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



