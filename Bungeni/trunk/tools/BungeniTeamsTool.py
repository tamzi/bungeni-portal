# -*- coding: utf-8 -*-
#
# File: BungeniTeamsTool.py
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
from Products.TeamSpace.tool import TeamsTool
from Products.Bungeni.config import *


from Products.CMFCore.utils import UniqueObject

    
##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

BungeniTeamsTool_schema = BaseBTreeFolderSchema.copy() + \
    getattr(TeamsTool, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class BungeniTeamsTool(UniqueObject, BaseBTreeFolder, TeamsTool):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(UniqueObject,'__implements__',()),) + (getattr(BaseBTreeFolder,'__implements__',()),) + (getattr(TeamsTool,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'BungeniTeamsTool'

    meta_type = 'BungeniTeamsTool'
    portal_type = 'BungeniTeamsTool'
    allowed_content_types = ['Parliament', 'Party', 'Committee', 'Ministry', 'Reporters'] + list(getattr(TeamsTool, 'allowed_content_types', []))
    filter_content_types = 1
    global_allow = 0
    #content_icon = 'BungeniTeamsTool.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "BungeniTeamsTool"
    typeDescMsgId = 'description_edit_bungeniteamstool'
    #toolicon = 'BungeniTeamsTool.gif'

    _at_rename_after_creation = True

    schema = BungeniTeamsTool_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # tool-constructors have no id argument, the id is fixed
    def __init__(self, id=None):
        BaseBTreeFolder.__init__(self,'portal_bungeniteamstool')
        self.setTitle('BungeniTeamsTool')
        
        ##code-section constructor-footer #fill in your manual code here
        ##/code-section constructor-footer


    # tool should not appear in portal_catalog
    def at_post_edit_script(self):
        self.unindexObject()
        
        ##code-section post-edit-method-footer #fill in your manual code here
        ##/code-section post-edit-method-footer


    # Methods


registerType(BungeniTeamsTool, PROJECTNAME)
# end of class BungeniTeamsTool

##code-section module-footer #fill in your manual code here
##/code-section module-footer



