import operator

from zope import interface
from zope import component
from zope import schema

from zope.publisher.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.publisher.browser import queryDefaultViewName
from zope.formlib import form
from zope.security.proxy import removeSecurityProxy
from zope.security import canWrite
from zope.security.interfaces import ForbiddenAttribute
from zope.traversing.browser import absoluteURL

from sqlalchemy import orm

from ore.alchemist.interfaces import IIModelInterface

from bungeni.ui.i18n import MessageFactory as _
from bungeni.ui.table import TableFormatter
from bungeni.core.interfaces import IVersioned

from alchemist.ui.core import BaseForm, getSelected
from zc.table import  column

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

class VersionLogView(BaseForm):
    class IVersionEntry(interface.Interface):
        commit_message = schema.Text(title=_(u"Change Message"))

    form_fields = form.Fields(IVersionEntry)
    formatter_factory = TableFormatter
    
    render = ViewPageTemplateFile('templates/version.pt')
    extra = None
    
    columns = [
        column.SelectionColumn(lambda item: str(item.version_id), name="selection"),
        column.GetterColumn(
            title=_(u"version"),
            getter=lambda i,f: '<a href="%s">%d</a>' % (
                "%s/versions/obj-%d" % (f.url, i.version_id), i.version_id)),
        column.GetterColumn(title=_(u"manual"), getter=lambda i,f:i.manual),
        column.GetterColumn(title=_(u"modified"), getter=lambda i,f: i.change.date.strftime('%Y-%m-%d %H:%M')),
        column.GetterColumn(title=_(u"by"), getter=lambda i,f:i.change.user_id),
        column.GetterColumn(title=_(u"message"), getter=lambda i,f:i.change.description ),
        ]
    
    selection_column = columns[0]

    def __init__(self, context, request):
        super(VersionLogView, self).__init__(context.__parent__, request)
        
    def listing(self):
        # set up table
        values = list(self._versions.values())
        values.sort(key=operator.attrgetter('version_id'))
        values.reverse()
        formatter = self.formatter_factory(
            self.context, self.request,
            values,
            prefix="results",
            visible_column_names = [c.name for c in self.columns],
            columns = self.columns)

        # the column getter methods expect an ``url`` attribute
        formatter.url = absoluteURL(self.context, self.request)

        # update and render
        formatter.updateBatching()
        return formatter()

    def has_write_permission(self, context):
        """check that  the user has the rights to edit 
             the object, if not we assume he has no rights 
             to make a version             
             assumption is here that if he has the rights on any of the fields
             he may create a version."""  
        trusted = removeSecurityProxy( self.context)                
        table = orm.class_mapper(trusted.__class__).mapped_table   
        for column in table.columns:
            try:
                if canWrite(self.context, column.name):
                    return True
            except ForbiddenAttribute:
                pass                    
        else:
            return False

            
    @form.action(label=_("New Version"), condition=has_write_permission)
    def handle_new_version( self, action, data ):
        self._versions.create( message = data['commit_message'], manual=True )        
        self.status = _(u"New Version Created")

    @form.action(label=_("Revert To"), condition=has_write_permission)
    def handle_revert_version( self, action, data):
        selected = getSelected( self.selection_column, self.request )  
        if len(selected) != 1:
            self.status = _("Select one item to revert to.")
            return                          
        version = self._versions.get( selected[0] )
        message = data['commit_message']
        self._versions.revert( version, message )
        self.status = (_(u"Reverted to Previous Version %s") %(version.version_id))

    @form.action(
        label=_("Show Differences"), name="diff",        
        validator=lambda form, action, data: ())
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
            if source.version_id > target.version_id:
                t = source
                source = target
                target = t            
        except:
            target = context
                                      
        view = z3c.schemadiff.browser.DiffView(source, target, self.request)

        self.extra = view(
            *filter(IIModelInterface.providedBy, interface.providedBy(context)))

    def setUpWidgets( self, ignore_request=False):
        # setup widgets in data entry mode not bound to context
        actions = self.actions
        self.actions = []
        for action in actions:
            if getattr(action, 'condition', None):
                if action.condition(self, self.context):
                    self.actions.append(action) 
            else:
                self.actions.append(action)           
        if not self.has_write_permission(self.context):                                        
            self.form_fields = self.form_fields.omit('commit_message')
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
