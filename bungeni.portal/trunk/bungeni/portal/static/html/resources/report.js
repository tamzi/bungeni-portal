(function($) { 
    $(document).ready(function(){  
        $("#groupsitting-form #actionsView").before('<div id="options" style="display:block"></div>');
        $("#form\\.bill_options\\.0").parents(".widget-multicheckboxwidget").appendTo("#options").css('display', 'inline-block');
        $("#form\\.bill_options\\.0").parents(".widget-multicheckboxwidget").hide();
        $("#form\\.agenda_options\\.0").parents(".widget-multicheckboxwidget").appendTo("#options").css('display', 'inline-block');
        $("#form\\.agenda_options\\.0").parents(".widget-multicheckboxwidget").hide();
        $("#form\\.motion_options\\.0").parents(".widget-multicheckboxwidget").appendTo("#options").css('display', 'inline-block');
        $("#form\\.motion_options\\.0").parents(".widget-multicheckboxwidget").hide();
        $("#form\\.question_options\\.0").parents(".widget-multicheckboxwidget").appendTo("#options").css('display', 'inline-block');
        $("#form\\.question_options\\.0").parents(".widget-multicheckboxwidget").hide();
        $("#form\\.tabled_document_options\\.0").parents(".widget-multicheckboxwidget").appendTo("#options").css('display', 'inline-block');
        $("#form\\.tabled_document_options\\.0").parents(".widget-multicheckboxwidget").hide();
        $("#options span").css('padding','0 0 0 0');
        $("#form\\.bill_options\\.0").attr('checked', true);
        $("#form\\.bill_options\\.1").attr('checked', true);
        $("#form\\.agenda_options\\.0").attr('checked', true);
        $("#form\\.agenda_options\\.3").attr('checked', true);
        $("#form\\.motion_options\\.0").attr('checked', true);
        $("#form\\.motion_options\\.3").attr('checked', true);
        $("#form\\.question_options\\.0").attr('checked', true);
        $("#form\\.question_options\\.3").attr('checked', true);
        $("#form\\.tabled_document_options\\.0").attr('checked', true);
        $("#form\\.tabled_document_options\\.3").attr('checked', true);
        var pathname = window.location.pathname;
        var path = new Array();
        path = pathname.split("/");
        var doc_type = path[path.length-1];
        if (doc_type == "")
        {
            doc_type = path[path.length-2];
        }
        if (doc_type == 'agenda')
        {
            $("#form\\.doc_type option[value='Proceedings of the day']").remove();
        }
        else
        {
            $("#form\\.doc_type option[value='Order of the day']").remove();
        }   
        $("input#form\\.item_types\\.0").change(function () {
            if ($("#form\\.item_types\\.0").is(":checked"))
            {
                $("#form\\.bill_options\\.0").parents(".widget-multicheckboxwidget").show();
            }
            else
            {
                $("#form\\.bill_options\\.0").parents(".widget-multicheckboxwidget").hide();
            }
        });
        $("input#form\\.item_types\\.1").change(function () {
            if ($("#form\\.item_types\\.1").is(":checked"))
            {
                $("#form\\.agenda_options\\.0").parents(".widget-multicheckboxwidget").show();
            }
            else
            {
                $("#form\\.agenda_options\\.0").parents(".widget-multicheckboxwidget").hide();
            }
        });
        $("input#form\\.item_types\\.2").change(function () {
            if ($("#form\\.item_types\\.2").is(":checked"))
            {
                $("#form\\.motion_options\\.0").parents(".widget-multicheckboxwidget").show();
            }
            else
            {
                $("#form\\.motion_options\\.0").parents(".widget-multicheckboxwidget").hide();
            }
        });
        $("input#form\\.item_types\\.3").change(function () {
            if ($("#form\\.item_types\\.3").is(":checked"))
            {
                $("#form\\.question_options\\.0").parents(".widget-multicheckboxwidget").show();
            }
            else
            {
                $("#form\\.question_options\\.0").parents(".widget-multicheckboxwidget").hide();
            }
        });
        $("input#form\\.item_types\\.4").change(function () {
            if ($("#form\\.item_types\\.4").is(":checked"))
            {
                $("#form\\.tabled_document_options\\.0").parents(".widget-multicheckboxwidget").show();
            }
            else
            {
                $("#form\\.tabled_document_options\\.0").parents(".widget-multicheckboxwidget").hide();
            }
        });
        $("#form\\.doc_type").change(function() {
            var choice = $("option:selected", this).val();
            if (choice == "Order of the day")
            {
                $("#form\\.item_types\\.0").attr('checked', true);
                $("#form\\.item_types\\.1").attr('checked', true);
                $("#form\\.item_types\\.2").attr('checked', true);
                $("#form\\.item_types\\.3").attr('checked', true);
                $("#form\\.item_types\\.4").attr('checked', true);
            }
            else if (choice == "Proceedings of the day")
            {
                $("#form\\.item_types\\.0").attr('checked', true);
                $("#form\\.item_types\\.1").attr('checked', true);
                $("#form\\.item_types\\.2").attr('checked', true);
                $("#form\\.item_types\\.3").attr('checked', true);
                $("#form\\.item_types\\.4").attr('checked', true);
            }
            else if (choice == "Weekly Business")
            {
                $("#form\\.item_types\\.0").attr('checked', true);
                $("#form\\.item_types\\.1").attr('checked', true);
                $("#form\\.item_types\\.2").attr('checked', true);
                $("#form\\.item_types\\.3").attr('checked', false);
                $("#form\\.item_types\\.4").attr('checked', true);
            }
            else if (choice == "Questions of the week")
            {
                $("#form\\.item_types\\.0").attr('checked', false);
                $("#form\\.item_types\\.1").attr('checked', false);
                $("#form\\.item_types\\.2").attr('checked', false);
                $("#form\\.item_types\\.3").attr('checked', true);
                $("#form\\.item_types\\.4").attr('checked', false);
            }
            $("#form\\.item_types\\.0").trigger('change');
            $("#form\\.item_types\\.1").trigger('change');
            $("#form\\.item_types\\.2").trigger('change');
            $("#form\\.item_types\\.3").trigger('change');
            $("#form\\.item_types\\.4").trigger('change');
        }).change();

    });
 })(jQuery)
