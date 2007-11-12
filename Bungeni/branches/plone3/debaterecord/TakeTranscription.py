# -*- coding: utf-8 -*-
#
# File: TakeTranscription.py
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
from Products.ATContentTypes.content.file import ATFile
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TakeTranscription_schema = BaseSchema.copy() + \
    getattr(ATFile, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TakeTranscription(BrowserDefaultMixin, BaseContent, ATFile):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ITakeTranscription)

    meta_type = 'TakeTranscription'
    _at_rename_after_creation = True

    schema = TakeTranscription_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declareProtected(permissions.View, 'index_html')
    def index_html(self, REQUEST=None, RESPONSE=None):
        """Download the file
        """
        return ATFile.index_html(self, REQUEST, RESPONSE)



registerType(TakeTranscription, PROJECTNAME)
# end of class TakeTranscription

##code-section module-footer #fill in your manual code here
##/code-section module-footer



