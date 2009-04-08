from zope import component
from zope.lifecycleevent.interfaces import IObjectCreatedEvent

import domain

@component.adapter(domain.ItemSchedule, IObjectCreatedEvent)
def create_discussion_for_item_scheduling(context, event):
    context.discussion = domain.ScheduledItemDiscussion()
