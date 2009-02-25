<script type="text/javascript">
<![CDATA[
(function() {
  var bungeni_tabView = new YAHOO.widget.TabView();
  var elements = YAHOO.util.Dom.getElementsByClassName('listing', 'div', 'bungeni-tabbed-nav' );
  
  for (i=0; i < elements.length; i++)
    {
      tab_label = YAHOO.util.Dom.getFirstChild(elements[i])
        bungeni_tabView.addTab( new YAHOO.widget.Tab({
            labelEl : tab_label,
                contentEl : elements[i]
                }));
    };
  
  bungeni_tabView.appendTo('bungeni-tabbed-nav');
  bungeni_tabView.set('activeTab', bungeni_tabView.getTab(0));
 })();
]]>
</script>
