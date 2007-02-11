# -*- coding: utf-8 -*-
#
# File: Annotations.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 1.5.1-svn
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
from Products.Marginalia.config import *


from Products.CMFCore.utils import UniqueObject

    
##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Annotations_schema = BaseBTreeFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Annotations(UniqueObject, BaseBTreeFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(UniqueObject,'__implements__',()),) + (getattr(BaseBTreeFolder,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Annotations'

    meta_type = 'Annotations'
    portal_type = 'Annotations'
    allowed_content_types = ['Annotation']
    filter_content_types = 1
    global_allow = 0
    #content_icon = 'Annotations.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Annotations"
    typeDescMsgId = 'description_edit_annotations'
    #toolicon = 'Annotations.gif'


    actions =  (


       {'action': "string:${object_url}/listAnnotations",
        'category': "object",
        'id': 'listAnnotations',
        'name': 'listAnnotations',
        'permissions': ("View",),
        'condition': 'python:1'
       },


    )

    _at_rename_after_creation = True

    schema = Annotations_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # tool-constructors have no id argument, the id is fixed
    def __init__(self, id=None):
        BaseBTreeFolder.__init__(self,'portal_annotations')
        self.setTitle('Annotations')
        
        ##code-section constructor-footer #fill in your manual code here
        ##/code-section constructor-footer


    # tool should not appear in portal_catalog
    def at_post_edit_script(self):
        self.unindexObject()
        
        ##code-section post-edit-method-footer #fill in your manual code here
        ##/code-section post-edit-method-footer


    # Methods

    security.declarePublic('preference') #XXX fix security
    def preference(self):
        """ Quick & REST dirty preferences. Move to configlet later.
        """
        rest_verb_map = {
            'GET': self.listPreferences,
            'POST': self.setPreference,
            }
        verb = rest_verb_map[self.REQUEST.REQUEST_METHOD]
        return verb()

    def listPreferences(self):
        """ Stub .. TODO
        """
        return ('annotations.show:true\n'
                'annotations.show-user:anonymous\n'
                'annotations.note-edit-mode:note freeform\n')

    def setPreference(self):
        """
        """
        # TODO: Ignore prefence saving for now
        self.REQUEST.RESPONSE.setHeader('NoContent')
        return

    security.declarePublic('annotate')
    def annotate(self):
        """ Examine request for REST verbs.
        """
        rest_verb_map = {
            'GET': self.listAnnotations, # Finds listAnnotations.pt in skins
            'POST': self.createAnnotation,
            'PUT': self.updateAnnotation,
            'DELETE': self.deleteAnnotation,
            }
        verb = rest_verb_map[self.REQUEST.REQUEST_METHOD]
        return verb()

    security.declarePublic('createAnnotation')
    def createAnnotation(self):
        """ Create annotation from POST.
        """
        params = {
            'url': '',
            'range': '',
            'note': '',
            'access': '',
            'quote': '',
            'quote_title': '',
            'quote_author': '',
            'link': '',
            }
        params.update(self.REQUEST)
        plone = getToolByName(self, 'portal_url').getPortalObject()
        obj_id = plone.generateUniqueId('Annotation')
        return self.invokeFactory('Annotation', id=obj_id, **params)

    security.declarePublic('updateAnnotation')
    def updateAnnotation(self):
        """
        """
        params = {
            'id': '',
            'note': '',
            'access': '',
            'link': '',
            }
        params.update(self.REQUEST)
        return self.edit(**params)

    security.declarePublic('deleteAnnotation')
    def deleteAnnotation(self):
        """
        """
        annotation_id = self.REQUEST.get('id', None)
        if annotation_id:
            self.manage_delObjects(annotation_id)
            self.REQUEST.RESPONSE.setStatus('NoContent')
            return
        self.REQUEST.RESPONSE.setStatus('BadRequest') # No id
        return

    security.declarePublic('getFeedUID')
    def getFeedUID(self):
        """
        """
        return 'tag:%s,%s:annotation' % ('localhost', '2007-01-24')

    security.declarePublic('getSortedFeedEntries')
    def getSortedFeedEntries(self, user, url):
        """
        """
        # TODO get from catalog, filter on user and url
        annotations = self.contentValues('Annotation')
        return annotations

    security.declarePublic('getBaseURL')
    def getBaseURL(self):
        """
        """
        return self.absolute_url()


registerType(Annotations, PROJECTNAME)
# end of class Annotations

##code-section module-footer #fill in your manual code here
##/code-section module-footer



