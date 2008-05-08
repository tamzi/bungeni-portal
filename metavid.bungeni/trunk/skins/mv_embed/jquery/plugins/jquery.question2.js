jQuery.fn.question = function() { 
    $w.ajax(
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
               $w(xml).find('questionnumber').each(function()
               {
                     var item_text = $w(this).text();
                     this.append( "<option>" + item_text + "</option>" );
                });
            }
      
 });
 return this;
}(jQuery);


