from datetime import datetime
from datetime import timedelta

from zope import interface
from zope import component
from zope import schema

from zope.publisher.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile

from zc.resourcelibrary import need

from bungeni.ui.calendar import utils
from bungeni.ui.i18n import _

class CalendarView(BrowserView):
    """Main calendar view."""

    template = ViewPageTemplateFile("main.pt")
    _macros = ViewPageTemplateFile("macros.pt")
    
    def __call__(self):
        # start the week on the first weekday (e.g. Monday)
        date = utils.datetimedict.now()
        date = date - timedelta(days=date.weekday())

        days = tuple(date + timedelta(days=d) for d in range(7))
        return self.template(
            display="weekly",
            formatted_date=_(
                u"Showing the week starting on $M/$d-$g @ $r.",
                mapping=date),
            formatted_month=_(u"$B", mapping=date),
            days=[{
                'formatted': datetime.strftime(day, '%A %d'),
                'id': datetime.strftime(day, '%Y-%m-%d'),
                } for day in days],
            hours=range(7,21),
            week_no=date.isocalendar()[1],
            )

    @property
    def macros(self):
        return self._macros.macros
