# encoding: utf-8

import time
import datetime
import tempfile
timedelta = datetime.timedelta

from zope import interface
from zope import component
from zope import schema
from zope.formlib import form
from zope.formlib import namedtemplate

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
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.app.file.file import File
from zope.app.file.browser.file import FileView
from zope.app.publisher.browser import queryDefaultViewName
from zope.datetime import rfc1123_date

from bungeni.core.interfaces import ISchedulingContext
from bungeni.core.schedule import DailySchedulingContext
from bungeni.ui.forms.forms import FormTemplate
from bungeni.ui.calendar import utils
from bungeni.ui.i18n import _
from bungeni.ui.utils import urljoin
from bungeni.ui.utils import is_ajax_request
from bungeni.core.location import location_wrapped
from bungeni.core.proxy import LocationProxy
from bungeni.server.interfaces import ISettings
from bungeni.core.odf import OpenDocument

from ploned.ui.interfaces import IViewView
from ploned.ui.interfaces import IStructuralView
from ore.alchemist.container import stringKey

class TIME_SPAN:
    daily = _(u"Daily")
    weekly = _(u"Weekly")

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

class ReportingView(form.PageForm):
    """Reporting view base class.

    The context of the view is a scheduling context, which always
    relates to a principal group, e.g. 'Plenary'.

    A starting date must be specified, as well as a time span
    parameter, which can be one of the following:

    - Daily
    - Weekly

    The time span parameter is used as title and to generate canonical
    filenames and unique identification strings for publishing the
    reports, e.g.

      'Daily agenda 2009/30/12' (agenda-daily-2009-30-12.pdf)

    It's not enforced that weeks begin on Mondays or any other
    particular day; a week is always 7 days.

    A report is a listing of sittings that take place in the defined
    period. For each sitting, the summary may be different depending
    on the type of report. The ``get_sittings`` method will fetch the
    relevant sittings.
    """

    class IReportingForm(interface.Interface):
        date = schema.Date(
            title=_(u"Date"),
            description=_(u"Choose a starting date for this report."),
            required=True)
        
        time_span = schema.Choice(
            title=_(u"Time span"),
            description=_("The time span is used to define the reporting interval "
                          "and will provide a name for the report."),
            vocabulary=SimpleVocabulary((
                SimpleTerm(TIME_SPAN.daily, "daily", TIME_SPAN.daily),
                SimpleTerm(TIME_SPAN.weekly, "weekly", TIME_SPAN.weekly),)),
            required=True)

    template = namedtemplate.NamedTemplate('alchemist.form')
    form_fields = form.Fields(IReportingForm)
    odf_filename = None
    
    def get_odf_document(self):
        assert self.odf_filename is not None
        settings = component.getUtility(ISettings)
        filename = "%s/%s" % (settings['templates'], self.odf_filename)
        return OpenDocument(filename)

    def setUpWidgets(self, ignore_request=False):
        class context:
            date = datetime.date.today()
            time_span = TIME_SPAN.daily

        self.adapters = {
            self.IReportingForm: context
            }
        
        self.widgets = form.setUpEditWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            adapters=self.adapters, ignore_request=ignore_request)
    
    @form.action(_(u"Preview"))
    def handle_preview(self, action, data):
        return self.download_preview(
            data['date'], data['time_span'], 'inline')

    @form.action(_(u"Download"))
    def handle_download(self, action, data):
        return self.download_preview(
            data['date'], data['time_span'], 'attachment')

    def download_preview(self, date, time_span, disposition):
        file = self.generate(date, time_span)
        self.request.response.setHeader('Content-Type', file.contentType)
        self.request.response.setHeader('Content-Length', file.getSize())
        self.request.response.setHeader(
            'Content-Disposition', '%s; filename="%s"' % (
                disposition, file.filename))
        self.request.response.setHeader('Last-Modified', rfc1123_date(time.time()))
        self.request.response.setHeader(
            'Cache-Control', 'no-cache, must-revalidate');
        self.request.response.setHeader('Pragma', 'no-cache')
        return file.data

    def generate(self, date, time_span):
        raise NotImplementedError("Must be implemented by subclass.")

    def get_sittings(self, start_date, time_span):
        if time_span is TIME_SPAN.daily:
            end_date = start_date + timedelta(days=1)
        elif time_span is TIME_SPAN.weekly:
            end_date = start_date + timedelta(weeks=1)
        else:
            raise RuntimeError("Unknown time span: %s." % time_span)
        return self.context.get_sittings(
            start_date=start_date, end_date=end_date)

class AgendaReportingView(ReportingView):
    """Agenda report."""
    
    form_name = _(u"Agenda")
    form_description = _(u"This form generates the “order of the day” report.")
    odf_filename = "agenda.odt"
    
    def generate(self, date, time_span):
        options = {
            'date': _(u"$r", mapping=utils.datetimedict.fromdate(date)),
            'parliament_name': _(u'Tenth Parliament'),
            'session_name': _(u'Second Session'),
            'sittings': self.get_sittings(date, time_span),
            }
            
        document = self.get_odf_document()
        archive = tempfile.NamedTemporaryFile(suffix=".odt")
        document.process("content.xml", self, **options)
        document.save(archive.name)

        file = File(archive, "application/vnd.oasis.opendocument.text")
        file.filename = "agenda-%s-%s-%s-%s.odt" % (
            str(time_span).lower(), date.year, date.month, date.day)
        
        return file
    
class VotesAndProceedingsReportingView(ReportingView):
    form_name = _(u"Votes and proceedings")
    form_description = _(u"This form generates the “votes and proceedings” report.")
    odf_filename = "votes-and-proceedings.odt"
    
    def generate(self, date, time_span):
        sittings = self.get_sittings(date, time_span)
        file = File(u"Votes and proceedings", "text/plain")
        file.filename = "votes-and-proceedings-%s-%s-%s-%s" % (
            str(time_span).lower(), date.year, date.month, date.day)
        return file
