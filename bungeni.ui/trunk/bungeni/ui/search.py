"""
User interface for Content Search
"""

from alchemist.ui.core import BaseForm
from ore.xapian import interfaces

from zope import interface, schema, component
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.formlib import form
from zc.table import table, column
from bungeni.core.i18n import _

class ISearch( interface.Interface ):
    
    full_text = schema.TextLine( title=_("Full Text"), required=False)
    title = schema.TextLine( title=_("Title"), required=False )

class Search( BaseForm ):
    """  content search form and results
    """
    
    form_fields = form.Fields( ISearch )
    template = ViewPageTemplateFile('templates/search.pt')
    formatter_factory = table.StandaloneFullFormatter
    
    results = None
    
    columns = [
        column.GetterColumn( title=_(u"type"), getter=lambda i,f: i.data.get('object_type','') ),
        column.GetterColumn( title=_(u"title"), getter=lambda i,f:i.data.get('title','') ),
        column.GetterColumn( title=_(u"rank"), getter=lambda i,f:i.rank ),
        column.GetterColumn( title=_(u"weight"), getter=lambda i,f:i.weight ),                
        column.GetterColumn( title=_(u"percent"), getter=lambda i,f:i.percent ),                        
        ]
    
    #selection_column = columns[0]
    
    def setUpWidgets( self, ignore_request=False):
        # setup widgets in data entry mode not bound to context
        self.adapters = {}
        self.widgets = form.setUpDataWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            ignore_request = ignore_request )
                
    @form.action(label=_("Search") )
    def handle_search( self, action, data ):
        searcher = component.getUtility( interfaces.IIndexSearch )()
        query = searcher.query_parse( data['title'])
        self.results = searcher.search( query, 0, 30)
        
    def listing( self ):
        columns = self.columns
        formatter = self.formatter_factory( self.context,
                                            self.request,
                                            self.results or (),
                                            prefix="results",
                                            visible_column_names = [c.name for c in columns],
                                            #sort_on = ( ('name', False)
                                            columns = columns )
        formatter.cssClasses['table'] = 'listing'
        return formatter()
