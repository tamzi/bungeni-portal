from zope import interface, schema, lifecycleevent
from zope.component.interfaces import IObjectEvent, ObjectEvent
from zope.app.container.interfaces import IContainer

from bungeni.models.interfaces import IVersion
import ore.workflow.interfaces


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

#####################
# Versioned Object Interfaces
#     
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

class IFilePathChooser( interface.Interface ):

    def path( ):
        """
        return the path to store a context's files within the repo 
        """        

########################
# Versioned Files

class IVersionedFileRepository( interface.Interface ):

    def locations( context ):
        """
        get all the directory locations for this content
        """

    def new( context, path=None):
        """create a new directory location for context
        """
        
    def get( path ):
        """
        fetch the versioned directory for the given repository
        path
        """
#class IStateWorkflowInfo (ore.workflow.interfaces.IWorkflowInfo):
#    """
#    subclass IWorkflowInfo so that it implements security states
#    """        
    
