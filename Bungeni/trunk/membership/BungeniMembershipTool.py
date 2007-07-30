# -*- coding: utf-8 -*-
#
# File: BungeniMembershipTool.py
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
from Products.Bungeni.config import *

# additional imports from tagged value 'import'
from Products.Archetypes.utils import DisplayList
from Products.remember.utils import getRememberTypes


from Products.CMFCore.utils import UniqueObject

    
##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    LinesField(
        name='MemberTypesWithHomeFolders',
        widget=MultiSelectionWidget(
            label='Membertypeswithhomefolders',
            label_msgid='Bungeni_label_MemberTypesWithHomeFolders',
            i18n_domain='Bungeni',
        ),
        multiValued=1,
        vocabulary='getMemberTypesVocab'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

BungeniMembershipTool_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class BungeniMembershipTool(UniqueObject, BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(UniqueObject,'__implements__',()),) + (getattr(BaseContent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'BungeniMembershipTool'

    meta_type = 'BungeniMembershipTool'
    portal_type = 'BungeniMembershipTool'
    allowed_content_types = []
    filter_content_types = 1
    global_allow = 0
    #content_icon = 'BungeniMembershipTool.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "BungeniMembershipTool"
    typeDescMsgId = 'description_edit_bungenimembershiptool'
    #toolicon = 'BungeniMembershipTool.gif'

    _at_rename_after_creation = True

    schema = BungeniMembershipTool_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # tool-constructors have no id argument, the id is fixed
    def __init__(self, id=None):
        BaseContent.__init__(self,'portal_bungenimembershiptool')
        self.setTitle('BungeniMembershipTool')
        
        ##code-section constructor-footer #fill in your manual code here
        ##/code-section constructor-footer


    # tool should not appear in portal_catalog
    def at_post_edit_script(self):
        self.unindexObject()
        
        ##code-section post-edit-method-footer #fill in your manual code here
        ##/code-section post-edit-method-footer


    # Methods

    security.declarePublic('getMemberTypesVocab')
    def getMemberTypesVocab(self):
        """ Get a displaylist of remember-based member types.
        """
        remtypes = getRememberTypes(self)
        remtypes.sort()
        remtypes = [(i, i) for i in remtypes]
        return DisplayList(remtypes)


registerType(BungeniMembershipTool, PROJECTNAME)
# end of class BungeniMembershipTool

##code-section module-footer #fill in your manual code here
##/code-section module-footer



