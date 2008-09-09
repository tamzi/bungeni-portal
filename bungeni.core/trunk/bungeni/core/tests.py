"""
$Id: $
"""

from zope import interface
from zope import component

import unittest

from zope.testing import doctest, doctestunit
from zope.app.testing import placelesssetup, ztapi
from zope.configuration import xmlconfig

from bungeni.core import metadata, interfaces

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

  <db:bind
     engine="bungeni-db"
     metadata="alchemist.security.metadata" />     

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

def assignment_tests( ):
    import assignment
    def _setUp( test ):
        setUp( test )
        ztapi.provideAdapter( (interfaces.IBungeniContent, interfaces.IBungeniGroup ),
                              interfaces.IAssignmentFactory,
                              assignment.GroupAssignmentFactory )

        ztapi.provideAdapter( interfaces.IBungeniContent,
                              interfaces.IContentAssignments,
                              assignment.ContentAssignments )

        ztapi.provideAdapter( interfaces.IBungeniGroup,
                              interfaces.IContextAssignments,
                              assignment.GroupContextAssignments )
        
    return doctestunit.DocFileSuite('assignment.txt',
                                    setUp = _setUp,
                                    tearDown = tearDown,
                                    optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS
                                    )

    

def test_suite():
    doctests = ('readme.txt', 
                'notification.txt', 
                #'assignment.txt',
                'workflows/question.txt', 
                'workflows/motion.txt',
                'workflows/bill.txt')
    #doctests = ()#('assignment.txt',)
    globs = dict(interface=interface, component=component)

    test_suites = []
    for filename in doctests:
        test_suite = doctestunit.DocFileSuite(filename,
                                              setUp = setUp,
                                              tearDown = tearDown,
                                              globs = globs,
                                              optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS )
        test_suites.append( test_suite )
        
    test_suites.append( assignment_tests() )
    
    return unittest.TestSuite( test_suites )

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')


