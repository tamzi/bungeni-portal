# -*- coding: utf-8 -*-
#
# File: AnnotationMixin.py
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
from Products.Marginalia.interfaces.IAnnotatable import IAnnotatable
from Products.Marginalia.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

AnnotationMixin_schema = schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class AnnotationMixin(BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)
    # zope3 interfaces
    interface.implements(IAnnotatable)

    allowed_content_types = []

    actions =  (


       {'action': "string:${object_url}/annotate",
        'category': "object",
        'id': 'annotate',
        'name': 'annotate',
        'permissions': ("View",),
        'condition': 'python:1'
       },


    )

    _at_rename_after_creation = True

    schema = AnnotationMixin_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('isAnnotatable')
    def isAnnotatable(self):
        """
        """
        return True

# end of class AnnotationMixin

##code-section module-footer #fill in your manual code here
##/code-section module-footer



