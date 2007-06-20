# -*- coding: utf-8 -*-
#
# File: VoteCount.py
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
from Products.Bungeni.votes.Vote import Vote
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    ComputedField(
        name='Pass',
        widget=ComputedField._properties['widget'](
            label='Pass',
            label_msgid='Bungeni_label_Pass',
            i18n_domain='Bungeni',
        )
    ),

    ComputedField(
        name='NumberOfAye',
        widget=ComputedField._properties['widget'](
            label='Numberofaye',
            label_msgid='Bungeni_label_NumberOfAye',
            i18n_domain='Bungeni',
        )
    ),

    ComputedField(
        name='NumberOfNay',
        widget=ComputedField._properties['widget'](
            label='Numberofnay',
            label_msgid='Bungeni_label_NumberOfNay',
            i18n_domain='Bungeni',
        )
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

VoteCount_schema = BaseFolderSchema.copy() + \
    getattr(Vote, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class VoteCount(BaseFolder, Vote):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseFolder,'__implements__',()),) + (getattr(Vote,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'VoteCount'

    meta_type = 'VoteCount'
    portal_type = 'VoteCount'
    allowed_content_types = ['VoteOfMP'] + list(getattr(Vote, 'allowed_content_types', []))
    filter_content_types = 1
    global_allow = 0
    #content_icon = 'VoteCount.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "VoteCount"
    typeDescMsgId = 'description_edit_votecount'

    _at_rename_after_creation = True

    schema = VoteCount_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getPass')
    def getPass(self):
        """
        """
        pass

    security.declarePublic('getNumberOfAye')
    def getNumberOfAye(self):
        """
        """
        pass

    security.declarePublic('getNumberOfNay')
    def getNumberOfNay(self):
        """
        """
        pass


registerType(VoteCount, PROJECTNAME)
# end of class VoteCount

##code-section module-footer #fill in your manual code here
##/code-section module-footer



