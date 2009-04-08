import datetime
timedelta = datetime.timedelta

from zope import interface
from zope import component

from zope.location.interfaces import ILocation
from zope.dublincore.interfaces import IDCDescriptiveProperties
from zope.publisher.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.traversing.browser import absoluteURL
from zope.app.component.hooks import getSite
from zope.security.proxy import removeSecurityProxy
from zope.security.proxy import ProxyFactory
from zope.publisher.interfaces import IPublishTraverse

from bungeni.core.interfaces import ISchedulingContext
from bungeni.core.schedule import DailySchedulingContext
from bungeni.ui.calendar import utils
from bungeni.ui.i18n import _
from bungeni.ui.utils import urljoin
from bungeni.ui.utils import is_ajax_request
from bungeni.core.location import location_wrapped
from bungeni.core.proxy import LocationProxy

from ploned.ui.interfaces import IViewView
from ploned.ui.interfaces import IStructuralView

from ore.alchemist.container import stringKey

def get_sitting_actions(sitting, request):
    menu = component.getUtility(IBrowserMenu, "sitting_actions")
    items = menu.getMenuItems(sitting, request)

    site_url = absoluteURL(getSite(), request)
    url = absoluteURL(sitting, request)
    
    return [{
        'url': urljoin(url, item['action']),
        'title': item['title'],
        'id': item['title'].lower().replace(' ', '-'),
        'description': item['description'],
        'icon': urljoin(site_url, item['icon'])} for item in items
            ]

def get_sitting_items(sitting, request):
    items = []

    schedulings = map(
        removeSecurityProxy,
        sitting.items.batch(order_by=("planned_order",), limit=None))

    for scheduling in schedulings:
        item = ProxyFactory(location_wrapped(scheduling.item, sitting))
       
        props = IDCDescriptiveProperties.providedBy(item) and item or \
                IDCDescriptiveProperties(item)
        
        items.append({
            'title': props.title,
            'description': props.description,
            'name': stringKey(scheduling),
            'delete_url': "%s/delete" % absoluteURL(scheduling, request),
            'url': absoluteURL(item, request)})

    return items

def create_sittings_map(sittings, request):
    """Returns a dictionary that maps:

      (day, hour) -> {
         'record'   : sitting database record
         'actions'  : actions that apply to this sitting
         'class'    : sitting
         'span'     : span
         }
         
      (day, hour) -> ``None``
      
    If the mapped value is a sitting, then a sitting begins on that
    day and hour, if it's ``None``, then a sitting is reaching into
    this day and hour.
    
    The utility of the returned structure is to aid rendering a
    template with columns spanning several rows.
    """

    mapping = {}
    for sitting in sittings:
        day = sitting.start_date.weekday()
        hour = sitting.start_date.hour

        start_date = utils.timedict(
            sitting.start_date.hour,
            sitting.start_date.minute)

        end_date = utils.timedict(
            sitting.end_date.hour,
            sitting.end_date.minute)

        mapping[day, hour] = {
            'url': absoluteURL(sitting, request),
            'items': get_sitting_items(sitting, request),
            'record': sitting,
            'class': u"sitting",
            'actions': get_sitting_actions(sitting, request),
            'span': sitting.end_date.hour - sitting.start_date.hour,
            'formatted_start_time': _(u"$R", mapping=start_date),
            'formatted_end_time': _(u"$R", mapping=end_date),
        }
        
        # make sure start- and end-date is the same year
        assert (sitting.start_date.day == sitting.end_date.day) and \
               (sitting.start_date.month == sitting.end_date.month) and \
               (sitting.start_date.year == sitting.end_date.year)

        for hour in range(sitting.start_date.hour+1, sitting.end_date.hour):
            mapping[day, hour] = None

    return mapping

class CalendarView(BrowserView):
    """Main calendar view."""

    interface.implements(IViewView, IStructuralView)

    template = ViewPageTemplateFile("main.pt")
    ajax = ViewPageTemplateFile("ajax.pt")
    
    _macros = ViewPageTemplateFile("macros.pt")

    short_name = u"Calendar"
    
    def __init__(self, context, request):
        super(CalendarView, self).__init__(
            ISchedulingContext(context), request)

        self.context.__name__ = self.__name__
        self.context.title = self.short_name
        interface.alsoProvides(self.context, ILocation)
        interface.alsoProvides(self.context, IDCDescriptiveProperties)
        self.__parent__ = context

    def __call__(self, timestamp=None):
        if timestamp is None:
            # start the week on the first weekday (e.g. Monday)
            date = utils.datetimedict.fromdate(datetime.date.today())
        else:
            try:
                timestamp = float(timestamp)
            except:
                raise TypeError(
                    "Timestamp must be floating-point (got %s)." % timestamp)
            date = utils.datetimedict.fromtimestamp(timestamp)

        if is_ajax_request(self.request):
            return self.render(date, template=self.ajax)
        return self.render(date)

    def publishTraverse(self, request, name):
        traverser = component.getMultiAdapter(
            (self.context, request), IPublishTraverse)
        return traverser.publishTraverse(request, name)

    def render(self, date, template=None):
        if template is None:
            template = self.template
            
        calendar_url = self.request.getURL()
        date = date - timedelta(days=date.weekday())
        today = utils.datetimedict.fromdate(datetime.date.today())
        days = tuple(date + timedelta(days=d) for d in range(7))

        sittings = self.context.get_sittings(
            start_date=date,
            end_date=days[-1],
            )

        return template(
            display="weekly",
            title=_(u"$B $Y", mapping=date),
            days=[{
                'formatted': datetime.datetime.strftime(day, '%A %d'),
                'id': datetime.datetime.strftime(day, '%Y-%m-%d'),
                'today': day == today,
                'url': "%s/%d" % (calendar_url, day.totimestamp()),
                } for day in days],
            hours=range(6,21),
            week_no=date.isocalendar()[1],
            links={
                'previous': "%s?timestamp=%s" % (
                    calendar_url, (date - timedelta(days=7)).totimestamp()),
                'next': "%s?timestamp=%s" % (
                    calendar_url, (date + timedelta(days=7)).totimestamp()),
                },
            sittings_map = create_sittings_map(sittings, self.request),
            )

    @property
    def macros(self):
        return self._macros.macros

class CommitteeCalendarView(CalendarView):
    """Calendar-view for a committee."""

class DailyCalendarView(CalendarView):
    """Daily calendar view."""

    interface.implementsOnly(IViewView)
    
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)

    def render(self, today, template=None):
        if template is None:
            template = self.template

        calendar_url = absoluteURL(self.context.__parent__, self.request)
        date = removeSecurityProxy(self.context.date)

        sittings = self.context.get_sittings()
        
        return template(
            display="daily",
            title=_(u"$B $Y", mapping=date),
            day={
                'formatted': datetime.datetime.strftime(date, '%A %d'),
                'id': datetime.datetime.strftime(date, '%Y-%m-%d'),
                'today': date == today,
                'url': "%s/%d" % (calendar_url, date.totimestamp()),
                },
            hours=range(6,21),
            week_no=date.isocalendar()[1],
            week_day=date.weekday(),
            links={
                'previous': "%s/%d" % (
                    calendar_url, (date - timedelta(days=1)).totimestamp()),
                'next': "%s/%d" % (
                    calendar_url, (date + timedelta(days=1)).totimestamp()),
                },
            sittings_map = create_sittings_map(sittings, self.request),
            )



    
