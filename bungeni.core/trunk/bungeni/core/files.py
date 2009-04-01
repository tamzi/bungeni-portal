import os
from os import path
from datetime import date

from zope import interface, component
from zope.publisher.interfaces import NotFound
from zope.security.proxy import removeSecurityProxy
from zope.location.interfaces import ILocation

from sqlalchemy import orm
from ore.alchemist import Session
from ore.svn import SubversionContext
from ore.svn.directory import SubversionDirectory
from ore.metamime.interfaces import IMimeClassifier
from ore.metamime.hachoir import HachoirFileClassifier, InputIOStream

from bungeni.core import interfaces
from bungeni.core.proxy import LocationProxy
from bungeni.models import schema as dbschema

def fileClassifierSubscriber( ob, event ):
    ob = removeSecurityProxy( ob )
    classifier = IMimeClassifier( ob )
    ob.mime_type = str( classifier.queryMimeType() )

class FileClassifier( HachoirFileClassifier ):

    def _stream( self ):
        return InputIOStream( self.context.open() )
    
def key( ob ):
    unwrapped = removeSecurityProxy( ob )
    mapper = orm.object_mapper( ob )
    primary_key = mapper.primary_key_from_instance( ob )[0]    
    return primary_key, unwrapped.__class__.__name__

class DefaultPathChooser( object ):

    interface.implements( interfaces.IFilePathChooser )
    
    def __init__( self, context ):
        self.context = context

    def path( self ):
        today = date.today()        
        segments = [ self.context.__class__.__name__.lower() ]
        segments.append( "%s-%s"%(today.year, today.month ) )
        segments.append( str( today.day ))
        pk, type_name = key( self.context )  
        segments.append( str( pk ) )
        segments.insert(0, "")
        path = '/'.join( segments )
	return path

class ContainedDirectory( SubversionDirectory ):
    interface.implements(ILocation)
    
    @classmethod
    def fromDirectory( cls, context, directory ):
        i = cls(directory.id, directory.svn_path, directory.__parent__ )
        i.context = directory.getSVNContext()
        i.__parent__ = context
        i.__name__ = 'files'
        return i
    
    def getSVNContext( self ):
        return self.context
    
class DirectoryLocation(object):
    """
    persistent adapter which specs the file location for a given object
    """
    def __init__(self, **kw):
        """docstring for __init__"""
        for k,v in kw.items():
            setattr(self,k,v)
    
    @property
    def directory( self ):
        repo = component.getUtility( interfaces.IVersionedFileRepository )
        directory = repo.get( self.repo_path )
        return ContainedDirectory.fromDirectory(self.context,  directory)
    
orm.mapper( DirectoryLocation, dbschema.directory_locations )        


def location( content ):
    """
    factory for a directory location
    """
    
    repo = component.getUtility( interfaces.IVersionedFileRepository )
    location = repo.location( content )

    if location:
        return location
    
    location = repo.new( content )
    return location


class _FileRepository( object ):
    
    interface.implements( interfaces.IVersionedFileRepository )
    context = None
        
    def location( self, context ):
        primary_key, object_type = key( context )
        location =  Session().query( DirectoryLocation ).filter_by(
            object_id = primary_key,
            object_type = object_type
            ).first()
        if location is not None:
            location.context = context
        return location
        
    def get( self, path ):
        # set to the most recent repository revision, if not currently
        # active.
        self.context.setRevision()
        try:
            return self.context.traverse( path )
        except KeyError:
            return self.context.traverse( path )
                
    def new( self, context, path=None ):
        if not path:
            path = interfaces.IFilePathChooser( context ).path()

        # Create a database relation to the content
        primary_key, object_type = key( context )
        location = DirectoryLocation( repo_path=path, 
                                      object_id = primary_key,
                                      object_type = object_type )
        Session().add( location )                                

        # Create the subversion path for the content
        directory, created = create_path( self.context.root, path )
        if created:
            self.context.getTransaction().commit()
            self.context.setRevision() # update to latest revision
        
        # Commit it
        location.context = context
        return location
                                
class DirectoryDescriptorTraversal( object ):
    """ traversal through directory descriptors named 'files'  """
    def __init__( self, context, request ):
        self.context = context
        self.request = request

    def publishTraverse( self, request, name ):
        if name == 'files':
            return self.context.files
        raise NotFound( self.context, name, request )

def create_path( root, path ):
    segments = path.split('/')
    directory = root
    created = False
    for s in segments:
        if s in directory:
            directory = directory[s]
        else:
            directory = directory.makeDirectory( s )
            created = True
    # attachments to versions (this may be translations) are 
    # stored in branches
    if not 'branches' in directory:
        branches = directory.makeDirectory( 'branches' )
    # attachments to original (head) is stored in trunk                
    if not 'trunk' in directory:
        trunk = directory.makeDirectory('trunk')        
    return directory, created
    
FileRepository = _FileRepository()


class _HeadFileRepository(_FileRepository ):
    """ File repository for the Head
    """
    def location( self, context ):        
        primary_key, object_type = key( context )
        location =  Session().query( DirectoryLocation ).filter_by(
            object_id = primary_key,
            object_type = object_type
            ).first()        
        if location is not None:
            location.repo_path = location.repo_path +'/trunk' 
            location.context = context
        return location

class _VersionFileRepository(_FileRepository ):
    """File repository for Versions 
    """
    def location( self, context ):
        head_ctx = context.head        
        primary_key, object_type = key( head_ctx )
        location =  Session().query( DirectoryLocation ).filter_by(
            object_id = primary_key,
            object_type = object_type
            ).first()        
        if location is not None:
            location.repo_path = location.repo_path +'/branches/' + str(context.version_id)
            location.context = context
        return location
    
    
    
def setupStorageDirectory( ):
    # we start in buildout/src/bungeni.core/bungeni/core
    # we end in buildout/parts/files    
    store_dir = __file__
    x = 0
    while x < 5:
        x += 1
        store_dir = path.split( store_dir )[0]
    store_dir = path.join( store_dir, 'parts', 'files')
    if path.exists( store_dir ):
        assert path.isdir( store_dir )
        assert path.exists( path.join( store_dir, 'format') )
    return store_dir

def setup( ):
    from ore.svn import repos
    storage = setupStorageDirectory()
    if os.path.exists( storage ):
        repo_context = SubversionContext( storage )
    else:
        repo_context = repos.create( storage )
    
    FileRepository.context = repo_context
