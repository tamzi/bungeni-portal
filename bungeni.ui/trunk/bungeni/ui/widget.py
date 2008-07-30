
from zope.app.form.browser.widget import UnicodeDisplayWidget, DisplayWidget
from zope.app.form.browser.textwidgets import TextAreaWidget, FileWidget
from zope.app.form.interfaces import ConversionError
from zc.resourcelibrary import need
from zope.app.form.browser.itemswidgets import  RadioWidget
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from bungeni.core.i18n import _

def CustomRadioWidget( field, request ):
    """ to replace the default combo box widget for a schema.choice field"""
    vocabulary = field.vocabulary
    return RadioWidget( field, vocabulary, request )


class ImageInputWidget(FileWidget):
    """
    render a inputwidget that displays the current
    image and lets you choose to delete, replace or just
    leave the current image as is.
    """
    _missing = u''
    
    
    __call__ = ViewPageTemplateFile('templates/imagewidget.pt')    
    
    @property
    def update_action_name(self):
        return self.name + '.up_action'
        
    @property
    def upload_name(self):
        return self.name.replace(".","_") + '_file'
        
    @property    
    def imageURL(self):
        return '@@file-image/%s' % self.context.__name__            
        
    def empty_field(self):
        return self._data is None

    def _getFieldInput(self, name):
        return self.request.form.get(name, self._missing)     
                
    def _getFormInput(self):
        """extract the input value from the submitted form """
        return (self._getFieldInput(self.update_action_name),
                self._getFieldInput(self.upload_name))
        

    def _toFieldValue( self, (update_action, upload) ):
        """convert the input value to an value suitable for the field.
        check the update_action if we should leave the data alone, delete or replace it"""
        if update_action == u'update':
            if upload is None or upload == '':
                if self._data is None:
                    return self.context.missing_value
                else:                    
                    raise ConversionError(_('Form upload is not a file object'))                
            try:
                seek = upload.seek
                read = upload.read
            except AttributeError, e:
                raise ConversionError(_('Form upload is not a file object'), e)
            else:
                seek(0)
                data = read()
                if data or getattr(upload, 'filename', ''):
                    return data
                else:
                    return self.context.missing_value
        elif update_action == u'delete':
            return None
        else:
            raise NotImplementedError
            return                    
                
    def hasInput(self):
        """
        determins if the widget widget has changed
        """       

        if self.update_action_name in self.request.form:
            action = self.request.form.get(self.update_action_name, self._missing) 
            if action == u'keep':
                return False
            elif action == u'delete':
                return True
            else:
                return self.upload_name  in self.request.form   
 


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
