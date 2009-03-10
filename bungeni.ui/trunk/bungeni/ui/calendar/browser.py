from datetime import datetime
from datetime import timedelta

from zope import interface
from zope import component
from zope import schema

from zope.location.interfaces import ILocation
from zope.publisher.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile

from zc.resourcelibrary import need

from bungeni.ui.calendar import utils
from bungeni.ui.i18n import _

class CalendarView(BrowserView):
    """Main calendar view."""

    template = ViewPageTemplateFile("main.pt")
    _macros = ViewPageTemplateFile("macros.pt")

    def __init__(self, context, request):
        super(CalendarView, self).__init__(context, request)
    
    def __call__(self, timestamp=None):
        if timestamp is None:
            # start the week on the first weekday (e.g. Monday)
            date = utils.datetimedict.now()
        else:
            try:
                timestamp = float(timestamp)
            except:
                raise TypeError(
                    "Timestamp must be floating-point (got %s)." % timestamp)
            date = utils.datetimedict.fromtimestamp(timestamp)

        return self.render_weekly(date)
    
    def render_weekly(self, date):
        calendar_url = self.request.getURL()
        date = date - timedelta(days=date.weekday())
        days = tuple(date + timedelta(days=d) for d in range(7))
        
        return self.template(
            display="weekly",
            formatted_date=_(
                u"Showing the week starting on $m/$d-$g @ $r.",
                mapping=date),
            formatted_month=_(u"$B", mapping=date),
            days=[{
                'formatted': datetime.strftime(day, '%A %d'),
                'id': datetime.strftime(day, '%Y-%m-%d'),
                } for day in days],
            hours=range(7,21),
            week_no=date.isocalendar()[1],
            links={
                'previous_week': "%s?timestamp=%s" % (
                    calendar_url, (date - timedelta(days=7)).totimestamp()),
                'next_week': "%s?timestamp=%s" % (
                    calendar_url, (date + timedelta(days=7)).totimestamp()),

                # note that giving a date -28 or +32 days in the future
                # will work, because we always start the calendar on a
                # fixed day of the week
                'previous_month': "%s?timestamp=%s" % (
                    calendar_url, (date - timedelta(days=28)).totimestamp()),
                'next_month': "%s?timestamp=%s" % (
                    calendar_url, (date + timedelta(days=32)).totimestamp()),
                },
            )

    @property
    def macros(self):
        return self._macros.macros
