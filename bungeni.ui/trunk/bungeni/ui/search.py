"""
User interface for Content Search
"""
from alchemist.ui.core import BaseForm

from zope import interface, schema
from zope.formlib import form

from bungeni.core.i18n import _

class ISearch( interface.Interface ):
    
    full_text = schema.TextLine( title=_("Full Text")
    title = schema.TextLine( title=_("Title") )

class Search( BaseForm ):
    """  
    """
    
    form_fields = form.Fields( ISearch )
    
    def setUpWidgets( self, ignore_request=False):
        # setup widgets in data entry mode not bound to context
        self.adapters = {}
        self.widgets = form.setUpDataWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            ignore_request = ignore_request )
                
    @form.action(label=_("Search") )
    def handle_search( self, action, data ):
        print data
        
