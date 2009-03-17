(function($) {
  var re_time_range = /(.*) \((\d+):(\d+):\d+-(\d+):(\d+):\d+\)/;
  
  $.fn.bungeniCalendarInteractivity = function() {
    var calendar = $(this);
    var selector = '#'+calendar.attr('id');
    
    calendar.find("td.sitting")
    .droppable({
      accept: "*",
          })
    .bind('drop', function(droppable) {
        var id = $(this).find("a[relation=id]");
        var target = $(droppable.target);
        var link = target.find("a[relation=schedule-item]");
        var url = link.attr('href');

        $.post(url, {item_id: id}, function(data, status) {
            console.log(data);
          });
      });

    calendar.find("thead a")
    .click(function() {
        $.get($(this).attr('href'), {}, function(data, status) {
            var old_tables = calendar.find("table");
            var new_tables = $(data).find(selector).find("table");
            
            old_tables.eq(0).replaceWith(new_tables.eq(0));
            old_tables.eq(1).replaceWith(new_tables.eq(1));

            calendar.bungeniCalendarInteractivity();
          });
        return false;
      });
  }
  
  $.fn.bungeniSafeResize = function() {
    $.each($(this), function(i, o) {
        var table = $(o);
        if (table) {
          var wrapper = $('<div id="calendar-table-resize-wrapper" />');
          table.wrap(wrapper);
          wrapper = table.parents("#calendar-table-resize-wrapper");
          
          wrapper
            .resizable({
              helper: "resize-proxy",
                  handles: "s",
                  });
          
          wrapper.bind("resizestop", function(event, ui) {
              var height = wrapper.height();
              table.css("height", height+"px");
            });
        }
      });
  };
  
  $.fn.bungeniCalendarSittingsDragAndDrop = function(sittings) {
    $.each($(this), function(i, o) {
        var id = $(o).attr('id');
        var dd = new YAHOO.util.DDProxy(id);

      });
  };
  
  $.fn.bungeniPostWorkflowActionMenuItem = function() {
    $(this).click(function() {
        var url_parts = $(this).attr("href").split('?');
        var url = url_parts[0];
        var args = url_parts[1].split('=');
        if (args[0] == 'transition') {
          var transition_id = args[1];
          
          var input = $('<input type="hidden" name="transition"/>').
            attr("value", transition_id);
          
          var form = $("<form/>").
            attr("method", "POST").
            attr("action", url).
            appendTo(document.body);
          
          input.appendTo(form);
          form.get(0).submit();
          
          return false;
        }
      });
  };
  
  // when selecting an option on the format "Label
  // (start_time-end_time)", listen to the ``change`` event and
  // update corresponding start- and end time options
  $.fn.bungeniTimeRangeSelect = function() {
    $.each($(this), function(i, o) {
      var options = $(o).children();
      var form = $(o).parents("form").eq(0);

      var start_hour = form.find("select[name$=start_date__hour]").get(0);
      if (!start_hour) return;
      var start_minute = form.find("select[name$=start_date__minute]").get(0);
      if (!start_minute) return;
      var end_hour = form.find("select[name$=end_date__hour]").get(0);
      if (!end_hour) return;
      var end_minute = form.find("select[name$=end_date__minute]").get(0);
      if (!end_minute) return;

      var option_matches = [];
      $.each(options, function(j, p) {
          var option = $(p);
          var matches = re_time_range.exec(option.text());
          option_matches.push(matches);
          if (matches)
            option.text(matches[1]);
        });

      function handle_change() {
        var matches = option_matches[o.selectedIndex];

        if (!matches) return;

        // convert matches to integers
        for (var k=1; k < 5; k++) {
          var v = matches[k];
          if (v[0] == '0') v = v[1];
          matches[k] = parseInt(v);
        }

        // for each dropdown, change selection
        start_hour.selectedIndex = matches[2]
        start_minute.selectedIndex = matches[3];
        end_hour.selectedIndex = matches[4];
        end_minute.selectedIndex = matches[5];
      };

      // setup event handler
      $(o).change(handle_change);

      // initialize
      handle_change();
    });
  };
    
    
  $.fn.yuiTabView = function(elements) {
    if (!YAHOO.widget.TabView) {
      return console.log("Warning: YAHOO.widget.TabView module not loaded.")
    }
    var tab_view = new YAHOO.widget.TabView();
    
    $.each(elements, function(i, o) {
        var label = YAHOO.util.Dom.getFirstChild(o)
          tab_view.addTab(new YAHOO.widget.Tab({
              labelEl : label, contentEl : o,
                  }));
      });

    tab_view.appendTo($(this).get(0));
    tab_view.set('activeTab', tab_view.getTab(0));
  };
  
  $.fn.yuiDataTable = function(context_name, link_url, data_url, fields, columns, table_id) {
    if (!YAHOO.widget.DataTable) {
      return console.log("Warning: YAHOO.widget.DataTable module not loaded.")
    }

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
