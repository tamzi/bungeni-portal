import unittest

from Products.PloneTestCase import PloneTestCase
from bungeni.marginalia.interfaces import IMarginaliaTool
from zope.testbrowser.browser import Browser
from Testing import ZopeTestCase as ztc
from zope.testing import doctest



PloneTestCase.setupPloneSite(
    extension_profiles=('bungeni.marginalia:default',))

class MarginaliaTestCase(PloneTestCase.PloneTestCase):

    def testToolInstalled(self):
        tool = self.portal.portal_marginalia
        self.failUnless(IMarginaliaTool.providedBy(tool))

    def testCatalogInstalled(self):
        self.failUnless('marginalia_catalog' in self.portal.objectIds())

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(MarginaliaTestCase))
    suite.addTest(
        ztc.FunctionalDocFileSuite(
            'browser.txt',
            package="bungeni.marginalia",
            test_class=PloneTestCase.FunctionalTestCase,
            ))

    return suite




