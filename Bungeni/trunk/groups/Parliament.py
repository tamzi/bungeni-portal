# -*- coding: utf-8 -*-
#
# File: Parliament.py
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
from Products.ATContentTypes.content.event import ATEvent
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Parliament_schema = BaseSchema.copy() + \
    getattr(Team, 'schema', Schema(())).copy() + \
    getattr(ATEvent, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Parliament(BaseContent, Team, ATEvent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),) + (getattr(Team,'__implements__',()),) + (getattr(ATEvent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Parliament'

    meta_type = 'Parliament'
    portal_type = 'Parliament'
    allowed_content_types = [] + list(getattr(Team, 'allowed_content_types', [])) + list(getattr(ATEvent, 'allowed_content_types', []))
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'Parliament.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Parliament"
    typeDescMsgId = 'description_edit_parliament'

    _at_rename_after_creation = True

    schema = Parliament_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(Parliament, PROJECTNAME)
# end of class Parliament

##code-section module-footer #fill in your manual code here
##/code-section module-footer



