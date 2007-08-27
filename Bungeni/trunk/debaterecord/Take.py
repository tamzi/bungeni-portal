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
from Products.Relations.field import RelationField
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
from Products.Archetypes.utils import DisplayList
from Products.CMFCore.utils import getToolByName
##/code-section module-header

schema = Schema((

    RelationField(
        name='RotaItem',
        vocabulary='getRotaItemVocab',
        widget=ReferenceWidget(
            label='Rotaitem',
            label_msgid='Bungeni_label_RotaItem',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='take_rotaitem',
        default_method="getNextRotaItem"
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
        if rota_items:
            return [ri for ri in rota_items if not ri.getReporter()]
        return []

    security.declarePublic('getRotaItemVocab')
    def getRotaItemVocab(self):
        """
        """
        ris = self.getRotaItems()
        return DisplayList([(ri.UID(), ri.Title()) for ri in ris])

    # Manually created methods

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



registerType(Take, PROJECTNAME)
# end of class Take

##code-section module-footer #fill in your manual code here
##/code-section module-footer



