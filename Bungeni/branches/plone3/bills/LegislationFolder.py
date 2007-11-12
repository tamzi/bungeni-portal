# -*- coding: utf-8 -*-
#
# File: LegislationFolder.py
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
from Products.PloneHelpCenter.content.ReferenceManualFolder import HelpCenterReferenceManualFolder
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Bungeni.config import *

# additional imports from tagged value 'import'
from Products.Marginalia.content.AnnotatableDocument import AnnotatableDocument

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

LegislationFolder_schema = BaseFolderSchema.copy() + \
    getattr(HelpCenterReferenceManualFolder, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class LegislationFolder(HelpCenterReferenceManualFolder, BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ILegislationFolder)

    meta_type = 'LegislationFolder'
    _at_rename_after_creation = True

    schema = LegislationFolder_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('PUT_factory')
    def PUT_factory(self,name,typ,body):
        """ Hook PUT creation to make objects of the right type when
            new item uploaded via FTP/WebDAV.
        """
        if typ is None:
            typ, enc = guess_content_type(name, body)
        if typ == 'text/html':
            self.invokeFactory( 'AnnotatableDocument', name )
            # invokeFactory does too much, so the object has to be removed again
            obj = aq_base( self._getOb( name ) )
            self._delObject( name )
            return obj
        return None # take the default, then


registerType(LegislationFolder, PROJECTNAME)
# end of class LegislationFolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



