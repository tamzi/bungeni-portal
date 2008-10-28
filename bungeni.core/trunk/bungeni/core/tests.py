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


def file_setup( ):
    import files
    files_store = files.setupStorageDirectory()
    if files_store.endswith('test'):
        return
    
    def setupStorageDirectory( ):
        return files_store + '-test'
    files.setupStorageDirectory = setupStorageDirectory
    
def file_tests( ):
    file_setup()
    def _setUp( test ):
        setUp( test )
        import files
        files.setup()
        
        ztapi.provideUtility( interfaces.IVersionedFileRepository, component=files.FileRepository )

        ztapi.provideAdapter( interfaces.IBungeniContent,
                              interfaces.IDirectoryLocation,
                              files.location )

        ztapi.provideAdapter( interfaces.IBungeniContent,
                              interfaces.IFilePathChooser,
                              files.DefaultPathChooser )

    def _tearDown( test ):
        import files, shutil
        files.FileRepository.context.clear()
        dir = files.setupStorageDirectory()
        shutil.rmtree( dir )
        tearDown( test )        

    return doctestunit.DocFileSuite('files.txt',
                                    setUp = _setUp,
                                    tearDown = _tearDown,
                                    optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS
                                    )

def test_suite():

    doctests = ('readme.txt', 
                'audit.txt',
                'settings.txt',
                'workflows/questionnotification.txt', 
                'workflows/motionnotification.txt',                 
                'workflows/question.txt',
                'workflows/response.txt',               
                'workflows/motion.txt',
                'workflows/bill.txt',
                'workflows/dbutils.txt',
                'workflows/transitioncron.txt',                
                )
    
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
    test_suites.append( file_tests() )

    
    return unittest.TestSuite( test_suites )

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')


