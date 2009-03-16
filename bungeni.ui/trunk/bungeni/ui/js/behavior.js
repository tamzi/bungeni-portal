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

      $("select").bungeniTimeRangeSelect();
        
    });
 })(jQuery);
