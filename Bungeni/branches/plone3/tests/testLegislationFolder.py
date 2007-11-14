# -*- coding: utf-8 -*-
#
# File: testLegislationFolder.py
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
# Test-cases for class(es) LegislationFolder
#

from Testing import ZopeTestCase
from Products.Bungeni.config import *
from Products.Bungeni.tests.testBungeni import testBungeni

# Import the tested classes
from Products.Bungeni.bills.LegislationFolder import LegislationFolder

##code-section module-beforeclass #fill in your manual code here
##/code-section module-beforeclass


class testLegislationFolder(testBungeni):
    """Test-cases for class(es) LegislationFolder."""

    ##code-section class-header_testLegislationFolder #fill in your manual code here
    ##/code-section class-header_testLegislationFolder

    def afterSetUp(self):
        pass

    # from class LegislationFolder:
    def test_PUT_factory(self):
        pass

    # Manually created methods


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testLegislationFolder))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


