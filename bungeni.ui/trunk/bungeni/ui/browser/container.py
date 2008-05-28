# encoding: utf-8
from ore.alchemist.model import queryModelDescriptor
import alchemist.ui.container
import datetime

from zope.security import proxy
from zc.table import  table
from bungeni.ui.utils import getDisplayDate, getFilter


def dateFilter( request ):
    filter_by = ''
    displayDate = getDisplayDate(request)
    
    if displayDate:
        filter_by = getFilter( displayDate )
    else:
        filter_by = ''          
    return filter_by            





class ContainerListing( alchemist.ui.container.ContainerListing ):
    
    def update(self):           
        super( ContainerListing, self ).update()
        
    @property
    def formatter( self ):
        context = proxy.removeSecurityProxy( self.context )        
        order_by = self.request.get('order_by', None)       
        query=context._query
        order_list=[]
        if order_by:
            if order_by in context._class.c._data._list:
                order_list.append(order_by)
        default_order = getattr(context._class,'sort_on',None)
        if default_order:
            #define your default in bungeni.core.domain
            if default_order in  context._class.c._data._list:
                order_list.append(default_order)                            
        if 'short_name' in  context._class.c._data._list and 'short_name' not in order_list:
            #default order and secondary sort is on short_name
            order_list.append('short_name')             
        filter_by = dateFilter( self.request )
        if filter_by:  
            if 'start_date' in  context._class.c._data._list and 'end_date' in  context._class.c._data._list:                 
                query=query.filter(filter_by).order_by(order_list)                           
        else:            
            query=query.order_by(order_list)                                                            
        formatter = table.AlternatingRowFormatter( context,
                                                   self.request,
                                                   query,
                                                   prefix="form",
                                                   columns = self.columns )
        formatter.cssClasses['table'] = 'listing'
        #formatter.cssClasses['tbody'] = 'scrollingtable'
        formatter.table_id = "datacontents"
        return formatter        
        
        
    @property
    def form_name( self ):
        descriptor = queryModelDescriptor( self.context.domain_model )
        if descriptor:
            name = getattr( descriptor, 'display_name', None)
        if not name:
            name = getattr( self.context.domain_model, '__name__', None)                
        return "%s %s"%(name, self.mode.title())

        

