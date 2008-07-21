
from zope import interface, schema, lifecycleevent
from zope.component.interfaces import IObjectEvent, ObjectEvent
from zope.app.container.interfaces import IContainer
from ore.alchemist.interfaces import IAlchemistContent
from ore.wsgiapp.interfaces import IApplication
from ore.xapian.interfaces import IIndexable
from i18n import _


ENABLE_LOGGING = True

class IBungeniApplication( IApplication ):
    """
    Bungeni Application
    """

class IBungeniAdmin( IContainer ):
    """
    Admin Container
    """

class IAdminUserContainer( interface.Interface ):
    pass

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

class IBungeniUser( IIndexable, interface.Interface ):
    """
    a user in bungeni
    """     
    
class IBungeniGroup( IIndexable, interface.Interface ):
    """
    a group in bungeni
    """

class IBungeniContent( IIndexable, IAuditable, IVersionable ):
    """
    parliamentary content
    """

class IQuestion( interface.Interface ):
    """ Parliamentary Question
    """

class IBill( interface.Interface ):
    """ Parliamentary Bill
    """

class IMotion( interface.Interface ):
    """ Parliamentary Motion
    """

class IBungeniSetup( interface.Interface ):

    def setUp( app ):
        """
        setup the application on server start
        """
        
#####################
# Version Interfaces
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

###############################
# Assignment Implementation
# 
class IAssignment( IAlchemistContent ):

    content = schema.Object( IAlchemistContent )
    context = schema.Object( IAlchemistContent )
    title = schema.TextLine(title=_(u"Name of the Assignment"))
    start_date = schema.Date(title=_(u"Start Date of the Assignment"))
    end_date = schema.Date(title=_(u"End Date of the Assignment"))    
    type = schema.TextLine(title=_(u"Assignment Type"), readonly=True)
    status = schema.TextLine(title=_(u"Status"), readonly=True)
    notes  = schema.Text( title=_(u"Notes"), description=_(u"Notes"))

class IContentAssignments( interface.Interface ):
    """ assignments of this content to different contexts""" 

    def __iter__(  ):
        """ iterate over assignments for this context """

class IContextAssignments( interface.Interface ):
    """ content assignments for the given context/group """
    
    def __iter__(  ):
        """ iterate over assignments for this context """

class IAssignmentFactory( interface.Interface ):
    """ assignment factory """
    
    def new( **kw ):
        """
        create a new assignment
        """
    
    
