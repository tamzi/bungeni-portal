# -*- coding: utf-8 -*-
#
# File: LookAndFeel.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 1.5.1-svn
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

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.BungeniSkinPanafrica.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

LookAndFeel_schema = schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class LookAndFeel(BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)

    allowed_content_types = []

    actions =  (


       {'action': "string:${object_url}/main_template",
        'category': "object",
        'id': 'main_template',
        'name': 'main_template',
        'permissions': ("View",),
        'condition': 'python:1'
       },


       {'action': "string:${object_url}/global_logo",
        'category': "object",
        'id': 'global_logo',
        'name': 'global_logo',
        'permissions': ("View",),
        'condition': 'python:1'
       },


       {'action': "string:${object_url}/global_sections",
        'category': "object",
        'id': 'global_sections',
        'name': 'global_sections',
        'permissions': ("View",),
        'condition': 'python:1'
       },


       {'action': "string:${object_url}/global_siteactions",
        'category': "object",
        'id': 'global_siteactions',
        'name': 'global_siteactions',
        'permissions': ("View",),
        'condition': 'python:1'
       },


    )

    _at_rename_after_creation = True

    schema = LookAndFeel_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
# end of class LookAndFeel

##code-section module-footer #fill in your manual code here
##/code-section module-footer



