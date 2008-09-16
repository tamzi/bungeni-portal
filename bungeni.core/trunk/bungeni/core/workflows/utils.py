from zope.security.proxy import removeSecurityProxy

from bungeni.core.interfaces import IVersioned

import dbutils

def createVersion(info, context):
    """Create a new version of an object and return it."""

    instance = removeSecurityProxy(context)
    versions = IVersioned(instance)
    versions.create('New version created upon workflow transition.')
    
def setQuestionDefaults(info, context):
    """get the default values for a question.
    current parliament, ... """ 
    instance = removeSecurityProxy(context)
    dbutils.setQuestionParliamentId(instance)
           

        
