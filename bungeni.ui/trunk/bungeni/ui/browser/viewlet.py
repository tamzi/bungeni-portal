# encoding: utf-8
from zope import interface
from zope.viewlet import viewlet, manager
from zope.formlib import form
from zope.formlib.namedtemplate import NamedTemplate
from interfaces import ISubFormViewletManager

from bungeni.core.i18n import _
import alchemist.ui.core
import alchemist.ui.viewlet

class AttributesEditViewlet( alchemist.ui.core.DynamicFields, alchemist.ui.viewlet.EditFormViewlet ):

    mode = "edit"
    template = NamedTemplate('alchemist.subform')
    form_name = _(u"General")
    
#class AttributesViewViewlet( alchemist.ui.core.DynamicFields, alchemist.ui.viewlet.DisplayFormViewlet ):

#    mode = "view"
#    template = NamedTemplate('alchemist.subform')    
#    form_name = _(u"General")
    
class SubFormViewletManager( manager.WeightOrderedViewletManager ):
    """
    display subforms
    """
    interface.implements(ISubFormViewletManager)     
    
    
    
