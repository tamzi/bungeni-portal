# -*- coding: utf-8 -*-
#
# File: DebateRecordFolder.py
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
from Products.PloneHelpCenter.content.ReferenceManualFolder import HelpCenterReferenceManualFolder
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import DisplayList
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

DebateRecordFolder_schema = BaseFolderSchema.copy() + \
    getattr(HelpCenterReferenceManualFolder, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class DebateRecordFolder(BaseFolder, HelpCenterReferenceManualFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseFolder,'__implements__',()),) + (getattr(HelpCenterReferenceManualFolder,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'DebateRecordFolder'

    meta_type = 'DebateRecordFolder'
    portal_type = 'DebateRecordFolder'
    allowed_content_types = ['DebateRecord', 'Minutes', 'Take', 'RotaFolder']
    filter_content_types = 1
    global_allow = 0
    #content_icon = 'DebateRecordFolder.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "A Hansard folder contains Hansard reports."
    typeDescMsgId = 'description_edit_debaterecordfolder'

    _at_rename_after_creation = True

    schema = DebateRecordFolder_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getReportersVocab')
    def getReportersVocab(self):
        """ Get the current parliament's team of reporters, and return
        the active memberships.
        """
        members = self.getReporters()
        return DisplayList([(m.UID(), m.Title()) for m in members])

    security.declarePublic('getReporters')
    def getReporters(self):
        # TODO: this looks for all Reporters in all teams. If someone is
        # a Reporter in more than one team, this can return duplicates.
        # Is that a bug?
        catalog = getToolByName(self, 'portal_catalog')
        reporter_proxies = catalog.search(
                {'allowedRolesAndUsers': 'Reporter', 'review_state': 'active',
                    'portal_type': 'Team Membership'}
                )
        reporters = [p.getObject() for p in reporter_proxies]
        members = [r.getMember() for r in reporters]
        return members


registerType(DebateRecordFolder, PROJECTNAME)
# end of class DebateRecordFolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



