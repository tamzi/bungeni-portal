# encoding: utf-8

from zope import interface
from zope import component

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.dublincore.interfaces import IDCDescriptiveProperties
from zope.traversing.browser import absoluteURL
from zope.location.interfaces import ILocation
from zope.viewlet import viewlet
from zc.resourcelibrary import need
from zope.app.component.hooks import getSite

from bungeni.core.workflows.question import states as question_wf_state
from bungeni.core.workflows.motion import states as motion_wf_state
from bungeni.core.workflows.bill import states as bill_wf_state
from bungeni.core.workflows.agendaitem import states as agendaitem_wf_state
from bungeni.core.workflows.tableddocument import states as tableddocument_wf_state
from bungeni.models import domain
from bungeni.models.interfaces import IBungeniApplication
from bungeni.core.interfaces import ISchedulingContext

from ore.alchemist import Session
from ore.alchemist.container import stringKey
from ore.alchemist.container import contained
from ore.alchemist.model import queryModelDescriptor
from ore.workflow.interfaces import IWorkflow

from bungeni.ui.i18n import _
from bungeni.ui.calendar.utils import datetimedict

class SchedulablesViewlet(viewlet.ViewletBase):
    """Renders a portlet which calls upon the scheduling viewlet
    manager to render a list of schedulable items."""

    render = ViewPageTemplateFile('templates/scheduling.pt')
    title = _(u"Scheduling")

    def __init__(self, context, request, view, manager):
        while not ISchedulingContext.providedBy(context):
            context = ISchedulingContext(context, context.__parent__)
            if context is None:
                raise RuntimeError("Unable to locate a scheduling context.")
        super(SchedulablesViewlet, self).__init__(
            context, request, view, manager)

class SchedulableItemsViewlet(viewlet.ViewletBase):
    """Renders a list of schedulable items for a particular ``model``,
    filtered by workflow ``states``.

    Must subclass.
    """

    model = states = container = None

    render = ViewPageTemplateFile('templates/schedulable_items.pt')

    @property
    def app(self):
        parent = self.context.__parent__
        while parent is not None:
            if IBungeniApplication.providedBy(parent):
                return parent
            parent = parent.__parent__
        raise ValueError("Unable to locate application.")

    def update(self):
        need('yui-dragdrop')
        need('yui-container')

        session = Session()
        items = tuple(session.query(self.model).filter(
            self.model.status.in_(self.states)))

        # add location to items
        gsm = component.getSiteManager()
        adapter = gsm.adapters.lookup(
            (interface.implementedBy(self.model),
             interface.providedBy(self)), ILocation)

        items = [adapter(item, None) for item in items]

        # for each item, format dictionary for use in template
        self.items = [{
            'title': properties.title,
            'name': item.__class__.__name__,
            'description': properties.description,
            'date': _(u"$F", mapping=
                      datetimedict.fromdatetime(item.changes[-1].date)),
            'state': IWorkflow(item).workflow.states[item.status].title,
            'id': item.parliamentary_item_id,
            'url': absoluteURL(item, self.request)} for item, properties in \
            [(item, (IDCDescriptiveProperties.providedBy(item) and item or \
            IDCDescriptiveProperties(item))) for
             item in items]]

class SchedulableBillsViewlet(SchedulableItemsViewlet):
    model = domain.Bill

    states = (
        bill_wf_state[u"submitted"].id,
        bill_wf_state[u"first_reading"].id,        
        bill_wf_state[u"first_reading_postponed"].id,
        bill_wf_state[u"second_reading"].id,
        bill_wf_state[u"second_reading_postponed"].id,
        bill_wf_state[u"whole_house"].id,
        bill_wf_state[u"whole_house_postponed"].id,
        bill_wf_state[u"report_reading"].id,
        bill_wf_state[u"report_reading_postponed"].id,
        bill_wf_state[u"third_reading"].id,
        bill_wf_state[u"third_reading_postponed"].id,
        )

class SchedulableQuestionsViewlet(SchedulableItemsViewlet):
    model = domain.Question

    states = (
        question_wf_state[u"admissible"].id,
        question_wf_state[u"postponed"].id,
        )

class SchedulableMotionsViewlet(SchedulableItemsViewlet):
    model = domain.Motion

    states = (
        motion_wf_state[u"admissible"].id,
        motion_wf_state[u"postponed"].id,
        )
        
class SchedulableAgendaItemsViewlet(SchedulableItemsViewlet):
    model = domain.AgendaItem

    states = (
        agendaitem_wf_state[u"admissible"].id,
        agendaitem_wf_state[u"postponed"].id,
        )
        
class SchedulableTabledDocumentsViewlet(SchedulableItemsViewlet):
    model = domain.TabledDocument

    states = (
        tableddocument_wf_state[u"admissible"].id,
        tableddocument_wf_state[u"postponed"].id,
        )
                         
        
