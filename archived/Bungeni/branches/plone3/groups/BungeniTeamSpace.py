# -*- coding: utf-8 -*-
#
# File: BungeniTeamSpace.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 2.0-beta5
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Jean Jordaan <jean.jordaan@gmail.com>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.TeamSpace.space import TeamSpace
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

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

class BungeniTeamSpace(TeamSpace, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IBungeniTeamSpace)

    meta_type = 'BungeniTeamSpace'
    _at_rename_after_creation = True

    schema = BungeniTeamSpace_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declareProtected(permissions.ManageTeamSpace, 'getAllTeamsDisplayList')
    def getAllTeamsDisplayList(self):
        """
        """
        # TODO constrain this based on portal_type or something. The
        # idea is that e.g. a Committee workspace can only be associated
        # with types of committees and certain offices. See
        # http://code.google.com/p/bungeni-portal/issues/detail?id=80
        team_tool = getToolByName(self, 'portal_teams')
        display_vars = tuple([(team.UID(), team.title_or_id()) for team in team_tool.getTeams()])
        return DisplayList(display_vars)

    security.declarePublic('editTeams')
    def editTeams(self, team_ids):
        """
        edit the teams associated with this teamspace, defer to schema mutator
        """
        # TODO. See
        # http://code.google.com/p/bungeni-portal/issues/detail?id=80
        team_ids = filter(None, team_ids)
        teams_tool = getToolByName(self, 'portal_teams')
        team_uids = [ teams_tool._getOb(tid).UID() for tid in team_ids \
                      if teams_tool._getOb(tid, None)]
        return self.Schema()['space_teams'].getMutator(self)(team_uids)


registerType(BungeniTeamSpace, PROJECTNAME)
# end of class BungeniTeamSpace

##code-section module-footer #fill in your manual code here
##/code-section module-footer



