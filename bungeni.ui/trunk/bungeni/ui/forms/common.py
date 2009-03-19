import logging
import transaction

from zope import interface
from zope.event import notify
from zope.formlib import form
from zope.formlib.namedtemplate import NamedTemplate
from zope.traversing.browser import absoluteURL
from zope.container.contained import ObjectRemovedEvent
from zope.app.pagetemplate import ViewPageTemplateFile
from alchemist.catalyst import ui
from alchemist.ui.core import null_validator
from ore.alchemist.model import queryModelDescriptor

try:
    from sqlalchemy.exceptions import IntegrityError
except ImportError:
    from sqlalchemy.exc import IntegrityError

from bungeni.core.i18n import _

TRUE_VALS = "true", "1"

def set_widget_errors(widgets, errors):
    for widget in widgets:
        name = widget.context.getName()
        for error in errors:
            if isinstance(error, interface.Invalid) and name in error.args[1:]:
                if widget._error is None:
                    widget._error = error

class NoPrefix(unicode):
    """The ``formlib`` library insists on concatenating the form
    prefix with field names; we override the ``__add__`` method to
    prevent this.
    """
    
    def __add__(self, name):
        return name

NO_PREFIX = NoPrefix()

class DefaultAction(form.Action):
    def __init__(self, action):
        self.__dict__.update(action.__dict__)
        
    def submitted(self):
        return True

class AddForm(ui.AddForm):
    """Custom add-form for Bungeni content.

    Headless submission

        This add-form adds support for 'headless' submission, relying
        only on the schema field ids. The headless mode is enabled by
        giving a true value for the request parameter ``headless``.
        In this mode, no form prefix is applied and the default action
        is always executed.

    Custom validation

        The ``CustomValidation`` attribute is queried for extra validation
        steps to be performed.

    Redirection

        If ``next_url`` is provided, a redirect is issued upon
        successful form submission.

    In addition, additional actions are set up to allow users to
    continue editing an object, or add another of the same kind.
    """

    Adapts = None
    CustomValidation = None

    def __init__(self, *args):
        super(AddForm, self).__init__(*args)

        if self.request.get("headless", "").lower() in TRUE_VALS:
            self.setPrefix(NO_PREFIX)

            # in headless mode, the first action defined is submitted
            # by default
            default_action = tuple(self.actions)[0]
            self.actions = form.Actions(
                DefaultAction(default_action))

        # the ``_next_url`` attribute is used internally by our
        # superclass to implement formlib's ``nextURL`` method
        self._next_url = self.request.get('next_url', None)

    def __call__(self):
        return super(AddForm, self).__call__()
    
    @property
    def form_name( self ):
        descriptor = queryModelDescriptor( self.context.domain_model )
        
        if descriptor:
            name = getattr(descriptor, 'display_name', None)
            
        if not name:
            name = getattr( self.context.domain_model, '__name__', None)                
        return _(u"add_item_legend", default=u"Add $name",
                 mapping={'name': name.lower()})

    def update(self):
        self.status = self.request.get('portal_status_message', '')
        form.AddForm.update( self )
        set_widget_errors(self.widgets, self.errors)

    def finishConstruction(self, ob):
        """Adapt the custom fields to the object."""

        adapts = self.Adapts
        if adapts is None:
            adapts = self.model_schema
            
        self.adapters = {
            adapts : ob
            }

    def validate(self, action, data):    
        """Validation that require context must be called here,
        invariants may be defined in the descriptor."""

        errors = (
            form.getWidgetsData(self.widgets, self.prefix, data) +
            form.checkInvariants(self.form_fields, data))

        if self.CustomValidation is not None:
            errors += self.CustomValidation(self.context, data)

        return errors
    
    @form.action(_(u"Save"), condition=form.haveInputWidgets)
    def handle_add_save(self, action, data ):
        """After succesful content creation, redirect to the content listing."""

        self.createAndAdd(data)
        name = self.context.domain_model.__name__

        if not self._next_url:
            self._next_url = absoluteURL(
                self.context, self.request) + \
                '?portal_status_message=%s added' % name
        
    @form.action(_(u"Cancel"), validator=null_validator )
    def handle_cancel( self, action, data ):
        """Cancelling redirects to the listing."""

    @form.action(_(u"Save and continue editing"),
                 condition=form.haveInputWidgets, validator='validateAdd')
    def handle_add_edit( self, action, data ):
        ob = self.createAndAdd( data )
        name = self.context.domain_model.__name__

        if not self._next_url:        
            self._next_url = absoluteURL(ob, self.request ) + \
                             "/@@edit?portal_status_message=%s Added" % name
        
    @form.action(_(u"Save and add another"), condition=form.haveInputWidgets)
    def handle_add_and_another(self, action, data ):
        self.createAndAdd( data )
        name = self.context.domain_model.__name__

        if not self._next_url:
            self._next_url = absoluteURL(self.context, self.request) + \
                             '/@@add?portal_status_message=%s Added' % name

class DeleteForm(form.PageForm):
    """Delete-form for Bungeni content.

    Confirmation

        The user is presented with a confirmation form which details
        the items that are going to be deleted.

    Subobjects

        Recursively, a permission check is carried out for each item
        that is going to be deleted. If a permission check fails, an
        error message is displayed to the user.

    Will redirect back to the container on success.
    """

    form_template = NamedTemplate('alchemist.form')
    template = ViewPageTemplateFile("templates/delete.pt")

    _next_url = None
    form_fields = form.Fields()
    
    def _can_delete_item(self, action):
        return True

    def nextURL(self):
        return self._next_url

    def update(self):
        self.subobjects = self.get_subobjects()
        super(DeleteForm, self).update()

    def get_subobjects(self):
        return ()
        
    @form.action(_(u"Delete"), condition=_can_delete_item)
    def handle_delete(self, action, data):
        for subobject in self.subobjects:
            raise NotImplementedError(
                "Can't delete subobjects.")

        container = self.context.__parent__

        del container[self.context.__name__]
        
        try:
            transaction.commit()
        except IntegrityError, e:
            # this should not happen in production; it's a critical
            # error, because the transaction might have failed in the
            # second phase of the commit
            transaction.abort()
            logging.critical(e)

            self.status = _(u"Could not delete item due to "
                            "database integrity error.")

            return self.render()
    
        notify(ObjectRemovedEvent(
            self.context, oldParent=container, oldName=self.context.__name__))
        count = 1

        self.request.response.redirect(
            absoluteURL(container, self.request) + \
            '/@@add?portal_status_message=%d items deleted' % count)
