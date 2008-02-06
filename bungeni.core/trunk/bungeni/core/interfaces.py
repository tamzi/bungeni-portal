
from zope import interface, schema
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
        


    
    
