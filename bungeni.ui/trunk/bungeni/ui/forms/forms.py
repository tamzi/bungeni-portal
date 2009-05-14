# encoding: utf-8

import zope.security.management
import copy
import datetime

from sqlalchemy import sql

from zope import component
from zope.event import notify
from zope.formlib import form, namedtemplate
from zope.lifecycleevent import ObjectCreatedEvent
from zope import schema, interface
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.form.browser import MultiCheckBoxWidget
from zope.traversing.browser import absoluteURL
from zope.security.proxy import removeSecurityProxy
from ore.alchemist import Session
from alchemist.ui import generic

from bungeni.models import domain
from bungeni.models import interfaces
from bungeni.core import globalsettings as prefs
from bungeni.core.i18n import _
from bungeni.ui.queries import statements as sqlstatements
from bungeni.ui.queries import utils as sqlutils
from bungeni.ui.forms.workflow import createVersion
from bungeni.ui.forms import validations
from bungeni.ui.forms.common import ReorderForm
from bungeni.ui.forms.common import PageForm
from bungeni.ui.forms.common import AddForm
from bungeni.ui.forms.common import EditForm
from bungeni.ui.forms.common import DeleteForm
from bungeni.ui.widgets import SelectDateWidget
from bungeni.ui.widgets import MultiDateTextAreaWidget


FormTemplate = namedtemplate.NamedTemplateImplementation(
    ViewPageTemplateFile('templates/form.pt')
    )

ContentTemplate = namedtemplate.NamedTemplateImplementation(
    ViewPageTemplateFile('templates/content.pt')
    )

def hasDeletePermission(context):
    """Generic check if the user has rights to delete the object. The
    permission must follow the convention:
    ``bungeni.<classname>.Delete`` where 'classname' is the lowercase
    of the name of the python class.
    """
    
    interaction = zope.security.management.getInteraction()
    class_name = context.__class__.__name__ 
    permission_name = 'bungeni.' + class_name.lower() +'.Delete'
    return interaction.checkPermission(permission_name, context)

def set_widget_errors(widgets, errors):
    """Display invariant errors / custom validation errors in the
    context of the field."""

    for widget in widgets:
        name = widget.context.getName()
        for error in errors:
            if isinstance(error, interface.Invalid) and name in error.args[1:]:
                if widget._error is None:
                    widget._error = error

def flag_changed_widgets( widgets, context, data):
    for widget in widgets:
        name = widget.context.getName()
        # If the field is not in the data, then go on to the next one
        if name not in data:
            widget.changed = False
            continue
        if data[name] == getattr(context, name):
            widget.changed = False
        else:
            widget.changed = True  
    return []                  

class ResponseEditForm( EditForm ):
    """ Answer a Question
    UI for ministry to input response
    Display the question when adding the answer.
    """
    CustomValidations =  validations.null_validator

    
class ResponseAddForm( AddForm ):
    """
    Answer a Question
    UI for ministry to input response
    Display the question when adding the answer.
    """
    CustomValidation =  validations.null_validator

    
class ItemScheduleContainerReorderForm(ReorderForm):
    """Specialization of the general reorder form for item
    schedulings."""
    
    def save_ordering(self, ordering):
        for name, scheduling in self.context.items():
            scheduling.planned_order = ordering.index(name)

class ItemScheduleReorderForm(PageForm):
    """Form to reorder a scheduling within a list of schedulings."""

    class IReorderForm(interface.Interface):
        mode = schema.Choice(
            ('up', 'down'),
            title=_(u"Direction"),
            required=True)

    form_fields = form.Fields(IReorderForm)

    @form.action(_(u"Move"))
    def handle_move(self, action, data):
        """Move scheduling.

        This logic handles both reordering within the container and
        maintenance of category assignments.

        If we move up:

        - Next item inherits any assigned category
        - This item gets its category cleared

        If we move down:

        - We inherit category of the following item
        - Next item gets its category cleared 

        """

        mode = data['mode']
        container = self.context.__parent__
        name = self.context.__name__
        schedulings = container.batch(order_by=("planned_order",), limit=None)
        ordering = [scheduling.__name__ for scheduling in schedulings]
        index = ordering.index(name)
        category = self.context.category

        swap_category_with = None
        
        if mode == 'up':
            if category and index < len(ordering) + 1:
                prev = container[ordering[index+1]]
                prev.category_id = self.context.category_id
                self.context.category_id = None
            elif index > 0:
                prev = container[ordering[index-1]]
                planned_order = self.context.planned_order
                self.context.planned_order = prev.planned_order
                prev.planned_order = planned_order
                swap_category_with = prev
                
        if mode == 'down':
            if index < len(ordering) + 1:
                next = container[ordering[index+1]]
                
                # if next item has a category, swap, reset and skip
                # reordering
                if next.category_id is not None:
                    self.context.category_id = next.category_id
                    next.category_id = None
                else:
                    planned_order = self.context.planned_order
                    self.context.planned_order = next.planned_order
                    next.planned_order = planned_order
                    swap_category_with = next
                    
        if swap_category_with is not None:
            category_id = self.context.category_id
            self.context.category_id = swap_category_with.category_id
            swap_category_with.category_id = category_id

class ItemScheduleDeleteForm(DeleteForm):
    def get_subobjects(self):
        items = []
        discussion = self.context.discussion
        if discussion is not None:
            items.append(discussion)
        return items

    def delete_subobjects(self):
        """Delete subobjects.

        1) For category maintenance, move the scheduling to the bottom
        of the container.
        
        2) Delete any discussion items that have been associated to
        this scheduling.
        """
        
        reorder_form = ItemScheduleReorderForm(self.context, self.request)
        container = copy.copy(removeSecurityProxy(self.context.__parent__))
        subset_query = container.subset_query
        container.subset_query = sql.and_(
            subset_query,
            container.domain_model.planned_order > self.context.planned_order)
        for i in range(len(container) * 2):
            reorder_form.handle_move.success({'mode': 'down'})
        container.subset_query = subset_query
        if self.context.category:
            results = container._query.filter(
                sql.operators.lt(
                    container.domain_model.planned_order,
                    self.context.planned_order))[:-1]
            if results:
                results[0].category_id = self.context.category_id

        count = 0
        session = Session()
        unproxied = removeSecurityProxy(self.context)
        for key, discussion in unproxied.discussions.items():
            del unproxied.discussions[key]
            session.delete(discussion)
            count += 1
        return count

class GroupSittingAddForm(AddForm):
    """Add group-sittings form.

    This form includes functionality to create recurring events, which
    we'll test here.

      >>> from bungeni.models import domain
      >>> from bungeni.models import interfaces
      >>> from bungeni.models import testing
      
      >>> from bungeni.ui.calendar.utils import nth_day_of_week
      >>> db = testing.setup_db()

      >>> from ore.alchemist import Session
      >>> session = Session()

      >>> from zope.publisher.base import TestRequest
      >>> request = TestRequest('/sittings/add')
      >>> from datetime import datetime, date

    Add a parliament to be there parent of the group sittings
    container.

      >>> group = testing.add_content(domain.Group,
      ...    start_date=date(1999, 1, 1),
      ...    end_date=date(1999, 12, 31),
      ...    short_name=u'Test group')
      
      >>> parliament = testing.add_content(
      ...    domain.Parliament,
      ...    short_name=u'Test parliament',
      ...    start_date=date(1999, 1, 1),
      ...    end_date=date(1999, 12, 31),
      ...    election_date=datetime(1999, 1, 1),
      ...    group=group)

      >>> sittings = parliament.sittings

    Instantiate form and invoke factory.
    
      >>> form = GroupSittingAddForm(sittings, request)

      >>> data = {
      ...     'start_date': datetime(1999, 10, 1, 9, 0),
      ...     'end_date': datetime(1999, 10, 1, 12, 0),
      ...     'weekdays': [nth_day_of_week(0),
      ...                  nth_day_of_week(3)],
      ...     'repeat': 5}

      >>> validations.validate_recurring_sittings(
      ...    None, data, None, sittings)
      []
      
      >>> sitting = form.createAndAdd(data)

    Verify start- and end date of primary sitting.
    
      >>> sitting.start_date
      datetime.datetime(1999, 10, 1, 9, 0)

      >>> sitting.end_date
      datetime.datetime(1999, 10, 1, 12, 0)

    Verify creation of recurring events.

      >>> len(sittings)
      6

    Asking to create another set of sittings will fail because of
    validation constraints.

      >>> validations.validate_recurring_sittings(
      ...    None, data, None, sittings)
      [Invalid(...overlaps...)]

    Demonstrate date edge-case:
    
      >>> data.update({
      ...     'start_date': datetime(1999, 10, 1, 7, 0),
      ...     'end_date': datetime(1999, 10, 1, 17, 0)})

      >>> validations.validate_recurring_sittings(
      ...    None, data, None, sittings)
      [Invalid(...overlaps...)]

    Cleanup.

      >>> session.flush()  
      >>> session.close() 

    """
    
    class IRecurringEvents(interface.Interface):
        weekdays = schema.List(
            title=_(u"Weekdays"),
            description=_(u"Select the days on which the event should occur."),
            required=False,
            value_type=schema.Choice(
                vocabulary="bungeni.vocabulary.weekdays"),
            )

        monthly = schema.Choice(
            title=_(u"Montly"),
            description=_(u"Select the mode of montly recurrence."),
            vocabulary="bungeni.vocabulary.monthly_recurrence",
            required=False)

        repeat = schema.Int(
            title=_(u"Repeat"),
            description=_(u"Enter the number of times which the event should be "
                          "repeated (as an integer)."),
            required=False)

        repeat_until = schema.Date(
            title=_(u"Repeat until date"),
            description=_(u"Limit recurrence to the specified date."),
            required=False)

        exceptions = schema.List(
            title=_(u"Exceptions"),
            description=_(u"Events will not be scheduled at dates appearing "
                          "in this field. Separate with comma or newline. Format: "
                          "YYYY/MM/DD."),
            value_type=schema.Date(),
            required=False)

        @interface.invariant
        def must_limit_recurrence(recurring):
            if recurring.weekdays or recurring.monthly:
                if recurring.repeat or recurring.repeat_until:
                    return
                raise interface.Invalid(
                    _(u"Must limit recurrence (by number or date)."),
                    "repeat", "repeat_until")

    legends = {
        IRecurringEvents: _(u"Recurring events"),
        }

    def CustomValidation(self, context, data):
        return validations.validate_recurring_sittings(
            None, data, context, self.context)

    def get_form_fields(self):
        fields = super(GroupSittingAddForm, self).get_form_fields()
        fields += form.Fields(self.IRecurringEvents)
        def MultiCheckBoxWidgetFactory(field, request):
            return MultiCheckBoxWidget(
                field, field.value_type.vocabulary, request)
        fields['weekdays'].custom_widget = MultiCheckBoxWidgetFactory
        fields['repeat_until'].custom_widget = SelectDateWidget
        fields['exceptions'].custom_widget = MultiDateTextAreaWidget
        return fields

    def createAndAdd(self, data):
        objs = []
        def finishConstruction(ob):
            super(GroupSittingAddForm, self).finishConstruction(ob)
            objs.extend(self.createRecurringSittings(ob, data.copy()))
        self.finishConstruction = finishConstruction
        self.form_fields = super(
            GroupSittingAddForm, self).get_form_fields()

        ob = super(GroupSittingAddForm, self).createAndAdd(data)
        
        for obj in objs:
            obj.recurring_id = ob.sitting_id

        return ob

    def createRecurringSittings(self, ob, data):
        start = data['start_date']
        end = data['end_date']
        weekdays = data.get('weekdays')
        monthly = data.get('monthly')
        repeat = data.get('repeat')
        repeat_until = data.get('repeat_until')
        exceptions = data.get('exceptions', ())

        objs = []
        session = Session()
        group_id = self.context.__parent__.group_id
        group = session.query(domain.Group).get(group_id)
        
        if repeat or repeat_until:
            for date in validations.generate_recurring_sitting_dates(
                start.date(), repeat, repeat_until, weekdays, monthly, exceptions):
                # create the object, inspect data for constructor args

                data['start_date'] = datetime.datetime(
                    date.year, date.month, date.day, start.hour, start.minute)
                data['end_date'] = datetime.datetime(
                    date.year, date.month, date.day, end.hour, end.minute)

                try:
                    ob = generic.createInstance(self.domain_model, data)
                except TypeError:
                    ob = self.domain_model()

                form.applyChanges(ob, self.form_fields, data, {})
                ob.group_id = group_id
                
                session.save(ob)
                notify(ObjectCreatedEvent(ob))

                objs.append(ob)

        return objs
