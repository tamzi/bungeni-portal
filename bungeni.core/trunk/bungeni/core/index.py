"""
xapian indexing adapters
"""

from zope import interface
from ore.xapian import interfaces

class MotionIndexer( object ):

    interface.implements( interfaces.IIndexer )

    def __init__(self, context):
        self.context = context
        
    def index( self, connection):
        
        
    
    