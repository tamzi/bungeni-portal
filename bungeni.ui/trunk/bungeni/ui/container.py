# encoding: utf-8
import datetime

from zope.security import proxy
from zc.table import  table, column
from zope.formlib import form

from zope.publisher.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile

import simplejson
import sqlalchemy.sql.expression as sql
#from zope.app.securitypolicy.interfaces import IPrincipalRoleManager, IPrincipalRoleMap
from zope.securitypolicy.interfaces import IPrincipalRoleMap
from zope.security import canAccess, canWrite
from zope.security.proxy import ProxyFactory

from ore.alchemist.model import queryModelDescriptor, queryModelInterface
import alchemist.ui.container

from ore.alchemist.container import stringKey, contained
#from ore import yuiwidget
from zope.traversing.browser import absoluteURL

from bungeni.core.i18n import _
from bungeni.ui.utils import getDisplayDate, getFilter
import base64


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

def viewLink( item, formatter ):
    path = absoluteURL( formatter.context, formatter.request ) + '/'
    #path = getFullPath(formatter.context)
    return u'<a class="button-link" href="%s">View</a>'%( path + stringKey( item ) )

def editLink( item, formatter ):
    #path = getFullPath(formatter.context)
    path = absoluteURL( formatter.context, formatter.request ) + '/'
    return u'<a class="button-link" href="%s/edit">Edit</a>'%( path + stringKey( item ) )

def viewEditLinks( item, formatter ):
    return u'%s %s'%(viewLink( item, formatter), editLink( item, formatter ) )



class ContainerListing( alchemist.ui.container.ContainerListing ):
    #formatter_factory = yuiwidget.ContainerDataTableFormatter
    addLink = None

    def update( self ):
        super( ContainerListing, self).update()
        context = proxy.removeSecurityProxy( self.context )
        columns = alchemist.ui.core.setUpColumns( context.domain_model )
        columns.append(
            column.GetterColumn( title = _(u'Actions'),
                                 getter = viewEditLinks )
            )
        self.columns = columns
        self.actionUrl = '%s/' % ( absoluteURL( self.context, self.request ) )
        
        for role in self.getRoles():
            print role

        
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
        else:            
            query=query.order_by(order_list)     
        # self.formatter_factory    
        formatter = table.AlternatingRowFormatter( context,
                                                   self.request,
                                                   query,
                                                   prefix="form",
                                                   columns = self.columns )
        formatter.cssClasses['table'] = 'listing'
        formatter.table_id = "datacontents"
        return formatter        
        
        
    @property
    def form_name( self ):
        descriptor = queryModelDescriptor( self.context.domain_model )
        if descriptor:
            name = getattr( descriptor, 'display_name', None)
        if not name:
            name = getattr( self.context.domain_model, '__name__', None)                
        return name #"%s %s"%(name, self.mode.title())
        
    @form.action(_(u"Add") )
    def handle_add( self, action, data ):
        path = absoluteURL( self.context, self.request ) 
        addurl = '%s/add' %( path ) 
        self.request.response.redirect(addurl)


    def parents( self, ctx ):
          p = ctx.__parent__
          while p:
             yield p
             p = p.__parent__
          else:
            yield None                

    def nearest_prm( self, ctx ):
        prm = IPrincipalRoleMap( ctx, None )
        if prm: return prm        
        for p in self.parents( ctx ):
            try:
                prm = IPrincipalRoleMap( p, None )            
            except:
                prm = None                
            if prm: return prm
        #raise AttributeError("Invalid Containment Chain")
        print "Invalid Containment Chain"


    def getRoles(self):
        #XXX
        pn = self.request.principal.id
        grants = self.nearest_prm(self.context)
        roles = None
        if grants:
            roles = grants.getRolesForPrincipal(pn)
        return roles

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

    def getBatch( self, start=0, limit=20, order_by=None):
        context = proxy.removeSecurityProxy( self.context )    
        query=context._query            
        # fetch the nodes from the container
        filter_by = dateFilter( self.request )
        if filter_by:  
            if 'start_date' in  context._class.c and 'end_date' in  context._class.c :                 
                # apply date range resrictions
                query=query.filter(filter_by)
        query = query.limit( limit ).offset( start )                
        if order_by:
            query = query.order_by( order_by )  
        nodes = []                                       
        for ob in query:
            ob = contained( ob, self, stringKey(ob) )
            nodes.append(ob)    
            
        fields = list( getFields( self.context )  )
        batch = self._jsonValues( nodes, fields, self.context )
        return batch


    #XXX just proof of concept! to be removed!
    def canView(self, node, field, context):
            # set the node's parent to the context for security checks
            node.__parent__= self.context
            pn = self.request.principal.id
            grants = IPrincipalRoleMap( node, None )
            roles = grants.getRolesForPrincipal(pn)
            for role in roles:
                print role
            w_node = ProxyFactory(node)
            can_view = canAccess(w_node, field)
            print pn
            print field, can_view
            print canWrite(w_node, field)
            print canWrite(node, field)            
            return can_view
            

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
                
                self.canView(n, f, context) #XXX look at the permissions  
            values.append( d )
        return values
        
    def __call__( self ):
        start, limit = self.getOffsets( )
        sort_clause = self.getSort()
        batch = self.getBatch( start, limit, sort_clause )
        #XXX does not work with filtered listings!
        # use the query instead
        set_size = len( self.context )
        data = dict( length=set_size,
                     start=start,
                     recordsReturned=len(batch),
                     sort = self.request.get('sort'),
                     dir  = self.request.get('dir', "asc"),
                     nodes=batch )
        return simplejson.dumps( data )


def getFields( context ):
    domain_model = proxy.removeSecurityProxy( context.domain_model )
    domain_interface = queryModelInterface( domain_model )
    domain_annotation = queryModelDescriptor( domain_interface )   
    for column in  domain_annotation.listing_columns:   
        field = domain_interface[column]     
        yield field

