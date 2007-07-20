# -*- coding: utf-8 -*-
#
# File: AnnotatableDocument.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 1.6.0-beta-svn
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
from Products.Marginalia.content.AnnotationMixin import AnnotationMixin
from Products.ATContentTypes.content.document import ATDocument
from Products.Marginalia.config import *
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((
#    ReferenceField('reference_link', 
#                   multiValued=0,
#                   allowed_types=('ATDocument','ATFile', 'Article'),
#                   relationship='referenceLink1',
#                   widget=ReferenceBrowserWidget(default_search_index='SearchableText', description='This is the first field. Pick an object.')),
),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

AnnotatableDocument_schema = BaseSchema.copy() + \
    getattr(AnnotationMixin, 'schema', Schema(())).copy() + \
    getattr(ATDocument, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class AnnotatableDocument(BaseContent, AnnotationMixin, ATDocument):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),) + (getattr(AnnotationMixin,'__implements__',()),) + (getattr(ATDocument,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'AnnotatableDocument'

    meta_type = 'AnnotatableDocument'
    portal_type = 'AnnotatableDocument'
    allowed_content_types = [] + list(getattr(AnnotationMixin, 'allowed_content_types', [])) + list(getattr(ATDocument, 'allowed_content_types', []))
    filter_content_types = 0
    global_allow = 1
    #content_icon = 'AnnotatableDocument.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "AnnotatableDocument"
    typeDescMsgId = 'description_edit_annotatabledocument'

    _at_rename_after_creation = True

    schema = AnnotatableDocument_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # TODO: The following are necessary for the pop-up reference widget to work
    # I don't know how to determine these values, nor do I know how to
    # instantiate an AtReferenceBrowserWidget as a source for them
    # (at least not without embedding that widget in the page, which I don't want)
#    security.declarePublic( 'getReferenceBrowserPath' )
#    def getReferenceBrowserStartupDir( self ):
#        return 'http://localhost:8080/Plone'
#        
#    security.declarePublic( 'getReferenceBrowserAtUrl' )
#    def getReferenceBrowserAtUrl( self ):
#        return 'http://localhost:8080/Plone'

#    security.declarePublic( 'getReferenceLink' )
#    def getReferenceLink( self ):
#        self.folder.invokeFactory( 'ReferenceField', 'ref1' )
#        obj = self.folder.ObjectIds( ) [ 'ref1' ]
#        return self.getReference_link( )

registerType(AnnotatableDocument, PROJECTNAME)
# end of class AnnotatableDocument

##code-section module-footer #fill in your manual code here
##/code-section module-footer



