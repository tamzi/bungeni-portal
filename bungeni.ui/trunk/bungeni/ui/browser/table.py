# encoding: utf-8

from ore.yuiwidget.table import BaseDataTableFormatter
import container
from zope.traversing.browser import absoluteURL
from zope.security import proxy
import pdb

class ContextDataTableFormatter( BaseDataTableFormatter ):
    data_view ="/@@jsonlisting"
    prefix = "listing"
    
    def __init__( self, context, request, items,  paginator=None, data_view=None, *args, **kw ):
        if paginator:
            self.paginator = paginator
        if data_view:
            self.data_view = data_view  
        else:
            self.data_view = "/@@jsonlisting" #%  context.__name__ #absoluteURL( context, request )            
        super( ContextDataTableFormatter, self).__init__( context, request, items, self.paginator, self.data_view, *args, **kw )                      
        #pdb.set_trace()
        
    def getFields( self ):
        return container.getFields( self.context )


class AjaxContainerListing( container.ContainerListing ):
    formatter_factory = ContextDataTableFormatter

    @property
    def formatter( self ):
        context = proxy.removeSecurityProxy( self.context )
        prefix= "container_contents_" + context.__name__
        formatter = self.formatter_factory( context,
                                            self.request,
                                            (),
                                            prefix=prefix,
                                            columns = self.columns )
        formatter.cssClasses['table'] = 'listing'
        formatter.table_id = "datacontents"
        return formatter

    
