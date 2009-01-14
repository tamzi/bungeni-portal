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
        var sDir = (dt.get("sortedBy").dir === YAHOO.widget.DataTable.CLASS_ASC || dt.get("sortedBy").dir == "") ? "" : "desc";
        var query_url = "start=" + state.pagination.recordOffset + "&limit=" + state.pagination.rowsPerPage + "&sort=" + dt.get("sortedBy").key  + "&dir="+sDir;
        return query_url
    };
    
    var RequestBuilder = function(oState, oSelf) {
        // Get states or use defaults
        oState = oState || {pagination:null, sortedBy:null};
        var sort = (oState.sortedBy) ? oState.sortedBy.key : "";
        var dir = (oState.sortedBy && oState.sortedBy.dir === YAHOO.widget.DataTable.CLASS_DESC) ? "" : "desc";
        var startIndex = (oState.pagination) ? oState.pagination.recordOffset : 0;
        var results = (oState.pagination) ? oState.pagination.rowsPerPage : 100;
        
        // Build custom request
        return  "sort=" + sort +
                "&dir=" + dir +
                "&start=" + startIndex +
                "&limit=" +  results;
    };

    
    
    config = {        
       //paginator : %(paginator)s,
       paginator: new YAHOO.widget.Paginator({ 
	                rowsPerPage: 25, 
	                template: YAHOO.widget.Paginator.TEMPLATE_ROWS_PER_PAGE, 
	                rowsPerPageOptions: [10,25,50,100], 
	                //pageLinks: 5 
	            }),        
       initialRequest : 'start=0&limit=20',
       generateRequest : RequestBuilder, //buildQueryString,
       sortedBy : { dir : YAHOO.widget.DataTable.CLASS_ASC },
       dynamicData: true, // Enables dynamic server-driven data 
       //paginationEventHandler : YAHOO.widget.DataTable.handleDataSourcePagination 
    }

    table = new YAHOO.widget.DataTable( YAHOO.util.Dom.get("%(table_id)s"), columns, datasource, config  );
    // Update totalRecords on the fly with value from server 
	table.handleDataReturnPayload = function(oRequest, oResponse, oPayload) { 
	        oPayload.totalRecords = oResponse.meta.totalRecords; 
	        oPayload.pagination = oPayload.pagination || {};
            oPayload.pagination.recordOffset = oResponse.meta.paginationRecordOffset; 
	        return oPayload; 
	    };

    table.sortColumn = function(oColumn, sDir) {
        // Default ascending
        cDir = "asc";
        // If already sorted, sort in opposite direction     
        //var key =   this.get("sortedBy").key;
        //if(oColumn.key == this.get("sortedBy").key) {
        //   cDir = (this.get("sortedBy").dir === YAHOO.widget.DataTable.CLASS_ASC || this.get("sortedBy").dir == "") ? "desc" : "asc";
        //   };
       
        if (sDir == YAHOO.widget.DataTable.CLASS_ASC) {
            cDir = "asc"
        }
        else if (sDir == YAHOO.widget.DataTable.CLASS_DESC) {
            cDir = "desc"
        };

        // Pass in sort values to server request
        var newRequest = "sort=" + oColumn.key + "&dir=" + cDir + "&start=0";
        // Create callback for data request
        var oCallback = {
                success: this.onDataReturnInitializeTable,
                failure: this.onDataReturnInitializeTable,
                scope: this,
                argument: {
                    // Pass in sort values so UI can be updated in callback function
                    sorting: {
                        key: oColumn.key,
                        dir: (cDir === "asc") ? YAHOO.widget.DataTable.CLASS_ASC : YAHOO.widget.DataTable.CLASS_DESC,
                    }
                }
            };
                        
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
        need('yui-paginator')
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

    
