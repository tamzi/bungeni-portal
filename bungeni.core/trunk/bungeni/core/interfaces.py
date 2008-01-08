
from zope import interface, schema

from ore.wsgiapp.interfaces import IApplication

class IBungeniApplication( IApplication ):
    """
    Bungeni Application
    """

class IBungeniSetup( interface.Interface ):

    def setUp( app ):
        """
        setup the application on server start
        """
        


    
    
