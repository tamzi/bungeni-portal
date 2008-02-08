"""
User interface for Content Versioning.
"""
from alchemist.ui.core import BaseForm
from zope import interface, schema
from zope.security.proxy import removeSecurityProxy
from zope.formlib import form

from bungeni.core.interfaces import IVersioned
from bungeni.core.i18n import _

class IVersionEntry( interface.Interface ):
    
    commit_message = schema.Text(title=_("Change Message") )
    

class VersionLog( BaseForm ):
    """  
    """
    form_fields = form.Fields()
    
    def setUpWidgets( self, ignore_request=False):
        # setup widgets in data entry mode not bound to context
        self.adapters = {}
        self.widgets = form.setUpDataWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            ignore_request = ignore_request )
                
    @form.action(label=_("New Version") )
    def handle_new_version( self, action, data ):
        self._versions.create( message = data['commit_message'] )        
        
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
