# -*- coding: utf-8 -*-
#
# File: DebateRecordFolder.py
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
from zope import interface
from zope.interface import implements
import interfaces
from Products.PloneHelpCenter.content.ReferenceManualFolder import HelpCenterReferenceManualFolder
from Products.Bungeni.groups.BungeniTeamSpace import BungeniTeamSpace
from Products.Bungeni.interfaces.IDebateRecordFolder import IDebateRecordFolder
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import DisplayList
##/code-section module-header

copied_fields = {}
copied_fields['space_teams'] = BungeniTeamSpace.schema['space_teams'].copy()
copied_fields['space_teams'].widget.macro_edit = "space_teams_edit"
schema = Schema((

    copied_fields['space_teams'],

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

DebateRecordFolder_schema = BaseFolderSchema.copy() + \
    getattr(HelpCenterReferenceManualFolder, 'schema', Schema(())).copy() + \
    getattr(BungeniTeamSpace, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class DebateRecordFolder(HelpCenterReferenceManualFolder, BrowserDefaultMixin, BungeniTeamSpace):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IDebateRecordFolder, IDebateRecordFolder)

    meta_type = 'DebateRecordFolder'
    _at_rename_after_creation = True

    schema = DebateRecordFolder_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getReportersForSittingVocab')
    def getReportersForSittingVocab(self):
        """ Get the current parliament's team of reporters, and return
        the active memberships.
        """
        rota_tool = getToolByName(self, 'portal_rotatool')
        members = rota_tool.getAvailableReporters()
        return DisplayList([(m.UID(), m.Title()) for m in members])

    security.declarePublic('getSpaceTeamsDefault')
    def getSpaceTeamsDefault(self):
        """ Used from space_team_edit.pt
        """
        catalog = getToolByName(self, 'uid_catalog')
        team_ids = [p.UID for p in catalog(portal_type='DebateRecordOffice')]
        return team_ids

    security.declarePublic('getNotAddableTypes')
    def getNotAddableTypes(self):
        """ Don't allow a Rota folder to be added until we have proper
        parameters for it.
        """
        rota_tool = getToolByName(self, 'portal_rotatool')
        if (self.contentValues(filter={'portal_type': 'RotaFolder'}) or
                (not rota_tool.getReportingLeadTime()) or
                (not rota_tool.getTakeLength()) or
                (not rota_tool.getExtraTakes()) or
                (not rota_tool.getAvailableReporters())
                ):
            return ['RotaFolder', ]
        return []

    security.declareProtected(permissions.View, 'getItemsByAudiencesAndSections')
    def getItemsByAudiencesAndSections(self, **kwargs):
        """ Narrow search to allowed PHC types.
        """
        query = {'portal_type': ['HelpCenterReferenceManual', ]}
        query.update(kwargs)
        return HelpCenterReferenceManualFolder.getItemsByAudiencesAndSections(self, **query)


registerType(DebateRecordFolder, PROJECTNAME)
# end of class DebateRecordFolder

##code-section module-footer #fill in your manual code here
def addedDebateRecordFolder(obj, event):
    """ A DebateRecordFolder is always associated with teams of type
    DebateRecordOffice by default.
    """
    if obj.isTemporary():
        #DBG log('addedRotaFolder> Not yet!')
        return

    catalog = getToolByName(obj, 'portal_catalog')
    default_teams = [p.getId for p in catalog(portal_type='DebateRecordOffice')]

    current_teams = obj.getTeams()
    obj.editTeams(current_teams+default_teams)
##/code-section module-footer



