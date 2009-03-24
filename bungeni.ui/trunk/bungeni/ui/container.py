# encoding: utf-8

import datetime
import zc.table
import simplejson
import sqlalchemy.sql.expression as sql

from zope.security import proxy
from zope.security import checkPermission
from zope.security.proxy import ProxyFactory
from zope.publisher.browser import BrowserView

from ore.alchemist import Session
from ore.alchemist.model import queryModelDescriptor
from ore.alchemist.model import queryModelInterface
from ore.alchemist.container import contained
from ore.alchemist.container import stringKey

from alchemist.ui import container
from bungeni.ui.utils import getDisplayDate
from bungeni.ui.utils import getFilter

def dateFilter( request ):
    filter_by = ''
    displayDate = getDisplayDate(request)
    
    if displayDate:
        filter_by = getFilter( displayDate )
    else:
        filter_by = ''          
    return filter_by            

def getFullPath( context):
    #BBB use absoluteURL
    """
    traverse up to get the full path
    """
    path = ''
    if context.__parent__:
        path =  getFullPath(context.__parent__) + path
    if context.__name__:
        path = path + context.__name__ + '/'
    if len(path) == 0:
        return '/'    
    return path       
    
def getFields( context ):
    """ get all fields that will be displayed 
    in a containerlisting 
    """
    domain_model = proxy.removeSecurityProxy( context.domain_model )
    domain_interface = queryModelInterface( domain_model )
    domain_annotation = queryModelDescriptor( domain_interface )   
    for column in  domain_annotation.listing_columns:   
        field = domain_interface[column]     
        yield field
             
def secured_iterator(permission, query, parent):
    for item in query:
        item.__parent__ = parent
        proxied = ProxyFactory(item)
        if checkPermission("zope.View", proxied):
            yield item

class ContainerListing(container.ContainerListing):
    @property
    def formatter( self ):
        """We replace the formatter in our superclass to set up column
        sorting.

        Default sort order is defined in the model class
        (``sort_on``); if not set, the table is ordered by the
        ``short_name`` column (also used as secondary sort order).
        """

        session = Session()
        context = proxy.removeSecurityProxy(self.context)
        model = context.domain_model
        
        query = session.query(model)
        table = query.table
        names = table.columns.keys()
        order_list = []
        
        order_by = self.request.get('order_by', None)
        if order_by:
            if order_by in names:
                order_list.append(order_by)

        default_order = getattr(model, 'sort_on', None)
        if default_order:
            if default_order in names:
                order_list.append(default_order)

        if 'short_name' in names and 'short_name' not in order_list:
            order_list.append('short_name')
            
        filter_by = dateFilter(self.request)
        if filter_by:  
            if 'start_date' in names and 'end_date' in names:
                query = query.filter(filter_by).order_by(order_list)
            else:
                query = query.order_by(order_list)
        else:
            query = query.order_by(order_list)

        query = secured_iterator("zope.View", query, self.context)
            
        formatter = zc.table.table.AlternatingRowFormatter(
            context, self.request, query, prefix="form", columns=self.columns)
        
        formatter.cssClasses['table'] = 'listing'
        formatter.table_id = "datacontents"
        return formatter        

    @property
    def form_name( self ):
        domain_model = proxy.removeSecurityProxy(self.context).domain_model
        descriptor = queryModelDescriptor(domain_model)
        if descriptor:
            name = getattr(descriptor, 'display_name', None)
        if not name:
            name = getattr(domain_model, '__name__', None)
        return name
        
class ContainerJSONTableHeaders( BrowserView ):

    def __call__( self ):
        fields = getFields( self.context)
        th = []
        for field in fields:
            th.append({'name':  field.__name__, 'title': field.title })       
        return simplejson.dumps( th )

class ContainerJSONListing( BrowserView ):
    """
    paging, batching, sorting, json contents of a container
    """
    
    def appendSort( self, sort_key, columns):
        if sort_key and ( sort_key in columns ):
            column = domain_model.c[sort_key]
            return column
        

    def getSort( self ):
        """ server side sort,
        @web_parameter sort - request variable for sort column
        @web_parameter dir  - direction of the sort, only once acceptable value 'desc'
        """
        columns = []
        default_sort = None
        sort_key, sort_dir = self.request.get('sort'), self.request.get('dir')
        domain_model = proxy.removeSecurityProxy( self.context.domain_model )
        # in the domain model you may replace the sort with another column
        if getattr(domain_model,'sort_replace',None):            
            if sort_key in domain_model.sort_replace.keys():
                sort_key = domain_model.sort_replace[sort_key] 
                #pdb.set_trace()                          
        # get sort in sqlalchemy form
        if sort_key and ( sort_key in domain_model.c ):
            #column = domain_model.c[sort_key]
            if sort_dir == 'desc':
                columns.append( sql.desc(sort_key) )
            else:
                columns.append( sort_key )
        if getattr(domain_model,'sort_on',None):
            if domain_model.sort_on in domain_model.c and domain_model.sort_on != sort_key:
                # if a default sort is defined append it here (this will also serve as secondary sort)
                default_sort = domain_model.sort_on
                columns.append( default_sort )
        if getattr(domain_model,'short_name',None):            
            if 'short_name' in domain_model.c and 'short_name' != sort_key and 'short_name' != default_sort:
                # last if it has a short name sort by that
                columns.append('short_name')
                        
        return columns
    
    def getOffsets( self ):
        nodes = []
        start, limit = self.request.get('start',0), self.request.get('limit', 25)
        try:
            start, limit = int( start ), int( limit )
            if not limit:
                limit = 100
        except ValueError:
            start, limit = 0, 100
        return start, limit 

    def _get_secured_batch( self, query, start, limit):    
        secured_query = secured_iterator("zope.View", query, self.context)
        nodes =[]
        for ob in secured_query:
            ob = contained( ob, self, stringKey(ob) )
            nodes.append(ob)
        self.set_size = len(nodes)    
        return nodes[start : start + limit]

    def getBatch( self, start=0, limit=20, order_by=None):
        context = proxy.removeSecurityProxy( self.context )    
        query=context._query            
        # fetch the nodes from the container
        filter_by = dateFilter( self.request )
        if filter_by:  
            if 'start_date' in  context._class.c and 'end_date' in  context._class.c :                 
                # apply date range resrictions
                query=query.filter(filter_by)
        #query = query.limit( limit ).offset( start )                
        if order_by:
            query = query.order_by( order_by )  
        nodes = self._get_secured_batch(query, start, limit)                                                  
        batch = self._jsonValues( nodes, self.fields, self.context )
        return batch


            

    def _jsonValues( self, nodes, fields, context):
        """
        filter values from the nodes to respresent in json, currently
        that means some footwork around, probably better as another
        set of adapters.
        """
        values = []
        domain_model = proxy.removeSecurityProxy( context.domain_model )
        domain_interface = queryModelInterface( domain_model )
        domain_annotation = queryModelDescriptor( domain_interface )
        
        for n in nodes:
            d = {}
            # field to dictionaries
            for field in fields:
                f = field.__name__
                getter = field.query
                for anno_field in domain_annotation.fields:
                    if anno_field.name == f:
                        if getattr(anno_field.listing_column, 'getter', None):
                            getter=anno_field.listing_column.getter
                            d[ f ] = v = getter( n , field)
                        else:
                            d[ f ] = v = field.query( n )    
                #d[ f ] = v = field.query( n )
                if isinstance( v, datetime.datetime ):
                    d[f] = v.strftime('%F %I:%M %p')
                elif isinstance( v, datetime.date ):
                    d[f] = v.strftime('%F')
                d['object_id'] =   stringKey(n)                
            values.append( d )
        return values
        
    def __call__( self ):
        self.set_size = 0
        self.fields = list( getFields( self.context )  )
        start, limit = self.getOffsets( )
        sort_clause = self.getSort()
        batch = self.getBatch( start, limit, sort_clause )
        #XXX does not work with filtered listings!
        # use the query instead        
        data = dict( length=self.set_size,
                     start=start,
                     recordsReturned=len(batch),
                     sort = self.request.get('sort'),
                     dir  = self.request.get('dir', "asc"),
                     nodes=batch )
        return simplejson.dumps( data )




