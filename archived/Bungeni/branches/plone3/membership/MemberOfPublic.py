# -*- coding: utf-8 -*-
#
# File: MemberOfPublic.py
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
from Products.Bungeni.membership.BungeniMember import BungeniMember
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

# imports needed by remember
from Products.remember.content.member import BaseMember
from Products.remember.permissions import \
        VIEW_PUBLIC_PERMISSION, EDIT_ID_PERMISSION, \
        EDIT_PROPERTIES_PERMISSION, VIEW_OTHER_PERMISSION,  \
        VIEW_SECURITY_PERMISSION, EDIT_PASSWORD_PERMISSION, \
        EDIT_SECURITY_PERMISSION, MAIL_PASSWORD_PERMISSION, \
        ADD_MEMBER_PERMISSION
from AccessControl import ModuleSecurityInfo
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

MemberOfPublic_schema = BaseSchema.copy() + \
    getattr(BungeniMember, 'schema', Schema(())).copy() + \
    BaseMember.schema.copy() + \
    ExtensibleMetadata.schema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class MemberOfPublic(BaseContent, BaseMember, BrowserDefaultMixin, BungeniMember):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IMemberOfPublic)

    meta_type = 'MemberOfPublic'
    _at_rename_after_creation = True

    schema = MemberOfPublic_schema

    base_archetype = BaseContent

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # A member's __call__ should not render itself, this causes recursion
    def __call__(self, *args, **kwargs):
        return self.getId()
        

    # Methods


registerType(MemberOfPublic, PROJECTNAME)
# end of class MemberOfPublic

##code-section module-footer #fill in your manual code here
##/code-section module-footer



