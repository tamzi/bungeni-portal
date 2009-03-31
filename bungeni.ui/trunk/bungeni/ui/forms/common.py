import logging
import transaction

from zope.publisher.interfaces import BadRequest
from zope import component
from zope import interface
from zope import schema
from zope.i18n import translate
from zope.security.proxy import removeSecurityProxy
from zope.event import notify
from zope.schema.interfaces import IChoice
from zope.formlib import form
from zope.location.interfaces import ILocation
from zope.dublincore.interfaces import IDCDescriptiveProperties
from zope.formlib.namedtemplate import NamedTemplate
from zope.traversing.browser import absoluteURL
from zope.container.contained import ObjectRemovedEvent
from zope.app.pagetemplate import ViewPageTemplateFile
from alchemist.catalyst import ui
from alchemist.ui.core import null_validator
from ore.alchemist.model import queryModelDescriptor
from ore.alchemist.container import stringKey
from ore.workflow.interfaces import IWorkflowInfo
from alchemist.ui.core import handle_edit_action
from alchemist.ui.core import setUpFields
from zope.app.form.interfaces import IDisplayWidget

try:
    from sqlalchemy.exceptions import IntegrityError
except ImportError:
    from sqlalchemy.exc import IntegrityError

from bungeni.core.translation import get_language_by_name
from bungeni.core.translation import get_default_language
from bungeni.core.translation import is_translation
from bungeni.core.interfaces import IVersioned
from bungeni.core.i18n import _
from bungeni.models.interfaces import IVersion
from ploned.ui.interfaces import IViewView

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

class BaseForm(object):
    """Base form class for Bungeni content.

    Headless submission

        Adds support for 'headless' submission, relying only on the
        schema field ids. The headless mode is enabled by giving a
        true value for the request parameter ``headless``.  In this
        mode, no form prefix is applied and the default action is
        always executed.

    Custom validation

        The ``CustomValidation`` attribute is queried for extra validation
        steps to be performed.

    Redirection

        If ``next_url`` is provided, a redirect is issued upon
        successful form submission.
    """

    Adapts = None
    CustomValidation = None
    
    def __init__(self, *args):
        super(BaseForm, self).__init__(*args)

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
        
    def update(self):
        self.status = self.request.get('portal_status_message', '')
        super(BaseForm, self).update()
        set_widget_errors(self.widgets, self.errors)

    def validate(self, action, data):    
        """Validation that require context must be called here,
        invariants may be defined in the descriptor."""

        errors = (
            form.getWidgetsData(self.widgets, self.prefix, data) +
            form.checkInvariants(self.form_fields, data))

        if self.CustomValidation is not None:
            errors += self.CustomValidation(self.context, data)

        return errors

class DisplayForm(ui.DisplayForm):
    interface.implements(IViewView)
        
    template = ViewPageTemplateFile('templates/content-view.pt')

class AddForm(BaseForm, ui.AddForm):
    """Custom add-form for Bungeni content.

    Additional actions are set up to allow users to continue editing
    an object, or add another of the same kind.
    """

    interface.implements(ILocation, IDCDescriptiveProperties)

    description = None
    
    def validate(self, action, data):    
        errors = super(AddForm, self).validate(action, data)

        descriptor = queryModelDescriptor(self.domain_model)
        for validator in getattr(descriptor, "custom_validators", ()):
            errors += validator(action, data, None, self.context)
        
        return errors

    def update(self):
        super(AddForm, self).update()

        # set default values for required choice fields
        for widget in self.widgets:
            field = widget.context
            if IChoice.providedBy(field) and field.required and field.default is None:
                for term in field.vocabulary:
                    field.default = term.value

    @property
    def domain_model(self):
        return self.context.domain_model

    @property
    def type_name( self ):
        descriptor = queryModelDescriptor(self.domain_model)
        
        if descriptor:
            name = getattr(descriptor, 'display_name', None)
            
        if not name:
            name = getattr( self.domain_model, '__name__', None)

        return name

    @property
    def form_name(self):
        return _(u"add_item_legend", default=u"Add $name",
                 mapping={'name': self.type_name.lower()})

    @property
    def title(self):
        return _(u"add_item_title", default=u"Adding $name",
                 mapping={'name': self.type_name.lower()})

    def finishConstruction(self, ob):
        """Adapt the custom fields to the object."""

        adapts = self.Adapts
        if adapts is None:
            adapts = self.model_schema
            
        self.adapters = {
            adapts : ob
            }

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

class EditForm(BaseForm, ui.EditForm):
    """Custom edit-form for Bungeni content."""

    @property
    def is_translation(self):
        return is_translation(self.context)

    @property
    def side_by_side(self):
        return self.is_translation

    @property
    def form_name(self):
        if IVersion.providedBy(self.context):
            context = self.context.head

        props = IDCDescriptiveProperties.providedBy(context) \
                and context or IDCDescriptiveProperties(context)

        if self.is_translation:
            language = get_language_by_name(self.context.language)
            return _(u"edit_translation_legend",
                     default=u'Editing $language translation of "$title"',
                     mapping={'title': translate(props.title, context=self.request),
                              'language': language})
        
        elif IVersion.providedBy(self.context):
            return _(u"edit_version_legend",
                     default=u'Editing "$title" (version $version)',
                     mapping={'title': translate(props.title, context=self.request),
                              'version': self.context.version_id})

        return _(u"edit_item_legend", default=u'Editing "$title"',
                 mapping={'title': translate(props.title, context=self.request)})

    @property
    def form_description(self):
        if self.is_translation:
            language = get_language_by_name(self.context.head.language)
            return _(u"edit_translation_help",
                     default=u'The original $language version is shown on the left.',
                     mapping={'language': language})
            
    def validate(self, action, data):    
        errors = super(EditForm, self).validate(action, data)

        descriptor = queryModelDescriptor(self.context.__class__)
        for validator in getattr(descriptor, "custom_validators", ()):
            errors += validator(action, data, self.context, self.context.__parent__)
        
        return errors

    def setUpWidgets(self, ignore_request=False):
        super(EditForm, self).setUpWidgets(ignore_request=ignore_request)

        # for translations, add a ``render_original`` method to each
        # widget, which will render the display widget bound to the
        # original (HEAD) document
        if self.is_translation:
            head = self.context.head
            form_fields = setUpFields(self.context.__class__, "view")
            for widget in self.widgets:
                form_field = form_fields.get(widget.context.__name__)
                if form_field is None:
                    form_field = form.Field(widget.context)

                # bind field to head document
                field = form_field.field.bind(head)

                # create custom widget or instantiate widget using
                # component lookup
                if form_field.custom_widget is not None:
                    display_widget = form_field.custom_widget(
                        field, self.request)
                else:
                    display_widget = component.getMultiAdapter(
                        (field, self.request), IDisplayWidget)
                
                display_widget.setRenderedValue(field.get(head))

                # attach widget as ``render_original``
                widget.render_original = display_widget

class TranslateForm(AddForm):
    """Custom translate-form for Bungeni content.

    When a translation is saved, a new version is created.
    """

    def __init__(self, *args):
        super(TranslateForm, self).__init__(*args)
        self.language = self.request.get('language', get_default_language())
        
    @property
    def form_name(self):
        language = get_language_by_name(self.language)
                
        return _(u"translate_item_legend",
                 default=u"Add $language translation",
                 mapping={'language': language})

    @property
    def form_description(self):
        language = get_language_by_name(self.language)
        props = IDCDescriptiveProperties.providedBy(self.context) \
                and self.context or IDCDescriptiveProperties(self.context)
                
        return _(
            u"translate_item_help",
            default=u'The document "$title" has not yet been translated into $language. Use this form to add the translation.',
            mapping={'title': translate(props.title, context=self.request),
                     'language': language})

    @property
    def title(self):
        language = get_language_by_name(self.language)

        return _(u"translate_item_title", default=u"Adding $language translation",
                 mapping={'language': language})

    @property
    def domain_model(self):
        return type(removeSecurityProxy(self.context))

    def setUpAdapters(self, context):
        interfaces = set(field.interface for field in self.form_fields)
        self.adapters = {}
        for iface in interfaces:
            self.adapters[iface] = context

    def setUpWidgets(self, ignore_request=False):
        self.setUpAdapters(self.context)
        self.widgets = form.setUpEditWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            adapters=self.adapters, ignore_request=ignore_request)

        language = self.request.get('language')
        if language is not None:
            widget = self.widgets['language']

            try:
                widget.vocabulary.getTermByToken(language)
            except LookupError:
                raise BadRequest("No such language token: '%s'." % language)

            # if the term exists in the vocabulary, set the value on
            # the widget
            widget.setRenderedValue(language)

    @form.action(_(u"Save translation"), condition=form.haveInputWidgets)
    def handle_add_save(self, action, data ):
        """After succesful creation of translation, redirect to the
        view."""

        url = absoluteURL(self.context, self.request)
        
        language = get_language_by_name(data['language'])
        versions = IVersioned(self.context)
        version = versions.create("'%s' translation added." % language)

        # reset workflow state
        version.status = None
        IWorkflowInfo(version).fireTransition("create-translation")

        # redefine form context and proceed with edit action
        self.setUpAdapters(version)
        handle_edit_action(self, action, data)

        # commit version such that it gets a version id
        transaction.commit()
        
        if not self._next_url:
            self._next_url = ( \
                '%s/versions/%s' % (url, stringKey(version)) + \
                '?portal_status_message=Translation added')

        self._finished_add = True
        
class ReorderForm(BaseForm, form.PageForm):
    """Item reordering form.

    We use an intermediate list of ids to represent the item order.

    Note that this form must be subclassed with the ``save_ordering``
    method overriden.
    """

    class IReorderForm(interface.Interface):
        ordering = schema.List(
            title=u"Ordering",
            value_type=schema.TextLine())

    template = NamedTemplate('alchemist.form')
    form_name = _(u"Item reordering")
    form_fields = form.Fields(IReorderForm, render_context=True)

    def setUpWidgets(self, ignore_request=False):
        class context:
            ordering = list(self.context)

        self.adapters = {
            self.IReorderForm: context,
            }

        self.widgets = form.setUpWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            form=self, adapters=self.adapters, ignore_request=ignore_request)

    def save_ordering(self, ordering):
        raise NotImplementedError("Must be defined by subclass.")
    
    @form.action(_(u"Save"))
    def handle_save(self, action, data):
        self.save_ordering(data['ordering'])

class DeleteForm(BaseForm, form.PageForm):
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
