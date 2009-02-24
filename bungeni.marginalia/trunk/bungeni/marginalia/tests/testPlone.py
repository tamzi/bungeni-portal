from Products.PloneTestCase import PloneTestCase

from bungeni.marginalia.interfaces import IMarginaliaTool

PloneTestCase.setupPloneSite(
    extension_profiles=('bungeni.marginalia:default',))

class MarginaliaTestCase(PloneTestCase.PloneTestCase):

    def testToolInstalled(self):
        tool = self.portal.portal_marginalia
        self.failUnless(IMarginaliaTool.providedBy(tool))

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(MarginaliaTestCase))
    return suite


