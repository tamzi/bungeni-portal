# encoding: utf-8
# Calendar for scheduling parliamentary or group sitting items
# at the top  you have a calendar that displays the sittings
# below the items available for scheduling are displayed
# to schedule drag the item to be scheduled to the sitting

import datetime
import calendar

from zope.viewlet import viewlet
from zope.publisher.browser import BrowserView
from zope.viewlet.manager import WeightOrderedViewletManager
import zope.interface
from zope.app.pagetemplate import ViewPageTemplateFile

from zc.resourcelibrary import need


import sqlalchemy.sql.expression as sql

from ore.alchemist import Session

import bungeni.core.globalsettings as prefs

from bungeni.ui.utils import getDisplayDate

import interfaces
from schedule import makeList


class Calendar(BrowserView):
    __call__ = ViewPageTemplateFile("templates/schedule_sitting_items.pt")


#class ScheduleCalendarViewletManager( WeightOrderedViewletManager ):
#    """
#    manage the viewlets that make up the calendar view
#    """
#    zope.interface.implements(IScheduleCalendar) 


class ScheduleItemCalendar( viewlet.ViewletBase):
    """
    display the calendar with the sittings 
    and the items which are scheduled for the sitting
    """
    
    
