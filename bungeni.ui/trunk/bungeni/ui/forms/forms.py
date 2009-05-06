# encoding: utf-8

import zope.security.management
import copy
from sqlalchemy import sql

from zope import component
from zope.formlib import form, namedtemplate
from zope import schema, interface
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.traversing.browser import absoluteURL 
from zope.security.proxy import removeSecurityProxy
from ore.workflow import interfaces
from ore.alchemist import Session

from bungeni.models import domain
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
