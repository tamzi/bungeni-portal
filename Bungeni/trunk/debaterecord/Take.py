# -*- coding: utf-8 -*-
#
# File: Take.py
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
from zope import interface
from Products.ATContentTypes.content.file import ATFile
from Products.Bungeni.interfaces.ITake import ITake
from Products.Relations.field import RelationField
from Products.Bungeni.config import *

# additional imports from tagged value 'import'
from appy.pod import renderer

##code-section module-header #fill in your manual code here
import os
import time
import tempfile
from Products.Archetypes.utils import DisplayList
from Products.CMFCore.utils import getToolByName
import Products.Bungeni
##/code-section module-header

schema = Schema((

    RelationField(
        name='RotaItem',
        vocabulary='getRotaItemVocab',
        widget=ReferenceWidget(
            macro_edit="rotaitem_edit",
            label='Rotaitem',
            label_msgid='Bungeni_label_RotaItem',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='take_rotaitem'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Take_schema = BaseFolderSchema.copy() + \
    getattr(ATFile, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Take(BaseFolder, ATFile):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseFolder,'__implements__',()),) + (getattr(ATFile,'__implements__',()),)
    # zope3 interfaces
    interface.implements(ITake)

    # This name appears in the 'add' box
    archetype_name = 'Take'

    meta_type = 'Take'
    portal_type = 'Take'
    allowed_content_types = ['TakeTranscription'] + list(getattr(ATFile, 'allowed_content_types', []))
    filter_content_types = 1
    global_allow = 0
    #content_icon = 'Take.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Take"
    typeDescMsgId = 'description_edit_take'

    _at_rename_after_creation = True

    schema = Take_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getNextRotaItem')
    def getNextRotaItem(self):
        """
        """
        rota_items = self.getRotaItems()
        if not rota_items:
            self.plone_log('getNextRotaItem> No items') #DBG
            return []
        for ri in rota_items:
            if not ri.getTake():
                break
        # return the first RotaItem w/o a take, or the last one.
        self.plone_log('getNextRotaItem> %s: %s'%(ri.getId(), ri.UID())) #DBG
        return ri.UID()

    security.declarePublic('getRotaItemVocab')
    def getRotaItemVocab(self):
        """
        """
        ris = self.getRotaItems()
        return DisplayList([(ri.UID(), ri.Title()) for ri in ris])

    security.declarePublic('getRotaItems')
    def getRotaItems(self):
        """
        """
        parent = self
        while parent.portal_type != 'DebateRecordFolder':
            parent = parent.aq_parent
        rf = parent.contentValues(
                filter={'portal_type': 'RotaFolder'})
        if rf:
            rota_items = rf[0].contentValues(
                    filter={'portal_type': 'RotaItem'})
            return rota_items
        else:
            return []

    security.declarePublic('getNotAddableTypes')
    def getNotAddableTypes(self):
        """ A take can have only one transcription.
        """
        transcription = self.contentIds(
                filter={'portal_type': 'TakeTranscription'})
        if transcription:
            return ['TakeTranscription', ]
        return []

    security.declarePrivate('_generateTakeTranscription')
    def _generateTakeTranscription(self):
        """
        """
        # Get our associated RotaItem
        self.setRotaItem(self.REQUEST.form['RotaItem'])
        ri = self.getRotaItem()

        # Add a new transcription
        t_id = self.generateUniqueId('TakeTranscription')
        self.invokeFactory('TakeTranscription', t_id,
                title=self.getRotaItem().Title())
        tt = self[t_id]

        # Use a template to generate a new document
        #DBG from ipdb import set_trace; set_trace()
        # fd, fn = tempfile.mkstemp()
        tempFileName = '/tmp/%s.%f.%s' % (self._at_uid, time.time(), 'odt')
        r = renderer.Renderer(
                '%s/taketranscription.odt' % os.path.dirname(
                    Products.Bungeni.__file__),
                {'InsertedText': ri.Title()},
                tempFileName)
        r.run()

        # Set that document on our transcription
        new_file = open(tempFileName, 'rb')
        tt.setFile(new_file)
        os.remove(tempFileName)


registerType(Take, PROJECTNAME)
# end of class Take

##code-section module-footer #fill in your manual code here
def addedTake(obj, event):
    """ After the Take has been added, populate it with a TakeTranscription.
    """
    if obj.isTemporary():
        #DBG log('addedRotaFolder> Not yet!')
        return

    obj._generateTakeTranscription()
##/code-section module-footer



