(function($) {
  $(document).ready(function() {
      var manager = $(".alchemist-content-manager");
      manager.yuiTabView(manager.find("div.listing"));

      var menu_links = $('#plone-contentmenu-workflow dd.actionMenuContent a');
      console.log(menu_links.length);
      menu_links.click(function() {
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

      // when selecting an option on the format "Label
      // (start_time-end_time)", listen to the ``change`` event and
      // update corresponding start- and end time options
      var re_time_range = /(.*) \((\d+):(\d+):\d+-(\d+):(\d+):\d+\)/;
      $.each($("select"), function(i, o) {
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
        
    });
 })(jQuery);
