from zope import interface

from bungeni.models import interfaces

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


