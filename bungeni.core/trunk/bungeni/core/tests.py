"""
$Id: $
"""

from zope import interface
from zope import component

import copy
import unittest
import datetime

from zope.testing import doctest, doctestunit
from zope.app.testing import placelesssetup, ztapi
from zope.configuration import xmlconfig

from bungeni.models import metadata
from bungeni.models.interfaces import IBungeniContent
from bungeni.models.interfaces import IDirectoryLocation
from bungeni.core.interfaces import IFilePathChooser
from bungeni.core.interfaces import IVersionedFileRepository

zcml_slug = """
<configure xmlns="http://namespaces.zope.org/zope"
           xmlns:db="http://namespaces.objectrealms.net/rdb">

  <include package="bungeni.core" file="ftesting.zcml" />
  
</configure>
"""

def setUp(test):
    placelesssetup.setUp()
    xmlconfig.string( zcml_slug )
    metadata.create_all( checkfirst=True )
    
def tearDown( test ):
    placelesssetup.tearDown()
    metadata.drop_all( checkfirst=True )

    import bungeni.models.domain
    import bungeni.models.schema
    import bungeni.models.orm
    import bungeni.ui.content
    
    # reload catalyzed modules
    reload(bungeni.ui.content)
    reload(bungeni.models.domain)
    reload(bungeni.models.schema)
    reload(bungeni.models.orm)
    reload(bungeni.models)

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
        
        ztapi.provideUtility( IVersionedFileRepository, component=files.FileRepository )

        ztapi.provideAdapter( IBungeniContent,
                              IDirectoryLocation,
                              files.location )

        ztapi.provideAdapter( IBungeniContent,
                              IFilePathChooser,
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
    from bungeni.core.app import BungeniApp

    doctests = ('audit.txt',
                'version.txt',                 
                'workflows/question.txt',
                'workflows/motion.txt',
                'workflows/bill.txt',
                'workflows/transitioncron.txt',
                )

    # set up global symbols for doctests
    today = datetime.date.today()
    globs = dict(
        interface=interface,
        component=component,
        copy=copy,
        app=BungeniApp(),
        today=today,
        yesterday=today-datetime.timedelta(1),
        daybeforeyesterday=today-datetime.timedelta(2),
        tomorrow=today+datetime.timedelta(1),
        dayat=today+datetime.timedelta(2)
        )

    test_suites = []
    for filename in doctests:
        test_suite = doctestunit.DocFileSuite(filename,
                                              setUp = setUp,
                                              tearDown = tearDown,
                                              globs = globs,
                                              optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS )
        test_suites.append( test_suite )
        
    test_suites.append( file_tests() )

    
    return unittest.TestSuite( test_suites )

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')


