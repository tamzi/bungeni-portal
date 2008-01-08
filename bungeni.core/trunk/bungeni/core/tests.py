"""
$Id: $
"""

import unittest
import zope.interface

from zope.testing import doctest, doctestunit
from zope.app.testing import placelesssetup, ztapi

def setUp( test ):
    placelesssetup.setUp()

def tearDown( test ):
    placelesssetup.tearDown()

def test_suite():
    return unittest.TestSuite((
        doctestunit.DocFileSuite('readme.txt',
                                 setUp = setUp,
                                 tearDown = tearDown,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS
                                 ),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')


