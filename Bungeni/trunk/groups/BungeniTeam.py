# -*- coding: utf-8 -*-
#
# File: BungeniTeam.py
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
from Products.TeamSpace.team import Team
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

BungeniTeam_schema = BaseSchema.copy() + \
    getattr(Team, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class BungeniTeam(Team):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(Team,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'BungeniTeam'

    meta_type = 'BungeniTeam'
    portal_type = 'BungeniTeam'
    allowed_content_types = [] + list(getattr(Team, 'allowed_content_types', []))
    filter_content_types = 0
    global_allow = 1
    #content_icon = 'BungeniTeam.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "BungeniTeam"
    typeDescMsgId = 'description_edit_bungeniteam'

    _at_rename_after_creation = True

    schema = BungeniTeam_schema

    ##code-section class-header #fill in your manual code here

    # All the overridden methods below are just
    # s/portal_teams/portal_bungeniteamstool/ .. is there a better way?

    ##/code-section class-header

    # Methods

    security.declarePublic('addMember')
    def addMember(self, member_id, membership_type=None, reindex=True):
        """
        add a membership object with the given member id and associate
        via archetypes reference engine with the member object
        """
        pm_tool = getToolByName(self, 'portal_membership')
        pt_tool = getToolByName(self, 'portal_types')
        teams_tool = getToolByName(self, 'portal_bungeniteamstool')

        membership = self._getOb(member_id, None)
        if membership is not None: # member already exists
            return

        member = pm_tool.getMemberById(member_id)

        if member is None:
            raise MemberNotFound(str(member_id))

        if membership_type is None:
            membership_type = self.getDefaultMembershipType()
        elif not membership_type in teams_tool.allowed_membership_types:
            raise RuntimeError("Invalid Membership Type %r" % membership_type)

        pt_tool.constructContent(membership_type, self, member_id)

        membership = self._getOb(member_id)
        refclass = self.membership_reference_class
        member.addReference(membership,
                            relationship=refclass.relationship,
                            referenceClass=refclass)

        # Assign the default Role to the member
        # We want to assign the default roles to the member
        membership.editTeamRoles(self._default_roles)

        # And notify space objects as these are the most likely
        # subclasses that could hook the event.
        spaces = self.getTeamSpaces()
        for space in spaces:
            space._updateMember('add', member, membership, self)
        if reindex:
            self.reindexTeamSpaceSecurity()

        return membership

    security.declarePublic('getMembers')
    def getMembers(self):
        """
        return all members in the team
        """
        ttool = getToolByName(self, 'portal_bungeniteamstool')
        rship = MemberTeamRelation.relationship
        mbrains = ttool.getRefSourceBrains(self,
                                           relationship=rship)
        return [m.getObject() for m in mbrains]

    security.declarePublic('getOrphanedRoles')
    def getOrphanedRoles(self):
        """
        get the roles that are now hidden from the team zmi interface
        """
        tt = getToolByName(self, 'portal_bungeniteamstool')

    security.declarePublic('initializeArchetype')
    def initializeArchetype(self, **kw):
        BaseBTreeFolder.initializeArchetype(self, **kw)
        # Use our aq context to find the team tool and get our initial state

        tt = getToolByName(self, 'portal_bungeniteamstool')

        self.allowed_content_types = tt.allowed_membership_types

        if not self._active_states:
            self._active_states = tt.getDefaultActiveStates()

        if not self._allowed_team_roles:
            self._allowed_team_roles = tt.getDefaultAllowedRoles()

        if not self._default_roles:
            self._default_roles = tt.getDefaultRoles()

        if not self._default_membership_type:
            self._default_membership_type = tt.getDefaultMembershipType()


registerType(BungeniTeam, PROJECTNAME)
# end of class BungeniTeam

##code-section module-footer #fill in your manual code here
##/code-section module-footer



