# -*- coding: utf-8 -*-
#
# File: BungeniMembershipTool.py
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

# additional imports from tagged value 'import'
from Products.Archetypes.utils import DisplayList
from Products.remember.utils import getRememberTypes


from Products.CMFCore.utils import UniqueObject

    
##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    LinesField(
        name='MemberTypesWithHomeFolders',
        widget=MultiSelectionWidget(
            label='Membertypeswithhomefolders',
            label_msgid='Bungeni_label_MemberTypesWithHomeFolders',
            i18n_domain='Bungeni',
        ),
        multiValued=1,
        vocabulary='getMemberTypesVocab'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

BungeniMembershipTool_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class BungeniMembershipTool(UniqueObject, BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IBungeniMembershipTool)

    meta_type = 'BungeniMembershipTool'
    _at_rename_after_creation = True

    schema = BungeniMembershipTool_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # tool-constructors have no id argument, the id is fixed
    def __init__(self, id=None):
        BaseContent.__init__(self,'portal_bungenimembershiptool')
        self.setTitle('')
        
        ##code-section constructor-footer #fill in your manual code here
        ##/code-section constructor-footer


    # tool should not appear in portal_catalog
    def at_post_edit_script(self):
        self.unindexObject()
        
        ##code-section post-edit-method-footer #fill in your manual code here
        ##/code-section post-edit-method-footer


    # Methods

    security.declarePublic('getMemberTypesVocab')
    def getMemberTypesVocab(self):
        """ Get a displaylist of remember-based member types.
        """
        remtypes = getRememberTypes(self)
        remtypes.sort()
        remtypes = [(i, i) for i in remtypes]
        return DisplayList(remtypes)

    security.declarePublic('getMemberByUID')
    def getMemberByUID(self,uid):
        """
        """
        proxies = self.uid_catalog(UID=uid)
        if proxies:
            assert len(proxies) == 1
            member = proxies[0].getObject()
            return member


registerType(BungeniMembershipTool, PROJECTNAME)
# end of class BungeniMembershipTool

##code-section module-footer #fill in your manual code here
##/code-section module-footer



