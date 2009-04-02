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

    def __getitem__(self, key):
        item = super(ContainedDirectory, self).__getitem__(key)
        interface.alsoProvides(item, ILocation)
        return item
    
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
        #import pdb; pdb.set_trace()
        return ContainedDirectory.fromDirectory(self.context,  directory)
    
orm.mapper( DirectoryLocation, dbschema.directory_locations )        


class HeadDirectoryLocation( DirectoryLocation ):
    """ Adapter for head - trunk directory of svn
    """
    
    @property
    def directory( self ):
        repo = component.getUtility( interfaces.IVersionedFileRepository )
        directory = repo.get( self.repo_path + '/trunk' )
        #import pdb; pdb.set_trace()
        return ContainedDirectory.fromDirectory(self.context,  directory)

orm.mapper( HeadDirectoryLocation, dbschema.directory_locations )  

class BranchDirectoryLocation( DirectoryLocation ):
    """ Adapter for branches - versions of content
    """
    @property
    def directory( self ):
        repo = component.getUtility( interfaces.IVersionedFileRepository )
        directory = repo.get( self.repo_path + '/branches' )
        import pdb; pdb.set_trace()
        if str(self.context.version_id) in directory.keys():
            directory = directory[str(self.context.version_id)] 
        else:            
            directory = directory.makeDirectory( str(self.context.version_id))    
            repo.context.getTransaction().commit()
            repo.context.setRevision()                                       
        return ContainedDirectory.fromDirectory(self.context,  directory)

orm.mapper( BranchDirectoryLocation, dbschema.directory_locations )  

def location( content, cls, context ):
    """
    factory for a directory location
    """
    
    repo = component.getUtility( interfaces.IVersionedFileRepository )
    location = repo.location( content, cls, context )

    if location:        
        return location
    else:
        location = repo.new( content )
        location = repo.location( content, cls, context )
        return location


def headlocation( context ):
    return location(context, HeadDirectoryLocation, context )
    
def branchlocation( context ):
    content = context.head
    import pdb; pdb.set_trace()
    return location(content, BranchDirectoryLocation, context )
        

class _FileRepository( object ):
    
    interface.implements( interfaces.IVersionedFileRepository )
    context = None
        
    def location( self, content, cls, context ):
        primary_key, object_type = key( content )
        location =  Session().query( cls ).filter_by(
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
            create_path( self.context.root, path )
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
            # attachments to versions (this may be translations) are 
            # stored in branches
            if not 'branches' in directory:
                branches = directory.makeDirectory( 'branches' )
            # attachments to original (head) is stored in trunk                
            if not 'trunk' in directory:
                trunk = directory.makeDirectory('trunk')        
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
        session = Session()
        if name == 'files':
            context = removeSecurityProxy( self.context)
            return context.files
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
    return directory, created
 
# utility that provides IVersionedFileRepository:    
FileRepository = _FileRepository()



      
    
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
