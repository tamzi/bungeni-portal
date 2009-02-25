# encoding: utf-8

#import pdb
from zope.app.pagetemplate import ViewPageTemplateFile

from zope.security.proxy import removeSecurityProxy


from ore.alchemist.model import queryModelDescriptor
from ore.workflow import interfaces

from bungeni.core.i18n import _

from alchemist.ui.core import DynamicFields

from bungeni.ui.forms.workflow import bindTransitions
from alchemist.ui.viewlet import DisplayFormViewlet
from zc.resourcelibrary import need

class BungeniAttributeDisplay(DynamicFields, DisplayFormViewlet):
    mode = "view"
    template = ViewPageTemplateFile('templates/display_form.pt')        
    form_name = _(u"General")    
    has_data = True

    def setupActions( self ):
        try:
            self.wf = interfaces.IWorkflowInfo( self.context )
            transitions = self.wf.getManualTransitionIds()
            self.actions = tuple(bindTransitions( self, transitions, None, interfaces.IWorkflow( self.context ) ) )  
        except:
            pass
            
    def update( self ):
        need("yui-tab")
        self.form_name = self.getform_name()
        self.setupActions()
        super(BungeniAttributeDisplay, self).update() 
        self.setupActions()  # after we transition we have different actions  
        try:
            wf_state =interfaces.IWorkflowState(
                removeSecurityProxy(self.context)).getState()
            self.wf_status = wf_state  
        except:
            pass
               
    def getform_name( self ):
        try:
            if self.context.__parent__:
                descriptor = queryModelDescriptor(
                    self.context.__parent__.domain_model)
            else:
                return self.form_name
        except:
            return self.form_name                        
        if descriptor:
            name = getattr( descriptor, 'display_name', None)
        if not name:
            name = getattr( self.context.__parent__.domain_model, '__name__', None)                
        return name #"%s %s"%(name, self.mode.title())





  
