# encoding: utf-8

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.dublincore.interfaces import IDCDescriptiveProperties
from zope.traversing.browser import absoluteURL
from zope.viewlet import viewlet
from zc.resourcelibrary import need

from bungeni.core.workflows.question import states as question_wf_state
from bungeni.core.workflows.motion import states as motion_wf_state
from bungeni.core.workflows.bill import states as bill_wf_state
from bungeni.models import domain

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

    @property
    def container(self):
        return self.context.__parent__['bills']
    
    states = (
        bill_wf_state[u"billstates.submitted"].id,
        bill_wf_state[u"billstates.first_reading_postponed"].id,
        bill_wf_state[u"billstates.second_reading"].id, 
        bill_wf_state[u"billstates.second_reading_postponed"].id, 
        bill_wf_state[u"billstates.whole_house"].id,
        bill_wf_state[u"billstates.whole_house_postponed"].id,
        bill_wf_state[u"billstates.report_reading"].id,
        bill_wf_state[u"billstates.report_reading_postponed"].id,
        bill_wf_state[u"billstates.third_reading"].id,
        bill_wf_state[u"billstates.third_reading_postponed"].id,
        )
    
class SchedulableQuestionsViewlet(SchedulableItemsViewlet):
    model = domain.Question

    @property
    def container(self):
        return self.context.__parent__['questions']
    
    states = (
        question_wf_state[u"questionstates.admissible"].id,
        question_wf_state[u"questionstates.postponed"].id,
        )

class SchedulableMotionsViewlet(SchedulableItemsViewlet):
    model = domain.Motion

    @property
    def container(self):
        return self.context.__parent__['motions']

    states = (
        motion_wf_state[u"motionstates.admissible"].id,
        motion_wf_state[u"motionstates.postponed"].id,
        )

    
