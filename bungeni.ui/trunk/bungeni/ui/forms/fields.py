# encoding: utf-8

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.security.proxy import removeSecurityProxy
from zope import security

from ore.alchemist.model import queryModelDescriptor
from ore.alchemist.interfaces import IAlchemistContainer
from ore.alchemist.interfaces import IAlchemistContent
from ore.workflow import interfaces
from alchemist.ui.core import DynamicFields
from alchemist.ui.viewlet import DisplayFormViewlet

from bungeni.ui.forms.workflow import bindTransitions
from bungeni.core.i18n import _

def filterFields(context, form_fields):
    omit_names=[]
    for field in form_fields:
        if security.canWrite( context, field.__name__):
            #r/w
            continue
        if security.canAccess( context, field.__name__):                
            field.for_display = True
            #r/o
        else:
            omit_names.append(field.__name__)
            #ignore          
    return form_fields.omit(*omit_names)   


class BungeniAttributeDisplay(DynamicFields, DisplayFormViewlet):
    mode = "view"
    template = ViewPageTemplateFile('templates/display_form.pt')
    form_name = _(u"General")    
    has_data = True

    def setupActions(self):
        return
        wf = self.wf = interfaces.IWorkflowInfo(self.context, None)
        if wf is not None:
            transitions = self.wf.getManualTransitionIds()
            self.actions = tuple(bindTransitions(
                self, transitions, None, interfaces.IWorkflow( self.context)))

    def setUpWidgets(self, ignore_request=False):
        self.form_fields = filterFields(self.context, self.form_fields)
        super(BungeniAttributeDisplay, self).setUpWidgets(ignore_request=ignore_request)
            
    def update( self ):
        self.setupActions()
        self.form_fields = filterFields(self.context, self.form_fields)
        super(BungeniAttributeDisplay, self).update() 
        #self.setUpWidgets()
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

