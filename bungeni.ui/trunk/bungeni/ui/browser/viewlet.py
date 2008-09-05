# encoding: utf-8
from zope import interface
from zope.viewlet import viewlet, manager
from zope.formlib import form
from zope.formlib.namedtemplate import NamedTemplate
from zc.resourcelibrary import need

import alchemist.ui.core
import alchemist.ui.viewlet

from bungeni.ui.i18n import _
from interfaces import ISubFormViewletManager

class AttributesEditViewlet( alchemist.ui.core.DynamicFields, alchemist.ui.viewlet.EditFormViewlet ):

    mode = "edit"
    template = NamedTemplate('alchemist.subform')
    form_name = _(u"General")
    

    
class SubFormViewletManager( manager.WeightOrderedViewletManager ):
    """
    display subforms
    """
    interface.implements(ISubFormViewletManager)     
    
class NavigateAwayWarningViewlet( viewlet.ViewletBase ):

    def render(self):
        need('yui-core')
        #warningMessage = _(u"""'You have unsaved data on this page, leave this page? Clicking “yes” to continue will loose your changes forever.'""")
        msg = u"""<script>
        YAHOO.util.Event.addListener(window, 'beforeunload', function(e) {
        if (e.target !='[object HTMLFormElement]') {		        
		        YAHOO.util.Event.stopEvent(e);
	      }
        });    
        </script>""" # % warningMessage

        return msg
