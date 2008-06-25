
from zope.app.form.browser.widget import UnicodeDisplayWidget, DisplayWidget
from zope.app.form.browser.textwidgets import TextAreaWidget
from zc.resourcelibrary import need

class ImageDisplayWidget(DisplayWidget):
    def __call__(self):
        return '<img src="@@file-image/%s" />' % self.context.__name__

class HTMLDisplay(UnicodeDisplayWidget):
    
    def __call__( self ):
        if self._renderedValueSet():
            value = self._data
        else:
            value = self.context.default
        if value == self.context.missing_value:
            return ""    
        return unicode(value)

class RichTextEditor( TextAreaWidget ):
    
    def __call__( self ):
        # require yahoo rich text editor and dependencies
        need('yui-editor')
        
        # render default input widget for text
        input_widget = super( RichTextEditor, self).__call__()
        
        # use '_' instead of '.' for js identifiers
        jsid = self.name.replace('.','_')
        
        # attach behavior to default input widget, disable titlebar
        input_widget += u"""
        <script language="javascript">
            options={ height:'300px', 
                      width:'530px', 
                      dompath:false, 
                      focusAtStart:false};
            var %s_editor = new YAHOO.widget.SimpleEditor('%s', options); 
            YAHOO.util.Event.on(
                %s_editor.get('element').form, 
                'submit', 
                function( ev ) { 
                    %s_editor.saveHTML(); 
                    }
                );            
            %s_editor._defaultToolbar.titlebar = false;
            %s_editor.render();     
        </script>    
        """%(jsid, self.name, jsid, jsid, jsid, jsid)
        
        # return the rendered input widget
        return input_widget
