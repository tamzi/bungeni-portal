(function($) {
  $(document).ready(function() {
      // prepare alchemist content views
      var manager = $(".alchemist-content-manager");
      manager.yuiTabView(manager.find("div.listing"));

      // wire workflow dropdown menu to use POST actions
      var menu_links = $('#plone-contentmenu-workflow dd.actionMenuContent a');
      menu_links.bungeniPostWorkflowActionMenuItem();

      // set up time range form automation
      $("select").bungeniTimeRangeSelect();

      // set up calendar resizing
      $("#calendar-table").bungeniSafeResize();

      // set up calendar item scheduling (drag and drop)
      $("#items-for-scheduling tbody tr").draggable({
        cursor: 'move',
            cursorAt: { left: 5 },
            helper: function() {
            var title = $(this).children().eq(1).text();
            var helper = $('<div class="helper" />');
            helper.text(title);
            return helper;
          },
        });
    
      // set up calendar ajax
      $('#weekly-calendar').bungeniCalendarInteractivity();

    });
 })(jQuery);
