"""
$Id: $
"""

from zope import interface
from zope import component

from zope.testing import doctest, doctestunit
from zope.configuration import xmlconfig

import unittest
import bungeni.core.tests
import time
import transaction

from ore.xapian import queue

zcml_slug = """
<configure xmlns="http://namespaces.zope.org/zope"
           xmlns:db="http://namespaces.objectrealms.net/rdb">

  <include package="bungeni.core" file="ftesting.zcml" />

</configure>
"""

def setUp( test ):
    queue.QueueProcessor.FLUSH_TIMEOUT = 0.1
    queue.QueueProcessor.FLUSH_THRESHOLD = 1  
    bungeni.core.tests.setUp(test)
    xmlconfig.string(zcml_slug)
    
def tearDown( test ):
    bungeni.core.tests.tearDown(test)

    # stop indexing queue
    queue.QueueProcessor.stop()
    sleep(1.0)

def test_suite():
    doctests = ('viewlets/viewlets.txt',)
    
    globs = dict(interface=interface,
                 component=component, time=time,
                 transaction=transaction)
    
    return unittest.TestSuite((
        doctestunit.DocFileSuite(filename,
                                 setUp = setUp,
                                 tearDown = tearDown,
                                 globs = globs,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS
                                 ) for filename in doctests
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
