from datetime import datetime
from datetime import timedelta

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

from bungeni.core.interfaces import ISchedulingContext
from bungeni.ui.calendar import utils
from bungeni.ui.i18n import _
from bungeni.ui.utils import urljoin
from bungeni.ui.utils import is_ajax_request
from bungeni.core.location import location_wrapped
from bungeni.core.proxy import LocationProxy
from ploned.ui.interfaces import IViewView

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

    for scheduling in sitting.items.batch(order_by=("planned_order",), limit=None):
        item = location_wrapped(scheduling.item, sitting)
       
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

        mapping[day, hour] = {
            'url': absoluteURL(sitting, request),
            'items': get_sitting_items(sitting, request),
            'record': sitting,
            'class': u"sitting",
            'actions': get_sitting_actions(sitting, request),
            'span': sitting.end_date.hour - sitting.start_date.hour
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

    interface.implements(IViewView)

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
            date = utils.datetimedict.now()
        else:
            try:
                timestamp = float(timestamp)
            except:
                raise TypeError(
                    "Timestamp must be floating-point (got %s)." % timestamp)
            date = utils.datetimedict.fromtimestamp(timestamp)

        if is_ajax_request(self.request):
            return self.render_weekly(date, template=self.ajax)
        return self.render_weekly(date)

    def publishTraverse(self, request, name):
        try:
            method = getattr(self, 'get_%s' % name)
        except AttributeError:
            return super(CalendarView, self).publishTraverse(request, name)

        obj = method()
        return ProxyFactory(LocationProxy(
            removeSecurityProxy(obj), container=self.context, name=name))

    def get_group(self):
        return self.context.get_group()

    def render_weekly(self, date, template=None):
        if template is None:
            template = self.template
            
        calendar_url = self.request.getURL()
        date = date - timedelta(days=date.weekday())
        days = tuple(date + timedelta(days=d) for d in range(7))

        sittings = self.context.get_sittings(
            start_date=date,
            end_date=days[-1],
            )

        return template(
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
            sittings_map = create_sittings_map(sittings, self.request),
            )

    @property
    def macros(self):
        return self._macros.macros
