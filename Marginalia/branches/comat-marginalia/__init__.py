# -*- coding: utf-8 -*-
#
# File: Marginalia.py
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


# There are three ways to inject custom code here:
#
#   - To set global configuration variables, create a file AppConfig.py.
#       This will be imported in config.py, which in turn is imported in
#       each generated class and in this file.
#   - To perform custom initialisation after types have been registered,
#       use the protected code section at the bottom of initialize().
#   - To register a customisation policy, create a file CustomizationPolicy.py
#       with a method register(context) to register the policy.

import logging
logger = logging.getLogger('Marginalia')
logger.info('Installing Product')

import os, os.path
from Globals import package_home
from Products.CMFCore import utils as cmfutils
from Products.CMFCore import permissions as cmfpermissions
from Products.CMFCore import DirectoryView
from Products.CMFPlone.utils import ToolInit
from Products.Archetypes.atapi import *
from Products.Archetypes import listTypes
from Products.Archetypes.utils import capitalize
from config import *

DirectoryView.registerDirectory('skins', product_globals)
DirectoryView.registerDirectory('skins/Marginalia',
                                    product_globals)
DirectoryView.registerDirectory('skins/marginalia',
                                    product_globals)

##code-section custom-init-head #fill in your manual code here
##/code-section custom-init-head
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.GenericSetup import EXTENSION, profile_registry

def initialize(context):
    ##code-section custom-init-top #fill in your manual code here
    ##/code-section custom-init-top

    # imports packages and types for registration
    import content
    import tools
    import interfaces


    # Initialize portal tools
    tools = [tools.Annotations.Annotations]
    ToolInit( PROJECTNAME +' Tools',
                tools = tools,
                icon='tool.gif'
                ).initialize( context )

    # Initialize portal content
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

    profile_registry.registerProfile('marginalia',
                                     'Marginalia',
                                     'Bungeni',
                                     'profiles/default',
                                     'Marginalia',
                                     EXTENSION,
                                     for_=IPloneSiteRoot)


    ##code-section custom-init-bottom #fill in your manual code here
    ##/code-section custom-init-bottom

