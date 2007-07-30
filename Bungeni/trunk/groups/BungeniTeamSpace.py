# -*- coding: utf-8 -*-
#
# File: BungeniTeamSpace.py
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
from Products.TeamSpace.space import TeamSpace
from Products.Bungeni.config import *

# additional imports from tagged value 'import'
from Products.TeamSpace import permissions

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

BungeniTeamSpace_schema = BaseSchema.copy() + \
    getattr(TeamSpace, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class BungeniTeamSpace(BaseContent, TeamSpace):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),) + (getattr(TeamSpace,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'BungeniTeamSpace'

    meta_type = 'BungeniTeamSpace'
    portal_type = 'BungeniTeamSpace'
    allowed_content_types = [] + list(getattr(TeamSpace, 'allowed_content_types', []))
    filter_content_types = 0
    global_allow = 1
    #content_icon = 'BungeniTeamSpace.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "BungeniTeamSpace"
    typeDescMsgId = 'description_edit_bungeniteamspace'

    _at_rename_after_creation = True

    schema = BungeniTeamSpace_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declareProtected(permissions.ManageTeamSpace, 'getAllTeamsDisplayList')
    def getAllTeamsDisplayList(self):
        """
        """
        team_tool = getToolByName(self, 'portal_bungeniteamstool')
        # TODO constrain this based on portal_type or something
        display_vars = tuple([(team.UID(), team.title_or_id()) for team in team_tool.getTeams(self.portal_type)])
        return DisplayList(display_vars)

    security.declarePublic('editTeams')
    def editTeams(self, team_ids):
        """
        edit the teams associated with this teamspace, defer to schema mutator
        """
        team_ids = filter(None, team_ids)
        teams_tool = getToolByName(self, 'portal_bungeniteamstool')
        team_uids = [ teams_tool._getOb(tid).UID() for tid in team_ids \
                      if teams_tool._getOb(tid, None)]
        return self.Schema()['space_teams'].getMutator(self)(team_uids)


registerType(BungeniTeamSpace, PROJECTNAME)
# end of class BungeniTeamSpace

##code-section module-footer #fill in your manual code here
##/code-section module-footer



