"""Skin Resource Directory

a skin resource directory walks through a stack of layers to find a named resource 

$Id: $
"""

from zope import interface, component
from zope.publisher.interfaces import NotFound

from zope.app.publisher.directoryresource import DirectoryResource, Directory, _marker

import interfaces

class RequestWrapper( object ):
    __slots__ = ('request',)
    
    def __init__( self, request ):
        self.request = request
    def __getattr__( self, name):
        return getattr( self.request, name )
    def __setattr__( self, name, value):
        setattr( self.request, name)
        
class SkinDirectory(DirectoryResource):

    interface.implements( interfaces.ISkinDirectory )

    layers = ()
        
    def get(self, name, default=_marker):
        value = super( SkinDirectory ).get( name, None)
        if value is not None:
            return value
        
        wrapper = RequestWrapper( self.request )
        
        for layer in self.layers:
            interface.directlyProvides( wrapper, layer )
            resource = component.queryAdapter(wrapper, name=name)
            if resource is not None:
                return resource
        raise NotFound( name )

class SkinDirectoryFactory(object):

    def __init__(self, path, checker, name, layers):
        self.__dir = Directory(path, checker, name)
        self.__checker = checker
        self.__name = name
        self.__layers = layers

    def __call__(self, request):
        resource = SkinDirectory(self.__dir, request)
        resource.layers = self.__layers
        resource.__Security_checker__ = self.__checker
        resource.__name__ = self.__name
        return resource