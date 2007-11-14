# -*- coding: utf-8 -*-
#
# File: testBill.py
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
# Test-cases for class(es) Bill
#

from Testing import ZopeTestCase
from Products.Bungeni.config import *
from Products.Bungeni.tests.testBungeni import testBungeni

# Import the tested classes
from Products.Bungeni.bills.Bill import Bill

##code-section module-beforeclass #fill in your manual code here
##/code-section module-beforeclass


class testBill(testBungeni):
    """Test-cases for class(es) Bill."""

    ##code-section class-header_testBill #fill in your manual code here
    ##/code-section class-header_testBill

    def afterSetUp(self):
        pass

    # from class Bill:
    def test_getTOC(self):
        pass

    # Manually created methods


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testBill))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


