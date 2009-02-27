from zope import interface
from zope.publisher.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.formlib import form

from ore.alchemist.interfaces import IIModelInterface

from bungeni.ui.i18n import MessageFactory as _

class BaseView(BrowserView):
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
