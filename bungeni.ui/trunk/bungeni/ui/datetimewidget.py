### -*- coding: utf-8 -*- #############################################

import datetime, pytz

from zope.component import getMultiAdapter
from zope.app.form.interfaces import ConversionError, InputErrors
from zope.app.form.browser.widget import SimpleInputWidget, renderElement
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from bungeni.core.i18n import _
from zope.interface.common import idatetime

#months = [_(u'January'),_(u'February'),_(u'March'),_(u'April'),_(u'May'),_(u'June'),
#          _(u'July'),_(u'August'),_(u'September'),_(u'October'),_(u'November'),_(u'December')]

class SelectDateWidget( SimpleInputWidget):
    """ A more user freindly date input """
    
    __call__ = ViewPageTemplateFile('templates/datewidget.pt')
    
    _missing = u''
    minYear = None
    maxYear = None

    minYearDelta = 100
    maxYearDelta = 5
    
    @property
    def time_zone( self ):
        try:
            time_zone = idatetime.ITZInfo(self.request)
        except TypeError:
            time_zone = pytz.UTC
        return time_zone

    def _days(self):
        dl = []
        for i in range( 1, 32 ):
            dl.append( '%02d' % (i) )
        return dl            
        

    def _months(self):
        """ return a dict of month values and names"""
        months = [
            { 'num' : '01' , 'name' : _(u'January')},
            { 'num' : '02' , 'name' : _(u'February')},
            { 'num' : '03' , 'name' : _(u'March')},
            { 'num' : '04' , 'name' : _(u'April')},
            { 'num' : '05' , 'name' : _(u'May')},
            { 'num' : '06' , 'name' : _(u'June')},
            { 'num' : '07' , 'name' : _(u'July')},
            { 'num' : '08' , 'name' : _(u'August')},
            { 'num' : '09' , 'name' : _(u'September')},
            { 'num' : '10' , 'name' : _(u'October')},
            { 'num' : '11' , 'name' : _(u'November')},
            { 'num' : '12' , 'name' : _(u'December')}
            ]
        return months
        
    @property    
    def _years(self):
        minYear = self.minYear
        if minYear is None:
            minYear = datetime.date.today().year - int(self.minYearDelta)
        maxYear = self.maxYear
        if maxYear is None:
            maxYear = datetime.date.today().year + int(self.maxYearDelta)
        return range( minYear, maxYear + 1 )                     
    
    @property
    def _day_name(self):
        return self.name.replace(".","__") + '__day'

    @property
    def _month_name(self):
        return self.name.replace(".","__") + '__month'

    @property
    def _year_name(self):
        return self.name.replace(".","__") + '__year'
        
 
    def hasInput(self):
        """Widgets need to determine whether the request contains an input
        value for them """
        return (self._day_name in self.request.form and \
                self._month_name in self.request.form and \
                self._year_name in self.request.form)

    def _hasPartialInput(self):
        return self._day_name in self.request.form or \
               self._month_name in self.request.form or \
               self._year_name in self.request.form
     
    
        
    def _getFormInput(self):
        """extract the input value from the submitted form """
        return (self._getFieldInput(self._day_name),
                self._getFieldInput(self._month_name),
                self._getFieldInput(self._year_name))

                
    def _getFieldInput(self, name):
        return self.request.form.get(name, self._missing)                
    
    def _toFieldValue(self, (day, month, year)):
        """convert the input value to an value suitable for the field."""
        if day == self._missing or month == self._missing or year == self._missing:
            if self.required:
                return self.context.missing_value
            else:        
                if day + month + year == self._missing:
                    return None
                else:
                    return self.context.missing_value
        else:
            try:
                time_zone = self.time_zone
                return datetime.datetime(year=int(year), month=int(month), day=int(day), tzinfo=time_zone )
            except ValueError, e:
                raise ConversionError(_(u"Incorrect string data for date"), e)                
                
    
    def _toFormValue(self, value):
        """convert a field value to a string that can be inserted into the form"""        
        if (value == self.context.missing_value) and self.required:
            d = datetime.date.today()
            return (d.day, d.month, d.year)
        else:
            try:
                return (value.day, value.month, value.year)                
            except:
                return( '0', '0', '0')
            
             
    def _getFormValue(self):
        """
        Returns a field value to a string that can be inserted into the form. 
        The difference to _toFormValue is that it takes into account when a form
        has already been submitted but needs to be re-rendered (input error)  
        """
        if not self._renderedValueSet():
            if self._hasPartialInput():
                error = self._error
                try:
                    try:
                        value = self.getInputValue()
                    except InputErrors:
                        return self._getFormInput()
                finally:
                    self._error = error
            else:
                if self.required:
                    value = self._getDefault()
                else:
                    value = None    
        else:
            value = self._data
        return self._toFormValue(value)
      
class SelectDateTimeWidget(SelectDateWidget):        

    __call__=ViewPageTemplateFile('templates/datetimewidget.pt')
    
    @property
    def _hour_name(self):
        return self.name.replace(".","__") + '__hour'

    @property
    def _minute_name(self):
        return self.name.replace(".","__") + '__minute'



    def hasInput(self):
        return super(SelectDateTimeWidget, self).hasInput() and \
                    self._hour_name in self.request.form and \
                    self._minute_name in self.request.form
    def _hasPartialInput(self):
        return super(SelectDateTimeWidget, self)._hasPartialInput() or \
            self._hour_name in self.request.form or \
            self._minute_name in self.request.form 

    def _getFormInput(self):
        return super(SelectDateTimeWidget, self)._getFormInput() +\
                    (self._getFieldInput(self._hour_name),
                    self._getFieldInput(self._minute_name))

    def _hours(self):
        hl = []
        for i in range( 0, 24 ):
            hl.append( '%02d' % (i) )
        return hl

    def _minutes(self):
        ml = []
        for i in range( 0, 60 ):
            ml.append( '%02d' % (i) )
        return ml

    def _toFormValue(self, value):
        if value == self.context.missing_value and self.required:
            d = datetime.datetime.now()
            return (d.day, d.month, d.year, d.hour, d.minute)
        else:
            try:
                return (value.day, value.month, value.year, value.hour, value.minute)
            except:                
                return ( '0', '0', '0', '0', '0')
                
    def _toFieldValue(self, (day, month, year, hour, minute)):
        if day == self._missing or month == self._missing or year == self._missing \
                                or hour == self._missing or minute == self._missing:
            if self.required:
                return self.context.missing_value
            else:
                if day + month + year + hour + minute == self._missing:
                    return None
                else:
                    return self.context.missing_value              
        else:
            try:    
                time_zone = self.time_zone                          
                return datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), tzinfo=time_zone)
            except ValueError, e:
                raise ConversionError(_(u"Incorrect string data for date and time"), e)
                            
                            
