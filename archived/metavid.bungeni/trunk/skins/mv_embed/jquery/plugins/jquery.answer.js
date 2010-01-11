(function($)
{ 
    
    
    $.fn.answer = function()
    {
        var $input = $(this);
        loadChoices($input);
        return this;
    };
   
   function loadChoices($select)
   { 
        $.ajax(
        {
            url: 'http://localhost/mmm/test.php',
            type: 'GET',
            dataType: 'xml',
            timeout: 1000,
            error: function()
            {
                alert('Error loading XML document');
            },
            success: function(xml)
            {
                $(xml).find('questionnumber').each(function()
                {
                    var item_text = $(this).text();
                    $select.append( "<option>" + item_text + "</option>" );
                });
            }
        });
    };
   
    return this;
    
})(jQuery);


