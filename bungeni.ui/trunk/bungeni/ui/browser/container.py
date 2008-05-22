# encoding: utf-8
#from alchemist.ui.container import ContainerListing
import alchemist.ui.container
from zope.security import proxy
from zc.table import  table

import pdb

class ContainerListing( alchemist.ui.container.ContainerListing ):
    
    def update(self):
        # order_by
        order_by = self.request.get('order_by', None)
        #start, limit = self.request.get('start',0), self.request.get('limit', 0)
        #self.batch = super( ContainerListing, self ).batch(order_by)  
        #self.context.batch =  
        #context = proxy.removeSecurityProxy( self.context )
        #query = context.query
        #query = query.order_by( order_by )
        #context.query = context._query.order_by ( order_by )              
        super( ContainerListing, self ).update()
        
    @property
    def formatter( self ):
        context = proxy.removeSecurityProxy( self.context )        
        order_by = self.request.get('order_by', None)       
        query=context._query
        if order_by:
            if order_by in context._class.c._data._list:
                query=query.order_by(order_by)            
            #pdb.set_trace()
            
        formatter = table.AlternatingRowFormatter( context,
                                                   self.request,
                                                   query,
                                                   prefix="form",
                                                   columns = self.columns )
        formatter.cssClasses['table'] = 'listing'
        formatter.table_id = "datacontents"
        return formatter        
        
        

        
              
