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

# additional imports from tagged value 'import'
from Products.TeamSpace.relations import MemberTeamRelation
from Products.Archetypes.utils import DisplayList

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from Products.TeamSpace.permissions import *
from Products.TeamSpace.team import team_type_information
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

    actions = team_type_information['actions']

    ##/code-section class-header

    # Methods

    security.declareProtected(ViewAllTeam, 'getActiveMembersByRoles')
    def getActiveMembersByRoles(self,roles):
        """
        """
        if type(roles) == type(''):
            roles = [roles]
        memberships = self.getMembershipsByStates('active')
        memberships_with_roles = []
        for r in roles:
            memberships.extend(
                    [m for m in memberships if r in m.getTeamRoles()]
                    )
        return memberships_with_roles

    security.declarePublic('_constrainMembershipRoles')
    def _constrainMembershipRoles(self,constrained_roles, member_roles):
        """
        """
        members_per_role = {}
        for mr in member_roles:
            for role in mr.get('roles', []):
                members = members_per_role.setdefault(role, [])
                if mr['member_id'] not in members:
                    members.append(mr['member_id'])
                    members_per_role[role] = members
        for role, number in constrained_roles.items():
            # TODO: fail more gracefully?
            member_ids = members_per_role.get(role, [])
            assert len(member_ids) <= number

    security.declarePublic('_get_member_roles')
    def _get_member_roles(self,members=[],new_roles=[]):
        """
        """
        member_roles_map = {}
        active_memberships = self.getActiveMemberships()
        for membership in active_memberships:
            member_roles_map[membership.getId()] = membership.getTeamRoles()
        if type(members) != type([]):
            members = [members]
        if type(new_roles) != type([]):
            new_roles = [new_roles]
        for member in members:
            roles = member_roles_map[member.getId()]
            for role in new_roles:
                if role not in roles:
                    roles.append(role)
            member_roles_map[member.getId()] = roles
        return [{'member_id': mid, 'roles': mroles} for mid, mroles in member_roles_map.items()]

    security.declarePublic('getMembershipVocab')
    def getMembershipVocab(self):
        """ Return a DisplayList of memberships of this team, as vocab
        for team officer references.
        """
        return DisplayList([(m.UID(), m.Title()) for m in self.getActiveMembers()])

    security.declarePublic('_get_member_roles_from_UIDs')
    def _get_member_roles_from_UIDs(self, uids, roles):
        mt = getToolByName(self, 'portal_bungenimembershiptool')
        members = [mt.getMemberByUID(uid) for uid in uids if uid]
        return self._get_member_roles(members, roles)


registerType(BungeniTeam, PROJECTNAME)
# end of class BungeniTeam

##code-section module-footer #fill in your manual code here
##/code-section module-footer



