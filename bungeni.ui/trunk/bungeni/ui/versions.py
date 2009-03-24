from zope import interface
from zope import component
from zope import schema

from zope.publisher.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.publisher.browser import queryDefaultViewName
from zope.formlib import form
from zope.security.proxy import removeSecurityProxy

from ore.alchemist.interfaces import IIModelInterface

from bungeni.ui.i18n import MessageFactory as _
from bungeni.core.interfaces import IVersioned

from alchemist.ui.core import BaseForm, getSelected
from zc.table import  column, batching
import z3c.schemadiff.browser

class VersionsView(BrowserView):
    """To-Do: Find out why this class isn't hooked up."""
    
    def __call__(self):
        context = self.context.__parent__.__parent__
        ifaces = filter(IIModelInterface.providedBy, interface.providedBy(context))

        class Form(form.DisplayForm):
            template = ViewPageTemplateFile("templates/form.pt")
            form_fields = form.FormFields(*ifaces)

            form_name = _(u"View")

            @property
            def description(self):
                return _(u"Currently displaying version ${version}.",
                         mapping={'version': self.context.version_id})
            
            def setUpWidgets( self, ignore_request=False):
                self.adapters = dict(
                    [(iface, self.context) for iface in ifaces])

                self.widgets = form.setUpEditWidgets(
                    self.form_fields, self.prefix, self.context, self.request,
                    adapters=self.adapters, for_display=True,
                    ignore_request=ignore_request
                    )

        view = Form(self.context, self.request)

        return view()                

class IVersionEntry( interface.Interface ):
    commit_message = schema.Text(title=_(u"Change Message"))

class VersionLogView(BaseForm):
    form_fields = form.Fields( IVersionEntry )
    formatter_factory = batching.Formatter
    
    render = ViewPageTemplateFile('templates/version.pt')

    extra = None
    
    columns = [
        column.SelectionColumn( lambda item: str(item.version_id), name="selection"),
        column.GetterColumn( title=_(u"version"), getter=lambda i,f:i.version_id ),  
        column.GetterColumn( title=_(u"manual"), getter=lambda i,f:i.manual ),          
        column.GetterColumn( title=_(u"modified"), getter=lambda i,f: i.change.date ),
        column.GetterColumn( title=_(u"by"), getter=lambda i,f:i.change.user_id ),
        column.GetterColumn( title=_(u"message"), getter=lambda i,f:i.change.description ),
        ]    
    
    selection_column = columns[0]

    def __init__(self, context, request):
        super(VersionLogView, self).__init__(context.__parent__, request)
        
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
        self._versions.create( message = data['commit_message'], manual=True )        
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
        if len(selected) != 1:
            self.status = _(u"Select one item to display")
            return
            
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
        
    def __call__(self):
        self.update()
        return self.render()
