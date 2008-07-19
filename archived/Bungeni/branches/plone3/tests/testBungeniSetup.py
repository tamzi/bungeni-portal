# -*- coding: utf-8 -*-
#
# File: testBungeniSetup.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 2.0-beta5
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Jean Jordaan <jean.jordaan@gmail.com>"""
__docformat__ = 'plaintext'

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

##code-section module-header #fill in your manual code here
##/code-section module-header

#
# Setup tests
#

import os, sys
from Testing import ZopeTestCase
from Products.Bungeni.tests.testBungeni import testBungeni

class testBungeniSetup(testBungeni):
    """Test cases for the generic setup of the product."""

    ##code-section class-header_testBungeniSetup #fill in your manual code here
    ##/code-section class-header_testBungeniSetup

    def afterSetUp(self):
        ids = self.portal.objectIds()

    def test_tools(self):
        ids = self.portal.objectIds()
        self.failUnless('archetype_tool' in ids)
        # []
    def test_types(self):
        ids = self.portal.portal_types.objectIds()
        self.failUnless('Document' in ids)

    def test_skins(self):
        ids = self.portal.portal_skins.objectIds()
        self.failUnless('plone_templates' in ids)

    def test_workflows(self):
        ids = self.portal.portal_workflow.objectIds()
        self.failUnless('plone_workflow' in ids)

    def test_workflowChains(self):
        getChain = self.portal.portal_workflow.getChainForPortalType
        self.failUnless('plone_workflow' in getChain('Document'))

    # Manually created methods


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testBungeniSetup))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


