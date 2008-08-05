# encoding: utf-8

from ore.yuiwidget.table import BaseDataTableFormatter
import container
from zope.traversing.browser import absoluteURL
from zope.security import proxy
from zc.resourcelibrary import need
import pdb

table_js_template ="""
<script type="text/javascript">
    YAHOO.util.Event.onDOMReady(function(){
  
    var datasource, columns, config;

//

	        this.%(context_name)sCustomFormatter = function(elCell, oRecord, oColumn, oData) { 
	           var object_id = oRecord.getData("object_id");
	           elCell.innerHTML = "<a href=\" +  '%(link_url)s/' + object_id + \">" + oData + "</a>"; 
	           
	        }; 
	         
	        // Add the custom formatter to the shortcuts 
	        YAHOO.widget.DataTable.Formatter.%(context_name)sCustom = this.%(context_name)sCustomFormatter; 

//

    // Setup Datasource for Container Viewlet
    datasource = new YAHOO.util.DataSource("%(data_url)s");
    datasource.responseType   = YAHOO.util.DataSource.TYPE_JSON;
    datasource.responseSchema = {
      resultsList: "nodes",
      fields: [ %(fields)s ,{key:"object_id"}],
      metaFields: { totalRecords: "length", sortKey:"sort", sortDir:"dir", paginationRecordOffset:"start"}
      }
      
    columns = [ %(columns)s ];
    
    // A custom function to translate the js paging request into a datasource query 
    var buildQueryString = function (state,dt) {
        sDir = (dt.get("sortedBy").dir === "asc"||dt.get("sortedBy").dir == "") ? "" : "desc";
        var query_url = "start=" + state.pagination.recordOffset + "&limit=" + state.pagination.rowsPerPage + "&sort=" + dt.get("sortedBy").key  + "&dir="+sDir;
        return query_url
    };
    
    config = {
       paginator : %(paginator)s,
       initialRequest : 'start=0&limit=20',
       generateRequest : buildQueryString,
       sortedBy : { key: "firstName", dir : "asc" },
       paginationEventHandler : YAHOO.widget.DataTable.handleDataSourcePagination 
    }

    table = new YAHOO.widget.DataTable( YAHOO.util.Dom.get("%(table_id)s"), columns, datasource, config  )

    table.sortColumn = function(oColumn) {
        // Default ascending
        var sDir = "asc";
        
        // If already sorted, sort in opposite direction
        if(oColumn.key === this.get("sortedBy").key) {
           sDir = (this.get("sortedBy").dir === "asc"||this.get("sortedBy").dir == "") ? "desc" : "asc";
           }

        // Pass in sort values to server request
        var newRequest = "sort=" + oColumn.key + "&dir=" + sDir + "&start=0";
        // Create callback for data request
        var oCallback = {
                success: this.onDataReturnInitializeTable,
                failure: this.onDataReturnInitializeTable,
                scope: this,
                argument: {
                    // Pass in sort values so UI can be updated in callback function
                    sorting: {
                        key: oColumn.key,
                        dir: (sDir === "asc") ? YAHOO.widget.DataTable.CLASS_ASC : YAHOO.widget.DataTable.CLASS_DESC
                    }
                }
            }
            
        // Send the request
        this.getDataSource().sendRequest(newRequest, oCallback);
        };
       
});
</script>
"""

class ContextDataTableFormatter( BaseDataTableFormatter ):
    data_view ="/@@jsonlisting"
    prefix = "listing"
    
#    def __init__( self, context, request, items,  paginator=None, data_view=None, *args, **kw ):
#        if paginator:
#            self.paginator = paginator
#        if data_view:
#            self.data_view = data_view  
#        else:
#            self.data_view = "/@@jsonlisting" #%  context.__name__ #absoluteURL( context, request )            
#        super( ContextDataTableFormatter, self).__init__( context, request, items, paginator, data_view, *args, **kw )                      
#        self.link_url = absoluteURL( context, request )
        
    def getFields( self ):
        return container.getFields( self.context )

    def getFieldColumns( self ):
        # get config for data table
        column_model = []
        field_model  = []

        for field in self.getFields( ):
            key = field.__name__
            column_model.append(
                '{key:"%s", label:"%s", formatter:"%sCustom", sortable:true}'%( key, field.title, self.context.__name__ )
                )
            field_model.append(
                '{key:"%s"}'%( key )               
                )
        #columns, fields
        return ','.join( column_model ), ','.join( field_model )


    def getDataTableConfig( self ):
        """
        fields
        columns
        table_id
        """
        config = {}
        config['columns'], config['fields'] = self.getFieldColumns()
        config['data_url'] = self.getDataSourceURL()
        config['table_id'] = self.prefix
        config['paginator'] = self.paginator
        #config['sort_field'] = self.columns[0].name.replace(' ', '_').lower()
        config['link_url'] = absoluteURL( self.context, self.request ) 
        config['context_name'] = self.context.__name__
        return config

    def renderExtra( self ):
        need('yui-datatable')
        extra = table_js_template%(self.getDataTableConfig())
        return extra


    def __call__(self):
        return '<div id="%s">\n<table %s>\n%s</table>\n%s</div>' % (
                self.prefix,
                self._getCSSClass('table'), self.renderContents(),
                self.renderExtra())


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

    
