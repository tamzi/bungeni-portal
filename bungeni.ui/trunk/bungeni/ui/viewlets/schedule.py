# encoding: utf-8

from zope import interface
from zope import component

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.dublincore.interfaces import IDCDescriptiveProperties
from zope.traversing.browser import absoluteURL
from zope.location.interfaces import ILocation
from zope.viewlet import viewlet
from zc.resourcelibrary import need

from bungeni.core.workflows.question import states as question_wf_state
from bungeni.core.workflows.motion import states as motion_wf_state
from bungeni.core.workflows.bill import states as bill_wf_state
from bungeni.models import domain
from bungeni.models.interfaces import IBungeniApplication

from ore.alchemist import Session
from ore.alchemist.container import stringKey
from ore.alchemist.container import contained
from ore.alchemist.model import queryModelDescriptor
from ore.workflow.interfaces import IWorkflow

from bungeni.ui.i18n import _

class SchedulablesViewlet(viewlet.ViewletBase):
    """Renders a portlet which calls upon the scheduling viewlet
    manager to render a list of schedulable items."""

    render = ViewPageTemplateFile('templates/scheduling.pt')
    title = _(u"Scheduling")

class SchedulableItemsViewlet(viewlet.ViewletBase):
    """Renders a list of schedulable items for a particular ``model``,
    filtered by workflow ``states``.

    Must subclass.
    """

    model = states = container = None
    
    render = ViewPageTemplateFile('templates/schedulable_items.pt')

    @property
    def title(self):
        descriptor = queryModelDescriptor(self.container.domain_model)
        return descriptor.container_name

    @property
    def app(self):
        parent = self.context.__parent__
        while parent is not None:
            if IBungeniApplication.providedBy(parent):
                return parent
            parent = parent.__parent__
        raise ValueError("Unable to locate application.")

    @property
    def container(self):
        gsm = component.getSiteManager()
        adapter = gsm.adapters.lookup(
            (interface.implementedBy(self.model),
             interface.providedBy(self)), ILocation)        
        return adapter.container
    
    def update(self):
        need('yui-dragdrop')
        need('yui-container')
        
        session = Session()
        items = session.query(self.model).filter(
            self.model.status.in_(self.states))

        # add location to items
        items = [contained(item, self.container, stringKey(item))
                 for item in items]

        # for each item, format dictionary for use in template
        self.items = [{
            'title': properties.title,
            'name': type(item).__name__,
            'description': properties.description,
            'date': item.changes[-1].date,
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
