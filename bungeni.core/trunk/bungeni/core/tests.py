"""
$Id: $
"""

from zope import interface
from zope import component

import unittest

from zope.testing import doctest, doctestunit
from zope.app.testing import placelesssetup
from zope.configuration import xmlconfig
from bungeni.core import metadata

zcml_slug = """
<configure xmlns="http://namespaces.zope.org/zope"
           xmlns:db="http://namespaces.objectrealms.net/rdb">

  <include package="ore.alchemist" file="meta.zcml"/>
  <include package="alchemist.catalyst" file="meta.zcml"/>

  <!-- Setup Database Connection -->
  <db:engine
     name="bungeni-db"
     url="postgres://localhost/bungeni-test"
     />
     
  <db:bind
     engine="bungeni-db"
     metadata="bungeni.core.metadata" />

  <!-- Setup Core Model --> 
  <include package="bungeni.core" file="catalyst.zcml"/>
 
</configure>
"""

def setUp( test ):
    placelesssetup.setUp()
    xmlconfig.string( zcml_slug )
    metadata.create_all( checkfirst=True )
    
def tearDown( test ):
    placelesssetup.tearDown()
    metadata.drop_all( checkfirst=True )

def test_suite():
    doctests = ('readme.txt', 'workflows/question.txt')

    globs = dict(interface=interface, component=component)
    
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


