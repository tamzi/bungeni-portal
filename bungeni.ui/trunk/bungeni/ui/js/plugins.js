(function($) {
  $.fn.yuiDataTable = function(context_name, link_url, data_url, fields, columns, table_id) {

    var datasource, columns, config;
    
    var formatter = function(elCell, oRecord, oColumn, oData) {
      var object_id = oRecord.getData("object_id");
      elCell.innerHTML = "<a href=\"" +  link_url + '/' + object_id + "\">" + oData + "</a>";
    };
    
    YAHOO.widget.DataTable.Formatter[context_name+"Custom"] = formatter;

    // Setup Datasource for Container Viewlet
    fields.push({key:"object_id"});
    datasource = new YAHOO.util.DataSource(data_url);
    datasource.responseType   = YAHOO.util.DataSource.TYPE_JSON;
    datasource.responseSchema = {
    resultsList: "nodes",
    fields: fields,
    metaFields: { totalRecords: "length", sortKey:"sort", sortDir:"dir", paginationRecordOffset:"start"}
    }
      
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

    table = new YAHOO.widget.DataTable(YAHOO.util.Dom.get(table_id), columns, datasource, config  );
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
      var sorted_by =   this.get("sortedBy");
      sorted_by = sorted_by || {key:null, dir:null};
      if(oColumn.key == sorted_by.key) {
        cDir = (sorted_by.dir === YAHOO.widget.DataTable.CLASS_ASC || sorted_by.dir == "") ? "desc" : "asc";
      };
       
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

  };
 })(jQuery);
