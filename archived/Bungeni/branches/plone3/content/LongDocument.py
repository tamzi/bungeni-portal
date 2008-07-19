# -*- coding: utf-8 -*-
#
# File: LongDocument.py
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
from Products.PloneHelpCenter.content.ReferenceManual import HelpCenterReferenceManual
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

LongDocument_schema = BaseFolderSchema.copy() + \
    getattr(HelpCenterReferenceManual, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class LongDocument(BaseFolder, HelpCenterReferenceManual, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ILongDocument)

    meta_type = 'LongDocument'
    _at_rename_after_creation = True

    schema = LongDocument_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declareProtected(permissions.View, 'getTOC')
    def getTOC(self, current=None, root=None):
        """ See HelpCenterReferenceManual.getTOC for documentation.
        We're only overriding the query.
        """
        if not root:
            root = self

        class Strategy(NavtreeStrategyBase):

            rootPath = '/'.join(root.getPhysicalPath())
            showAllParents = False

        strategy = Strategy()
        # Custom query for Bungeni:
        query=  {'path'        : '/'.join(root.getPhysicalPath()),
                 'portal_type' : ('LongDocumentSection', 'LongDocumentPage',),
                 'sort_on'     : 'getObjPositionInParent'}

        toc = buildFolderTree(self, current, query, strategy)['children']

        def buildNumbering(nodes, base=""):
            idx = 1
            for n in nodes:
                numbering = "%s%d." % (base, idx,)
                n['numbering'] = numbering
                buildNumbering(n['children'], numbering)
                idx += 1

        buildNumbering(toc)
        return toc


registerType(LongDocument, PROJECTNAME)
# end of class LongDocument

##code-section module-footer #fill in your manual code here
##/code-section module-footer



