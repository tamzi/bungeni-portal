from zope import interface
from zope.schema.interfaces import IVocabularyFactory
from zope.schema import vocabulary
from zope.i18n import translate

from i18n import _

import datetime

from bungeni.ui.calendar.utils import first_nth_weekday_of_month
from bungeni.ui.calendar.utils import nth_day_of_month
from bungeni.ui.calendar.utils import nth_day_of_week

days = [_('day_%d' % index, default=default)
        for (index, default) in enumerate(
            (u"Mon", u"Tue", u"Wed", u"Thu", u"Fri", u"Sat", u"Sun"))]

class WeekdaysVocabulary(object):
    interface.implements(IVocabularyFactory)
        
    def __call__(self, context):
        return vocabulary.SimpleVocabulary(
            [vocabulary.SimpleTerm(
                nth_day_of_week(index), str(index), msg)
             for (index, msg) in enumerate(days)])

WeekdaysVocabularyFactory = WeekdaysVocabulary()

class MonthlyRecurrenceVocabulary(object):
    """This vocabulary provides an option to choose between different
    modes of monthly recurrence.

    Vocabulary values are methods which take a date and generate
    future dates.
    """
    
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        today = datetime.date.today()
        weekday = today.weekday()
        day = today.day

        return vocabulary.SimpleVocabulary(
            (vocabulary.SimpleTerm(
                nth_day_of_month(day),
                "day_%d_of_every_month" % day,
                _(u"Day $number of every month", mapping={'number': day})),
             vocabulary.SimpleTerm(
                 first_nth_weekday_of_month(weekday),
                 "first_%s_of_every_month" % today.strftime("%a"),
                 _(u"First $day of every month", mapping={'day': translate(
                     today.strftime("%A"))})),
                 ))
                
MonthlyRecurrenceVocabularyFactory = MonthlyRecurrenceVocabulary()
