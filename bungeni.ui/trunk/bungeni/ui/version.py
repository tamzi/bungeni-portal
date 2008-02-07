"""
User interface for Content Versioning.
"""
from alchemist.ui.core import BaseForm

from zope.security.proxy import removeSecurityProxy
from zope.formlib import form

from bungeni.core.interfaces import IVersioned
from bungeni.core.i18n import _

class VersionLog( BaseForm ):
    """  
    """
    
    form_fields = form.Fields()
    
    @form.action(label=_("New Version") )
    def handle_new_version( self, action, data ):
        self._versions.create( message = data['message'] )        
        
    @form.action(label=_("Revert To") )
    def handle_revert_version( self, action, data):
        version = self._versions.get( data['version_id'])
        self._versions.revert( version )
        
    def getVersions( self ):
        return self._versions.values()
        
    @property
    def _versions( self ):
        instance = removeSecurityProxy( self.context )
        versions = IVersioned( instance )
        return versions
