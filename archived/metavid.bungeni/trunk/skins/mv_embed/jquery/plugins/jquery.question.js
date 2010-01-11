(function($)
{ 
    
    
    $.fn.question = function()
    {
        var $input = $(this);
        loadChoices($input);
        
         
            $input.change(function()
            {
                lookup($input.val())
            }
            );
         
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
    
    
        
    function lookup(id)
    {
        $.ajax(
        {   
            url: 'http://localhost/mmm/test.php',
            type: 'GET',
            data : "id="+id,
            timeout: 1000,
            error: function()
            {
                alert('Error loading XML document');
            },
            success: function(xml)
            {
                $(xml).find('questiontext').each(function()
                {
                    var item_text = $(this).text();
                    $("textarea#wpTextbox1").html( item_text );
                });
                $(xml).find('questionmp').each(function()
                {
                    var item_text = $(this).text();
                    $("textarea#wpTextbox1").html( item_text );
                });
                $(xml).find('questionimage').each(function()
                {
                    var item_text = $(this).text();
                    $("textarea#wpTextbox1").html( item_text );
                });
            }
        });
    };
        
    return this;
    
})(jQuery);


