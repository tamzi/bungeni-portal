# encoding: utf-8
from zope import interface
from zope.viewlet import viewlet, manager
from zope.formlib import form
from zope.formlib.namedtemplate import NamedTemplate
from zope.app.pagetemplate import ViewPageTemplateFile

from zc.resourcelibrary import need

from ore.alchemist import Session
import bungeni.core.domain as domain

import alchemist.ui.core
import alchemist.ui.viewlet


from bungeni.ui.i18n import _
from interfaces import ISubFormViewletManager, IResponeQuestionViewletManager

class AttributesEditViewlet( alchemist.ui.core.DynamicFields, alchemist.ui.viewlet.EditFormViewlet ):

    mode = "edit"
    template = NamedTemplate('alchemist.subform')
    form_name = _(u"General")
    

    
class SubFormViewletManager( manager.WeightOrderedViewletManager ):
    """
    display subforms
    """
    interface.implements(ISubFormViewletManager)   
      
    def filter(self, viewlets):
         viewlets = super(SubFormViewletManager, self).filter(viewlets)
         return [(name, viewlet)
                 for name, viewlet in viewlets
                 if viewlet.for_display == True]    
    




    
class NavigateAwayWarningViewlet( viewlet.ViewletBase ):

    def render(self):
        need('yui-core')
        #warningMessage = _(u"""'You have unsaved data on this page, leave this page? Clicking “yes” to continue will loose your changes forever.'""")
        msg = u"""<script>
        YAHOO.util.Event.addListener(window, 'beforeunload', function(e) {
        //confirm('navigate away: ' + e.target.tagName)
        if (!e.target || (e.target.tagName.upperCase() != 'FORM')) {		        
		        YAHOO.util.Event.stopEvent(e);
	      }
        });    
        </script>""" # % warningMessage

        return msg
        
class ResponseQuestionViewletManager( manager.WeightOrderedViewletManager ):
    """
    display subforms
    """
    interface.implements(IResponeQuestionViewletManager)         
    

class ResponseQuestionViewlet( viewlet.ViewletBase ):    
    """
    Display the question when adding/editing a response
    """
    def __init__( self,  context, request, view, manager ):        

        self.context = context
        self.request = request
        self.__parent__= context
        self.manager = manager
        self.query = None
        self.subject = ''
        self.question_text = ''
    
    def update(self):
        if self.context.__class__ == domain.Response:
            #edit response
            question_id = context.response_id
            session = Session()
            return session.query(domain.Question).get(question_id)
            self.subject = self.context.__parent__.__parent__.subject
            self.question_text = self.context.__parent__.__parent__.question_text
        else:
            # add a response
            if self.context.__parent__.__class__ == domain.Question:
                self.subject = self.context.__parent__.subject
                self.question_text = self.context.__parent__.question_text

    render = ViewPageTemplateFile ('templates/question.pt')  
