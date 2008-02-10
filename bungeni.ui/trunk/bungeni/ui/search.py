"""
User interface for Content Search


Todo - Canonical URL on index of results, tuple,
       AbsoluteURL adapter for results
       mark result class with interface
"""

import time
from alchemist.ui.core import BaseForm
from ore.xapian import interfaces

from zope import interface, schema, component
from zope.publisher.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.formlib import form
from zc.table import table, column
from bungeni.core.i18n import _

class ISearch( interface.Interface ):
    
    full_text = schema.TextLine( title=_("Query"), required=False)
        
class Search( BaseForm ):
    """  basic content search form and results
    """
    
    template = ViewPageTemplateFile('templates/search.pt')
    form_fields = form.Fields( ISearch )
    formatter_factory = table.StandaloneFullFormatter
    
    results = None 
    spelling_suggestion = None
    search_time = None
    doc_count = None
    
    columns = [
        column.GetterColumn( title=_(u"rank"), getter=lambda i,f:i.rank ),    
        column.GetterColumn( title=_(u"type"), getter=lambda i,f: i.data.get('object_type',('',))[0] ),
        column.GetterColumn( title=_(u"title"), getter=lambda i,f:i.data.get('title',('',))[0] ),
        column.GetterColumn( title=_(u"status"), getter=lambda i,f:i.data.get('status',('',))[0] ),        
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
        search_term = data[ 'full_text' ]

        # compose query
        t = time.time()
        query = searcher.query_parse( search_term )
        self.results = searcher.search( query, 0, 30)
        self.search_time = time.time()-t
        
        # spelling suggestions
        suggestion = searcher.spell_correct( search_term )
        self.spelling_suggestion = ( suggestion == search_term and None or suggestion )
        self.doc_count = searcher.get_doccount()
    
    @property
    def search_status( self ):
        return "Found %s Results in %s Documents in %0.5f Seconds"%( len(self.results), self.doc_count, self.search_time )
        
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


class Similiar( BrowserView ):
    
    results = None     

    def update( self ):
        resolver = component.getUtility( interfaces.IResolver )
        doc_id = resolver.id( self.context )
        
        searcher = component.getUtility( interfaces.IIndexSearch )()
        query = searcher.query_similiar( doc_id )
        
        # similarity includes original doc      
        # grab first fifteen matching  
        results = searcher.search( query, 0, 15)
        
    def render( self ):
        return ''
    
    def __call__( self ):
        self.update()
        return self.render()