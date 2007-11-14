# -*- coding: utf-8 -*-
#
# File: LegislationFolder.py
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



