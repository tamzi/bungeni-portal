from zope import interface
from zope.formlib import form
from zope.traversing.browser import absoluteURL 

from alchemist.catalyst import ui
from alchemist.ui.core import null_validator
from ore.alchemist.model import queryModelDescriptor

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
