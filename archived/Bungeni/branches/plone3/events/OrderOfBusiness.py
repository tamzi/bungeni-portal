# -*- coding: utf-8 -*-
#
# File: OrderOfBusiness.py
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

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

OrderOfBusiness_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class OrderOfBusiness(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IOrderOfBusiness)

    meta_type = 'OrderOfBusiness'
    _at_rename_after_creation = True

    schema = OrderOfBusiness_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(OrderOfBusiness, PROJECTNAME)
# end of class OrderOfBusiness

##code-section module-footer #fill in your manual code here
##/code-section module-footer



