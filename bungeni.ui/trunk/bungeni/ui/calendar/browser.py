# encoding: utf-8

import time
import datetime
import tempfile
timedelta = datetime.timedelta

from zope import interface
from zope import component
from zope import schema
from zope.i18n import translate
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
from zope.datetime import rfc1123_date

from bungeni.ui.calendar import utils
from bungeni.ui.i18n import _
from bungeni.ui.utils import urljoin
from bungeni.ui.utils import is_ajax_request
from bungeni.ui.forms.common import set_widget_errors
from bungeni.core.location import location_wrapped
from bungeni.core.interfaces import ISchedulingContext
from bungeni.core.odf import OpenDocument
from bungeni.models.queries import get_parliament_by_date_range
from bungeni.models.queries import get_session_by_date_range
from bungeni.models import vocabulary
from bungeni.models.interfaces import IGroupSitting
from bungeni.server.interfaces import ISettings

from ploned.ui.interfaces import IViewView
from ploned.ui.interfaces import IStructuralView
from ore.alchemist.container import stringKey
from ore.alchemist import Session

from zc.resourcelibrary import need

class TIME_SPAN:
    daily = _(u"Daily")
    weekly = _(u"Weekly")

def get_scheduling_actions(scheduling, request):
    return get_actions("scheduling_actions", scheduling, request)

def get_sitting_actions(sitting, request):
    return get_actions("sitting_actions", sitting, request)

def get_discussion_actions(sitting, request):
    return get_actions("discussion_actions", sitting, request)

def get_actions(name, context, request):
    menu = component.getUtility(IBrowserMenu, name)
    items = menu.getMenuItems(context, request)

    site_url = absoluteURL(getSite(), request)
    url = absoluteURL(context, request)
    
    return [{
        'url': urljoin(url, item['action']),
        'title': item['title'],
        'id': item['title'].lower().replace(' ', '-'),
        'description': item['description'],
        'icon': urljoin(site_url, item['icon'])} for item in items
            ]

def get_sitting_items(sitting, request, include_actions=False):
    items = []

    schedulings = map(
        removeSecurityProxy,
        sitting.items.batch(order_by=("planned_order",), limit=None))

    for scheduling in schedulings:
        item = ProxyFactory(location_wrapped(scheduling.item, sitting))
       
        props = IDCDescriptiveProperties.providedBy(item) and item or \
                IDCDescriptiveProperties(item)

        discussions = tuple(scheduling.discussions.values())
        discussion = discussions and discussions[0] or None
        
        record = {
            'title': props.title,
            'description': props.description,
            'name': stringKey(scheduling),
            'status': item.status,
            'category_id': scheduling.category_id,
            'category': scheduling.category,
            'discussion': discussion,
            'delete_url': "%s/delete" % absoluteURL(scheduling, request),
            'url': absoluteURL(item, request)}
        
        if include_actions:
            record['actions'] = get_scheduling_actions(scheduling, request)

            discussion_actions = get_discussion_actions(discussion, request)
            if discussion_actions:
                assert len(discussion_actions) == 1
                record['discussion_action'] = discussion_actions[0]
            else:
                record['discussion_action'] = None
        items.append(record)
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
    for sitting in sittings.values():
        day = sitting.start_date.weekday()
        hour = sitting.start_date.hour

        start_date = utils.timedict(
            sitting.start_date.hour,
            sitting.start_date.minute)

        end_date = utils.timedict(
            sitting.end_date.hour,
            sitting.end_date.minute)

        mapping[day, hour] = {
            'url': "%s/schedule" % absoluteURL(sitting, request),
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

        group = self.context.get_group()
        if group is None:
            return template(
                display=None,
                status=_(u"Calendar is not available because "
                         "the scheduling group ($label) is inactive.",
                         mapping={'label': translate(self.context.label).lower()}
                         )
                )

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

class GroupSittingScheduleView(CalendarView):
    """Group-sitting scheduling view.

    This view presents a sitting and provides a user interface to
    manage the agenda.
    """

    interface.implementsOnly(IViewView)
    
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)

    def render(self, date, template=None):
        need('yui-editor')
        need('yui-resize')
        
        if template is None:
            template = self.template

        container = self.context.__parent__
        schedule_url = self.request.getURL()
        container_url = absoluteURL(container, self.request)
        
        # determine position in container
        key = stringKey(self.context)
        keys = list(container.keys())
        pos = keys.index(key)

        links = {}
        if pos > 0:
            links['previous'] = "%s/%s/%s" % (
                container_url, keys[pos-1], self.__name__)
        if pos < len(keys) - 1:
            links['next'] = "%s/%s/%s" % (
                container_url, keys[pos+1], self.__name__)

        start_date = utils.datetimedict.fromdatetime(self.context.start_date)
        end_date = utils.datetimedict.fromdatetime(self.context.end_date)
        
        session = Session()
        sitting_type_dc = IDCDescriptiveProperties(self.context.sitting_type)

        site_url = absoluteURL(getSite(), self.request)
        
        return template(
            display="sitting",
            title=_(u"$A $e, $B $Y", mapping=start_date),
            description=_(u"$type &mdash; ${start}-${end}", mapping={
                'type': translate(sitting_type_dc.title),
                'start': translate(u"$H:$M", mapping=start_date),
                'end': translate(u"$H:$M", mapping=end_date),
                }),
            links=links,
            actions=get_sitting_actions(self.context, self.request),
            items=get_sitting_items(
                self.context, self.request, include_actions=True),
            categories=vocabulary.ItemScheduleCategories(self.context),
            new_category_url="%s/calendar/categories/add?next_url=..." % site_url,
            )

class SittingCalendarView(CalendarView):
    """Sitting calendar view."""

    interface.implementsOnly(IViewView)
    
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)

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

    date = None

    def __init__(self, context, request):
        super(ReportingView, self).__init__(context, request)
        
        if IGroupSitting.providedBy(context):
            self.date = datetime.date(
                context.start_date.year,
                context.start_date.month,
                context.start_date.day) 
        
        while not ISchedulingContext.providedBy(context):
            context = context.__parent__
            if context is None:
                raise RuntimeError(
                    "No scheduling context found.")
        
        self.scheduling_context = context

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
            date = self.date or datetime.date.today()
            time_span = TIME_SPAN.daily

        self.adapters = {
            self.IReportingForm: context
            }
        
        self.widgets = form.setUpEditWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            adapters=self.adapters, ignore_request=ignore_request)

    def update(self):
        self.status = self.request.get('portal_status_message', '')
        super(ReportingView, self).update()
        set_widget_errors(self.widgets, self.errors)

    def validate(self, action, data):    
        errors = super(ReportingView, self).validate(action, data)

        start_date = data['date']
        end_date = self.get_end_date(start_date, data['time_span'])

        parliament = get_parliament_by_date_range(self, start_date, end_date)
        session = get_session_by_date_range(self, start_date, end_date)

        if parliament is None:
            errors.append(interface.Invalid(
                _(u"A parliament must be active in the period."),
                "date"))
        elif session is None:
            errors.append(interface.Invalid(
                _(u"A session must be active in the period."),
                "date"))

        return errors
    
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
        end_date = self.get_end_date(start_date, time_span)
        container = self.scheduling_context.get_sittings(
            start_date=start_date, end_date=end_date)
        return container.values()

    def get_end_date(self, start_date, time_span):
        if time_span is TIME_SPAN.daily:
            return start_date + timedelta(days=1)
        elif time_span is TIME_SPAN.weekly:
            return start_date + timedelta(weeks=1)
        
        raise RuntimeError("Unknown time span: %s." % time_span)
    
class AgendaReportingView(ReportingView):
    """Agenda report."""
    
    form_name = _(u"Agenda")
    report_name = _(u"ORDER OF THE DAY")
    form_description = _(u"This form generates the “order of the day” report.")
    odf_filename = "agenda.odt"
    display_minutes = False
    
    def get_archive(self, date, time_span):
        end_date = self.get_end_date(date, time_span)
        
        parliament = get_parliament_by_date_range(self, date, end_date)
        session = get_session_by_date_range(self, date, end_date)

        options = {
            'title': self.report_name,
            'date': _(u"$r", mapping=utils.datetimedict.fromdate(date)),
            'parliament': parliament,
            'session': session,
            'country': u"Republic of Kenya".upper(),
            'assembly': u"National Assembly".upper(),
            'sittings': self.get_sittings(date, time_span),
            'show_minutes': self.show_minutes,
            }
            
        document = self.get_odf_document()
        archive = tempfile.NamedTemporaryFile(suffix=".odt")
        document.process("content.xml", self, **options)
        document.save(archive.name)

        return archive
    
    def generate(self, date, time_span):
        archive = self.get_archive(date, time_span)
        file = File(archive, "application/vnd.oasis.opendocument.text")
        file.filename = "agenda-%s-%s-%s-%s.odt" % (
            str(time_span).lower(), date.year, date.month, date.day)
        
        return file
    
class VotesAndProceedingsReportingView(AgendaReportingView):
    form_name = _(u"Votes and proceedings")
    form_description = _(u"This form generates the “votes and proceedings” report.")
    report_name = _(u"VOTES AND PROCEEDINGS")
    display_minutes = True
    
    def generate(self, date, time_span):
        archive = self.get_archive(date, time_span)
        file = File(archive, "application/vnd.oasis.opendocument.text")
        file.filename = "votes-and-proceedings-%s-%s-%s-%s.odt" % (
            str(time_span).lower(), date.year, date.month, date.day)

        return file
