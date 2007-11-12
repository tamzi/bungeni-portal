# -*- coding: utf-8 -*-
#
# File: Bungeni.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 2.0-beta4
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


# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. The items in there
# will be included (by importing) in this file if found.

from Products.CMFCore.permissions import setDefaultRoles
from Products.remember.permissions import ADD_MEMBER_PERMISSION
##code-section config-head #fill in your manual code here
##/code-section config-head


PROJECTNAME = "Bungeni"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))
ADD_CONTENT_PERMISSIONS = {
    'MemberOfPublic': ADD_MEMBER_PERMISSION,
    'MemberOfParliament': ADD_MEMBER_PERMISSION,
    'Staff': ADD_MEMBER_PERMISSION,
    'HelpFolder': 'Bungeni: Add HelpFolder',
    'Motion': 'Bungeni: Add Motion',
    'Question': 'Bungeni: Add Question',
    'LegislationFolder': 'Bungeni: Add LegislationFolder',
    'Amendment': 'Bungeni: Add Amendment',
    'DebateRecordFolder': 'Bungeni: Add DebateRecordFolder',
}

setDefaultRoles('Bungeni: Add HelpFolder', ('Manager','Owner'))
setDefaultRoles('Bungeni: Add Motion', ('Manager','Owner'))
setDefaultRoles('Bungeni: Add Question', ('Manager','Owner'))
setDefaultRoles('Bungeni: Add LegislationFolder', ('Manager','Owner'))
setDefaultRoles('Bungeni: Add Amendment', ('Manager','Owner'))
setDefaultRoles('Bungeni: Add DebateRecordFolder', ('Manager','Owner'))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

##code-section config-bottom #fill in your manual code here
##/code-section config-bottom


# Load custom configuration not managed by archgenxml
try:
    from Products.Bungeni.AppConfig import *
except ImportError:
    pass
