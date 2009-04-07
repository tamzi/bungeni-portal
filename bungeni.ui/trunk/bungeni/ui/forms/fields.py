# encoding: utf-8

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.security.proxy import removeSecurityProxy

from ore.alchemist.model import queryModelDescriptor
from ore.alchemist.interfaces import IAlchemistContainer
from ore.alchemist.interfaces import IAlchemistContent
from ore.workflow import interfaces
from alchemist.ui.core import DynamicFields
from alchemist.ui.viewlet import DisplayFormViewlet

from bungeni.ui.forms.workflow import bindTransitions
from bungeni.core.i18n import _

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
        self.setupActions()
        super(BungeniAttributeDisplay, self).update() 
        self.setupActions()  # after we transition we have different actions  
        try:
            wf_state =interfaces.IWorkflowState(
                removeSecurityProxy(self.context)).getState()
            self.wf_status = wf_state  
        except:
            pass

    @property
    def form_name( self ):
        parent = self.context.__parent__
        if IAlchemistContainer.providedBy(parent):
            descriptor = queryModelDescriptor(parent.domain_model)
        elif IAlchemistContent.providedBy(self.context):
            descriptor = queryModelDescriptor(self.context.__class__)
        else:
            raise RuntimeError("Unsupported object: %s." % repr(self.context))
        
        if descriptor:
            name = getattr(descriptor, 'display_name', None)

        if name is None:
            name = self.context.__class__.__name__

        return name
