from zope.interface import Interface

class ITranscribable(Interface):
    '''Transcribable Marker Interface'''
    
class ITranscript(Interface):
    '''Transcript Marker Interface'''

class IChange(Interface):
    """ Marker for Change (log table) """
    
class IVersion( Interface ):
    """
    a version of an object is identical in attributes to the actual object, based
    on that object's domain schema
    """
    
class IBungeniTranscriptsSitting(Interface):
    pass
    
class IBungeniTranscript(Interface):
    pass
