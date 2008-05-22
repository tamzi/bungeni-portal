# encoding: utf-8

import alchemist.ui.container
from zope.security import proxy
from zc.table import  table


class ContainerListing( alchemist.ui.container.ContainerListing ):
    
    def update(self):           
        super( ContainerListing, self ).update()
        
    @property
    def formatter( self ):
        context = proxy.removeSecurityProxy( self.context )        
        order_by = self.request.get('order_by', None)       
        query=context._query
        if order_by:
            if order_by in context._class.c._data._list:
                query=query.order_by(order_by)            
            
        formatter = table.AlternatingRowFormatter( context,
                                                   self.request,
                                                   query,
                                                   prefix="form",
                                                   columns = self.columns )
        formatter.cssClasses['table'] = 'listing'
        formatter.table_id = "datacontents"
        return formatter        
        
        

        
              
