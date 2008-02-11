
from zope import interface, schema, lifecycleevent
from zope.component.interfaces import IObjectEvent, ObjectEvent
from zope.app.container.interfaces import IContainer
from ore.wsgiapp.interfaces import IApplication
from ore.xapian.interfaces import IIndexable

class IBungeniApplication( IApplication ):
    """
    Bungeni Application
    """

####################
# Feature - Marker Interfaces 
# 
# declare implemented to apply feature to a domain model

class IAuditable( interface.Interface ):
    """
    marker interface to apply auditing/object log feature
    """

class ISubscribable( interface.Interface ):
    """
    marker interface to add a subscription to an object
    """
    
class IVersionable( interface.Interface ):
    """
    marker interface to apply versioning feature ( requires iauditable / object log)
    """
    
class IVersioned( IContainer ):
    """ a versioning system interface to an object, versioned is a container
        of versions.
    """    

    def create( ):
        """
        store the existing state of the adapted context as a new version
        """
        
    def revert( version ):
        """
        revert the current state of the adapted object to the values specified
        in version.
        """
        
class IVersion( interface.Interface ):
    """
    a version of an object is identical in attributes to the actual object, based
    on that object's domain schema
    """
    

class IVersionEvent( IObjectEvent ):
    """
    a versioning event
    """
    
    versioned = schema.Object( IVersioned )
    version = schema.Object( IVersion )    
    message = schema.Text(description=u"Message accompanying versioning event")
    
class VersionEvent( ObjectEvent ):
    """
    """
    interface.implements( IVersionEvent )

    def __init__( self, object, versioned, version, msg ):
        self.object = object
        self.versioned = versioned
        self.version = version
        self.message = msg
        
class IVersionCreated( IVersionEvent ):
    """
    a new version was created
    """

class VersionCreated( VersionEvent ):
    
    interface.implements( IVersionCreated )

class IVersionReverted( IVersionEvent, lifecycleevent.IObjectModifiedEvent ):
    """
    the context version was reverted
    """
    
class VersionReverted( VersionEvent ):
    
    interface.implements( IVersionReverted )
    
    descriptions = ()
    
class IBungeniUser( interface.Interface ):
    """
    a user in bungeni
    """     
    
class IBungeniGroup( interface.Interface ):
    """
    a group in bungeni
    """

class IBungeniContent( IIndexable, IAuditable, IVersionable ):
    """
    parliamentary content
    """

class IBungeniSetup( interface.Interface ):

    def setUp( app ):
        """
        setup the application on server start
        """
        


    
    
