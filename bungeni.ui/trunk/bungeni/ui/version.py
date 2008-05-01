"""
User interface for Content Versioning.
"""
from alchemist.ui.core import BaseForm, getSelected
from zope import interface, component, schema
from zope.security.proxy import removeSecurityProxy
from zope.formlib import form
from zope.publisher.browser import  BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zc.table import  column, batching
from interfaces import IVersionViewletManager
from zope.viewlet.manager import WeightOrderedViewletManager
from zope.viewlet import viewlet
from bungeni.core.interfaces import IVersioned
from bungeni.core.i18n import _

from ore.alchemist.interfaces import IIModelInterface
from zope.app.publisher.browser import queryDefaultViewName

import z3c.schemadiff.browser

class VersionViewletManager( WeightOrderedViewletManager ):
    """
    implements the Version viewlet
    """
    interface.implements(IVersionViewletManager)


class IVersionEntry( interface.Interface ):
    
    commit_message = schema.Text(title=_("Change Message") )

class VersionLogViewlet(BaseForm , viewlet.ViewletBase ):
    form_fields = form.Fields( IVersionEntry )
    formatter_factory = batching.Formatter
    render = ViewPageTemplateFile ('templates/version_viewlet.pt')

    extra = None
    
    columns = [
        column.SelectionColumn( lambda item: str(item.version_id), name="selection"),
        column.GetterColumn( title=_(u"version"), getter=lambda i,f:i.version_id ),    
        column.GetterColumn( title=_(u"modified"), getter=lambda i,f: i.change.date ),
        column.GetterColumn( title=_(u"by"), getter=lambda i,f:i.change.user_id ),
        column.GetterColumn( title=_(u"message"), getter=lambda i,f:i.change.description ),
        ]    
    
    selection_column = columns[0]

    def listing( self ):
        columns = self.columns
        formatter = self.formatter_factory( self.context,
                                            self.request,
                                            self._versions.values(),
                                            prefix="results",
                                            visible_column_names = [c.name for c in columns],
                                            #sort_on = ('name', False)
                                            columns = columns )
        formatter.cssClasses['table'] = 'listing'
        formatter.updateBatching()
        return formatter()
            
    @form.action(label=_("New Version") )
    def handle_new_version( self, action, data ):
        self._versions.create( message = data['commit_message'] )        
        self.status = _(u"New Version Created")

    #def validate_diff_version( self, ):
    #def validate_revert_version( self )

    @form.action(label=_("Revert To") )
    def handle_revert_version( self, action, data):
        selected = getSelected( self.selection_column, self.request )        
        version = self._versions.get( selected[0] )
        message = data['commit_message']
        self._versions.revert( version, message )
        self.status = (_(u"Reverted to Previous Version %s") %(version.version_id))

    @form.action(
        label=_("View"), name="view", validator=lambda form, action, data: ())
    def handle_view_version( self, action, data):
        selected = getSelected(self.selection_column, self.request)
        context = self._versions.get( selected[0] )

        view = component.getMultiAdapter((context, self.request),
                                         name=queryDefaultViewName(context, self.request))

        self.extra = view()
        
    @form.action(
        label=_("Show Differences"), name="diff", validator=lambda form, action, data: ())
    def handle_diff_version( self, action, data):
        self.status = _("Displaying differences.")

        selected = getSelected(self.selection_column, self.request)
        
        if len(selected) not in (1, 2):
            self.status = _("Select one or two items to show differences.")
            return

        context = removeSecurityProxy(self.context)
        source = self._versions.get( selected[0] )
                
        try:
            target = self._versions.get( selected[1] )
        except:
            target = context
            
        view = z3c.schemadiff.browser.DiffView(source, target, self.request)

        self.extra = view(
            *filter(IIModelInterface.providedBy, interface.providedBy(context)))

    def setUpWidgets( self, ignore_request=False):
        # setup widgets in data entry mode not bound to context
        self.adapters = {}
        self.widgets = form.setUpDataWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            ignore_request = ignore_request )
        
    @property
    def _versions( self ):
        instance = removeSecurityProxy( self.context )
        versions = IVersioned( instance )
        return versions
        

class VersionLog( BrowserPage ):
    
    __call__ = ViewPageTemplateFile('templates/version.pt')
    
