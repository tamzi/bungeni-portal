import os
from os import path
from datetime import date

from zope import interface, component
from zope.publisher.interfaces import NotFound
from zope.security.proxy import removeSecurityProxy

from sqlalchemy import orm
from ore.alchemist import Session
from ore.svn import SubversionContext
from ore.svn.directory import SubversionDirectory
from ore.metamime.interfaces import IMimeClassifier
from ore.metamime.hachoir import HachoirFileClassifier, InputIOStream

from bungeni.core import interfaces, schema as dbschema


def fileClassifierSubscriber( ob, event ):
    from zope.security.proxy import removeSecurityProxy
    ob = removeSecurityProxy( ob )
    classifier = IMimeClassifier( ob )
    ob.mime_type = str( classifier.queryMimeType() )

class FileClassifier( HachoirFileClassifier ):

    def _stream( self ):
        return InputIOStream( self.context.open() )
    
class DefaultPathChooser( object ):

    interface.implements( interfaces.IFilePathChooser )
    
    def __init__( self, context ):
        self.context = context

    def path( self ):
        today = date.today()        
        segments = [ self.context.__class__.__name__.lower() ]
        segments.append( "%s-%s"%(today.year, today.month ) )
        segments.append( str( today.day ))
        segments.insert(0, "")
        return '/'.join( segments )

class DirectoryDescriptor( object ):
    """
    you can place this on a content object to get easy access to its files.
    
    class foo( object ):
        
        attachments = DirectoryDescriptor()
        
    file = foo().attachments.makeFile('rabbits.txt')
    file.contents = "Hello World"

    you can then traverse to the file via
    
      base_url/foo_name/attachments/rabbits.txt
      
    # streaming interface also available see ore.svn docs
    """
        
    # assumes one directory per content context

    def __get__( self, instance, owner):
        if instance is None:
            raise AttributeError
        directory = interfaces.IDirectoryLocation( instance ).directory
        interface.directlyProvides( directory, interfaces.IProxiedDirectory )
        return directory

class DirectoryDescriptorTraversal( object ):
    """ traversal to directories  """
    def __init__( self, context, request ):
        self.context = context
        self.request = request

    def publishTraverse( self, request, name ):
        if name == 'files':
            return self.context.files
        raise NotFound( self.context, name, request )

class ContainedDirectory( SubversionDirectory ):

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
        return ContainedDirectory.fromDirectory( self.context,  repo.get( self.repo_path ) )    

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
        unwrapped = removeSecurityProxy( context )
        mapper = orm.object_mapper( unwrapped )
        primary_key = mapper.primary_key_from_instance( unwrapped )[0]

        location =  Session().query( DirectoryLocation ).filter_by(
            object_id = primary_key,
            object_type = unwrapped.__class__.__name__
            ).first()

        if location is not None:
            location.context = context
        return location
        
    def get( self, path ):
        return self.context.traverse( path )
                
    def new( self, context, path=None ):
        if not path:
            path = interfaces.IFilePathChooser( context ).path()

        # Create a database relation to the content
        unwrapped = removeSecurityProxy( context )            
        mapper = orm.object_mapper( unwrapped )
        primary_key = mapper.primary_key_from_instance( unwrapped )[0]            
    
        location = DirectoryLocation( repo_path=path, 
                                      object_id = primary_key,
                                      object_type = unwrapped.__class__.__name__ )
        Session().save( location )                                

        # Create the subversion path for the content
        create_path( self.context.root, path )
        self.context.getTransaction().commit()
        
        # Commit it
        location.context = context
        return location
                                

def create_path( root, path ):
    segments = path.split('/')
    directory = root
    for s in segments:
        if s in directory:
            directory = directory[s]
        else:
            directory = directory.makeDirectory( s )
    return directory
    
FileRepository = _FileRepository()

def setupStorageDirectory( ):
    # we start in buildout/src/bungeni.core/bungeni/core
    # we end in buildout/parts/index    
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
