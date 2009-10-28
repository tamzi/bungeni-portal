(function($) {
  $(document).ready(function() {
      // wire workflow dropdown menu to use POST actions
      var menu_links = $('#plone-contentmenu-workflow dd.actionMenuContent a');
      menu_links.bungeniPostWorkflowActionMenuItem();

      // set up parliament date range selection
      $("select[id=form.parliament]").bungeniTimeRangeSelect(false, false);

      // set up sitting time range form automation
      var select = $("select[id=form.sitting_type_id]");
      var errors = select.parents("form").eq(0).find(".widget.error").length > 0;
      select.bungeniTimeRangeSelect(true, !errors);

      // set up calendar resizing
      $("#calendar-table").bungeniSafeResize();

      // set up calendar item scheduling (drag and drop)
      $("#items-for-scheduling-bill tbody tr").bungeniDragAndDropScheduling();
      $("#items-for-scheduling-motion tbody tr").bungeniDragAndDropScheduling();
      $("#items-for-scheduling-question tbody tr").bungeniDragAndDropScheduling();
      $("#items-for-scheduling-agendaitem tbody tr").bungeniDragAndDropScheduling();
      $("#items-for-scheduling-tableddocument tbody tr").bungeniDragAndDropScheduling();
                              
      // set up calendar ajax
      $('#weekly-calendar').bungeniCalendarInteractivity(true);
      $('#daily-calendar').bungeniCalendarInteractivity(false);
      $('#scheduling-calendar').bungeniSchedulingCalendar();
      $('#scheduling-calendar').bungeniInteractiveSchedule();
    });
 })(jQuery);
