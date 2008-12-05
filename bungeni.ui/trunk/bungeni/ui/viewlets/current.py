# encoding: utf-8
#
# dislay the current parliament/government with its subitems
# at a given date (defaults to current date)

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.publisher.browser import BrowserView
from zope.viewlet.manager import WeightOrderedViewletManager
from zope.viewlet import viewlet, interfaces
from zope.security import proxy
from zope.traversing.browser import absoluteURL

import zc.resourcelibrary

import zope.interface
import datetime

from bungeni.ui.i18n import MessageFactory as _
import bungeni.core.domain as domain
import bungeni.core.schema as schema
from bungeni.core.interfaces import IGroupSitting, IGroupSittingAttendance, IGroupSittingAttendanceContainer
from bungeni.core.orm import _ugm_party

from ore.alchemist import Session
from ore.alchemist.interfaces import IAlchemistContainer, IAlchemistContent

from interfaces import ICurrent, ICurrentGovernment, ITabManager
from bungeni.ui.utils import getDisplayDate, getFilter

import sqlalchemy.sql.expression as sql
import simplejson


def getDateFilter(request):
    displayDate = getDisplayDate(request) 
    if not displayDate:
        displayDate = datetime.date.today()       
    if displayDate:
        filter_by='?date=' + datetime.date.strftime(displayDate,'%Y-%m-%d')
    else:
        filter_by = ''
    return filter_by        

class Current(BrowserView):
    __call__ = ViewPageTemplateFile("templates/current.pt")

class Government( BrowserView ):
    __call__ = ViewPageTemplateFile("templates/current-gov.pt")

class CurrentViewletManager( WeightOrderedViewletManager ):
    """Current viewlet manager."""
    zope.interface.implements(ICurrent) 

class DateChooserViewletManager( interfaces.IViewletManager ):
    """ Viewlet manager for Date chooser """
    #zope.interface.implements(IDateChooser)        
 
class CurrentGovernmentViewletManager( WeightOrderedViewletManager ):
    """Current viewlet manager."""
    zope.interface.implements(ICurrentGovernment)           
    
class TabManager( WeightOrderedViewletManager ):
    """YUI Tab manager."""
    zope.interface.implements(ITabManager) 
    
class YUITabView( viewlet.ViewletBase ):       
    """
    get the JS into the form
    """
    for_display = True
    def render( self ):
        zc.resourcelibrary.need("yui-tab")   
        yuijs ="""
             <script type="text/javascript">
                (function() {
                     var bungeni_tabView = new YAHOO.widget.TabView();
                   	 var elements = YAHOO.util.Dom.getElementsByClassName('listing', 'div', 'bungeni-tabbed-nav' ); 
                   	 
                   	 for (i=0; i < elements.length; i++) 
                   	    {
                   	        tab_label = YAHOO.util.Dom.getFirstChild(elements[i])
                   	        bungeni_tabView.addTab( new YAHOO.widget.Tab({ 
                   	            labelEl : tab_label,
                   	            contentEl : elements[i]
                   	            }));
                   	    };
                   	        	    
                   	 bungeni_tabView.appendTo('bungeni-tabbed-nav');    
                   	 bungeni_tabView.set('activeTab', bungeni_tabView.getTab(0));
                   	 })();
             </script>    
	       """     
        return yuijs
    
def getOrder( request, context_class ):
    """
    get the sort order
    """    
    order_list = []
    order_by = request.get('order_by', None)
    
    return order_list
    
class DateChooserViewlet( viewlet.ViewletBase ):
    """
    display a calendar to choose the date which to display the information for
    """    
    for_display = True
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager       
        self.Date=datetime.date.today()
        self.error = None
        self.error_message = None
        self.StartDateStr =None
        self.EndDateStr=None
        
               
        
    def _getDateConstraints(self):
        """
        get the start, end date of the parent
        """     
        if  IAlchemistContent.providedBy(self.context):
            start_date = getattr( self.context, 'start_date', None)
            if type(start_date) == datetime.datetime:
                start_date = start_date.date() 
            end_date = getattr( self.context, 'end_date', None)            
            if type(end_date) == datetime.datetime:
                end_date = end_date.date()
            return start_date, end_date                
        if IAlchemistContainer.providedBy(self.context):                        
            if IAlchemistContent.providedBy(self.context.__parent__):
                parent = self.context.__parent__
                start_date = getattr( parent, 'start_date', None)   
                if type(start_date) == datetime.datetime:
                    start_date = start_date.date()         
                end_date = getattr( parent, 'end_date', None)
                if type(end_date) == datetime.datetime:
                    end_date = end_date.date()
                return start_date, end_date            
        return None, None #datetime.date(1900,1,1), datetime.date(2100,1,1)


    def checkDateInConstraints(self):
        """
        check if the date is in the constraints of the parent
        """
        if self.Date:
            start_date, end_date = self._getDateConstraints()
            if start_date:
                if self.Date < start_date:
                    return start_date
            if end_date:
                if self.Date > end_date:
                    return end_date                    
        return None
            
    def getDateChooserJs(self):
        js_string = """
           YAHOO.util.Event.onDOMReady(function(){
           var dialog, calendar;
           
           pad = function (value, length) {
              value = String(value);
              length = parseInt(length) || 2;
              while (value.length < length)
                  value = "0" + value;
                  return value;
           };
           
           calendar = new YAHOO.widget.Calendar("select-dates-caldiv", {
                    iframe:false,          // Turn iframe off, since container has iframe support.
                    hide_blank_weeks:true,  // Enable, to demonstrate how we handle changing height, using changeContent 
                    pagedate:"%(pagedate)s",                   
                    mindate:"%(mindate)s",                    
                    maxdate:"%(maxdate)s",
                    selected:"%(curdate)s",
                    navigator:true
                    });
           
            function handle_cancel() {
                this.hide();
            }

            function handle_ok() {
                if ( calendar.getSelectedDates().length > 0) {
                     var selDate = calendar.getSelectedDates()[0];
                     var datestring = selDate.getFullYear() + "-" + pad( selDate.getMonth()+1, 2) + "-" + pad( selDate.getDate(), 2);
                     document.getElementById("select-dates").value = datestring;
                     OKButton.set('disabled', true);
                     location.href='?date=' + datestring;
                };
                this.hide();
            }

            dialog = new YAHOO.widget.Dialog("select-dates-container", {
                  context:["select-dates-btn", "tl", "bl"],
                  buttons:[ {text:"Select", isDefault:false, handler: handle_ok },
                            {text:"Cancel", handler: handle_cancel}],
                  width:"16em",  // Sam Skin dialog needs to have a width defined (7*2em + 2*1em = 16em).
                  draggable:false,
                  close:true
                  });        
                       
            calendar.render();
            dialog.render();            
            OKButton = dialog.getButtons()[0];
            OKButton.set('disabled', true);
            // Using dialog.hide() instead of visible:false is a workaround for an IE6/7 container known issue with border-collapse:collapse.
            dialog.hide();
            
            calendar.renderEvent.subscribe(function() {
               dialog.fireEvent("changeContent");
               });
               
            calendar.selectEvent.subscribe(function () {
                OKButton.set('disabled', false);
            });
               
            YAHOO.util.Event.on("select-dates-btn", "click", dialog.show, dialog, true);
            });

        """
        # Set dates for calendar widget
        # min, max, current
        start_date, end_date = self._getDateConstraints()        
        if start_date:            
            mindate = datetime.date.strftime(start_date,'%m/%d/%Y')
        else:
            mindate=''
        if end_date:                        
            maxdate = datetime.date.strftime(end_date,'%m/%d/%Y')                        
        else:
            maxdate=''                    
        if self.Date:
            curdate = datetime.date.strftime(self.Date,'%m/%d/%Y')
            pagedate = datetime.date.strftime(self.Date,'%m/%Y')             
        else:
            if end_date:
                curdate = maxdate                
                pagedate = datetime.date.strftime(end_date,'%m/%Y') 
            else:
                curdate = datetime.date.strftime(datetime.date.today(),'%d/%m/%Y')  
                pagedate = datetime.date.strftime(datetime.date.today(),'%m/%Y')    
        minmaxdate= self.checkDateInConstraints()
        if minmaxdate:
            pagedate = datetime.date.strftime(minmaxdate,'%m/%Y')                                   
        dates = {"curdate" : curdate,
                "maxdate" : maxdate,
                "mindate" : mindate,
                "pagedate" : pagedate}
        return js_string % dates         
    


    
    def update(self):
        """
        refresh the query
        """       
        zc.resourcelibrary.need("yui-calendar")
        zc.resourcelibrary.need("yui-container")
        zc.resourcelibrary.need("yui-button")
        
        self.Date = getDisplayDate(self.request)
        if IGroupSitting.providedBy(self.context):
            # group sittings last only a part of a day, get rid of the error message
            Date = getattr( self.context, 'start_date', None)
            if type(Date) == datetime.datetime:
                self.Date= Date.date()
            elif type(Date) == datetime.date:
                self.Date= Date 
        if self.Date:
            self.DateStr=datetime.date.strftime(self.Date,'%Y-%m-%d')
        else:
            self.DateStr='all'
            self.request.response.setCookie('display_date','all')

        minmaxdate= self.checkDateInConstraints()
        if minmaxdate:                    
            self.error = 'error' 
            error_message = (u"""
                The date you requested (%(current)s) is not in the current restrictions. <br />
                Either select <a href="?date=%(minmax)s"> %(minmax)s </a> 
                or browse the data <a href="?date=all">for all dates</a>.
                """)  
            self.error_message = error_message % ({'current': self.DateStr , 'minmax': minmaxdate})     
        if (IGroupSittingAttendance.providedBy(self.context) 
            or IGroupSittingAttendanceContainer.providedBy(self.context)):
            # group sitting attendance does not have start - end
            self.error = None
        
    render = ViewPageTemplateFile ('templates/date_chooser_viewlet.pt')    
            
            
class AllParliamentsViewlet( viewlet.ViewletBase ):
    """
    display all parliaments
    """            
    for_display = True
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.query = None
        self.current_query = None
        self.Date=datetime.date.today()
        
    def update(self):
        """
        refresh the query
        """
        session = Session()
        self.query = session.query(domain.Parliament)
        self.Date = getDisplayDate(self.request) 
        #current
        if not self.Date:
            self.Date = datetime.date.today()
            self.request.response.setCookie('display_date', datetime.date.strftime(self.Date,'%Y-%m-%d') )
        self.current_query = session.query(domain.Parliament).filter(getFilter(self.Date))    

    def _getCurrentData( self ):
        """
        return the data filtered for the current date.
        """
        return self.current_query.all() 

    def getCurrentData( self ):
        """
        return current data in a dict for use in pt
        """
        #data_list=[]
        results =  self._getCurrentData()
        for result in results:            
            data ={}
            data['url']= '/parliament/obj-'  + str(result.parliament_id) 
            data['short_name'] = result.short_name
            data['election_date'] = result.election_date
            data['start_date'] = str(result.start_date)
            data['end_date'] = str(result.end_date)
            data['mpurl']= '/parliament/obj-' + str(result.parliament_id) + '/parliamentmembers' 
            #data_list.append(data)
        if results:    
            return data #_list             
        else:
            return {'url' : '/parliament/', 'short_name': 'N/A', 'start_date':'', 'end_date':'', 'election_date':''}    
                    
    def getData(self):
        """
        return the data of the query
        """        
        data_list=[]
        curlpf=getDateFilter(self.request)  
        current_results = self._getCurrentData()   
        results = self.query.all()
        results.reverse()
        for result in results:            
            data ={}
            if result.start_date and result.end_date:
                #diff = result.end_date - result.start_date
                #mid = result.start_date + diff/2
                urlpf = '?date=' + datetime.date.strftime(result.end_date,'%Y-%m-%d')
            else:
                urlpf ='?date=' + datetime.date.strftime(datetime.date.today(),'%Y-%m-%d')            
            #data['url']= '/parliament/' +urlpf
            data['url']= '/parliament/obj-'  + str(result.parliament_id) +urlpf            
            data['short_name'] = result.short_name
            data['election_date'] = result.election_date
            data['start_date'] = str(result.start_date)
            data['end_date'] = str(result.end_date)
            data['mpurl']= '/parliament/obj-' + str(result.parliament_id) + '/parliamentmembers' + urlpf
            if result in current_results:
                data['current'] = 'even'
                data['selector'] = '-->>'
                data['mpurl']= '/parliament/obj-' + str(result.parliament_id) + '/parliamentmembers' + curlpf
                #data['url']= '/parliament/' + curlpf
                data['purl']= '/parliament/obj-' + str(result.parliament_id)  + curlpf                
            else:
                data['current'] = 'odd' 
                data['selector'] = ''               
            data_list.append(data)
        return data_list
                    
    render = ViewPageTemplateFile ('templates/current_parliament_viewlet.pt')


class CurrentParliamentViewlet( viewlet.ViewletBase ):
    """
    display the current parliament.   
    """
    for_display = True    
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.query = None
        self.Date=datetime.date.today()
        
    def update(self):
        """
        refresh the query
        """
        session = Session()
        self.Date = getDisplayDate(self.request)
        if not self.Date:
            self.Date = datetime.date.today()
            self.request.response.setCookie('display_date', datetime.date.strftime(self.Date,'%Y-%m-%d') )
        self.query = session.query(domain.Parliament).filter(getFilter(self.Date))        
        
    
    def getData(self):
        """
        return the data of the query
        """
        data_list=[]
        urlpf=getDateFilter(self.request)        
        results = self.query.all()
        for result in results:            
            data ={}
            data['url']= '/parliament/obj-' + str(result.parliament_id) + urlpf
            data['short_name'] = result.short_name
            data['start_date'] = str(result.start_date)
            data['end_date'] = str(result.end_date)
            data['mpurl']= '/parliament/obj-' + str(result.parliament_id) + '/parliamentmembers' + urlpf
            data['current'] = 'odd'
            data_list.append(data)
        return data_list
                    
    render = ViewPageTemplateFile ('templates/current_parliament_viewlet.pt')
        
        
class CurrentGovernmentViewlet( viewlet.ViewletBase ):         
    """
    display the current Government
    """
    for_display = True    
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.query = None
        self.Date=datetime.date.today()                       
        
    def update(self):        
        session = Session()
        self.Date = getDisplayDate(self.request)
        if not self.Date:
            self.Date = datetime.date.today()
        self.query = session.query(domain.Government).filter(getFilter(self.Date))
        


    def getData(self):
        """
        return the data of the query
        """
        data_list=[]        
        urlpf=getDateFilter(self.request)
        results = self.query.all()
        for result in results:            
            data ={}
            data['url']= ('/parliament/obj-' + str(result.parliament_id) +
                          '/governments/obj-' + str(result.government_id) + urlpf)
            data['short_name'] = result.short_name
            data['start_date'] = str(result.start_date)
            data['end_date'] = str(result.end_date)
            data_list.append(data)            
        return data_list
        
        
    render = ViewPageTemplateFile ('templates/current_government_viewlet.pt')
    
class CurrentParliamentGovernmentViewlet( CurrentGovernmentViewlet ):     
    for_display = True
    render = ViewPageTemplateFile ('templates/current_parliament_government_viewlet.pt')    

class CurrentMinistriesViewlet( viewlet.ViewletBase ):
    for_display = True    
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.query = None
        self.Date=datetime.date.today()                       
        
    def update(self):        
        session = Session()
        self.Date = getDisplayDate(self.request)
        if not self.Date:
            self.Date = datetime.date.today()
        self.query = session.query(domain.Ministry).filter(getFilter(self.Date))
        
    def skiptag( self ):
        """
        skip the tag to be included in yui tabs
        """
        return self.__name__ != 'bungeni.current-gov.ministries'

    def getData(self):
        """
        return the data of the query
        """   
        session = Session()   
        urlpf=getDateFilter(self.request)                  
        data_list=[]        
        results = self.query.all()
        if results:
            m_id= results[0].ministry_id
            mpg_query = session.query(domain.MinistryInParliament).filter(domain.MinistryInParliament.c.ministry_id == m_id)
            mpg_result = mpg_query.first()
                    

        for result in results:            
            data ={}
            data['url']= ('/parliament/obj-' + str(mpg_result.parliament_id) +
                          '/governments/obj-' + str(mpg_result.government_id) + 
                          '/ministries/obj-' + str(result.ministry_id) + urlpf)
            data['minister_url']= ('/parliament/obj-' + str(mpg_result.parliament_id) +
                          '/governments/obj-' + str(mpg_result.government_id) + 
                          '/ministries/obj-' + str(result.ministry_id) + 
                          '/ministers' + urlpf)
            data['short_name'] = result.short_name
            data['full_name'] = result.full_name            
            data['start_date'] = str(result.start_date)
            data['end_date'] = str(result.end_date)
            data_list.append(data)
        return data_list
        
        
    render = ViewPageTemplateFile ('templates/current_ministries_viewlet.pt')    
    
class CurrentCommitteesViewlet( viewlet.ViewletBase ):
    for_display = True    
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.query = None
        self.Date=datetime.date.today()                       
        
    def update(self):        
        session = Session()
        self.Date = getDisplayDate(self.request)
        if not self.Date:
            self.Date = datetime.date.today()
        self.query = session.query(domain.Committee).filter(getFilter(self.Date))
        


    def getData(self):
        """
        return the data of the query
        """
        data_list=[]        
        urlpf=getDateFilter(self.request)
        results = self.query.all()
        for result in results:            
            data ={}
            data['url']= ('/parliament/obj-' + str(result.parliament_id) +
                          '/committees/obj-' + str(result.committee_id) + urlpf)
            data['short_name'] = result.short_name
            data['full_name'] = result.full_name            
            data['start_date'] = str(result.start_date)
            data['end_date'] = str(result.end_date)
            data_list.append(data)
        return data_list
        
        
    render = ViewPageTemplateFile ('templates/current_committees_viewlet.pt')    
    
class CurrentSitting( viewlet.ViewletBase ):
    """
    the current sittings are those closest to the given date.
    """        
    for_display = True
        
class CurrentPartymemberships( viewlet.ViewletBase ):
    """
    the partymembership of a MP does have multiple start/end dates so we have to
    explictly define which one is to be used
    """
    for_display = True
    def __init__( self,  context, request, view, manager ):        
        self.context = context.party
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.Date=datetime.date.today()  
        self.query = None                  

    def getFilter(self):
        return sql.or_(
            sql.between(self.Date, _ugm_party.c.start_date, _ugm_party.c.end_date),
            sql.and_( _ugm_party.c.start_date <= self.Date, _ugm_party.c.end_date == None)
            )
        
        
        
    def update(self):        
        session = Session()
        self.Date = getDisplayDate(self.request)  
        context = proxy.removeSecurityProxy( self.context )                   
        query = context._query   
        if self.Date:        
            # append between start and end date clause
            self.query = query.filter( self.getFilter() )
        else:
            self.query=query
            

    def getData(self):
        """
        return the data of the query
        """
        data_list=[]        
        urlpf=getDateFilter(self.request)
        results = self.query.all()
        for result in results:            
            data ={}
#            data['url']= ('/parliament/obj-' + str(result.parliament_id) +
#                          '/committees/obj-' + str(result.committee_id) + urlpf)
            data['short_name'] = result.short_name
#            data['full_name'] = result.full_name            
            data['start_date'] = str(result.start_date)
            data['end_date'] = str(result.end_date)
            data_list.append(data)
        return data_list

    
    render = ViewPageTemplateFile ('templates/current_partymembership_viewlet.pt')    
    
class CurrentRootMenuTree( BrowserView):
    Date = datetime.date.today()
    
    #def getCurrentParliament(self):
    def __call__( self ):
        rooturl = absoluteURL( self.context, self.request )
        self.Date = datetime.date.today()
        cp_filter = sql.or_(
            sql.between(self.Date, schema.groups.c.start_date, schema.groups.c.end_date),
            sql.and_( schema.groups.c.start_date <= self.Date, schema.groups.c.end_date == None)
            )
        session = Session()
        query = session.query(domain.Parliament).filter(cp_filter)
        try:
          current_parliament = query[0]
        except:
           current_parliament = None
        if  current_parliament:
            data = []
            url = rooturl + '/parliament/obj-' + str(current_parliament.parliament_id)
            node = []
            node.append({'url' : url + '/committees/', 'name': 'Committee', 'node': None} )
            node.append({'url' : url + '/sessions/', 'name': 'Parliamentary Session', 'node': None} )
            node.append({'url' : url + '/parliamentmembers/', 'name': 'Member of Parliament', 'node': None} )
            node.append({'url' : url + '/extensionmembers/', 'name': 'Group extensions', 'node': None} )
            node.append({'url' : url + '/governments/', 'name': 'Government', 'node': None} )
            node.append({'url' : url + '/politicalparties/', 'name': 'Political Party', 'node': None })  
            pdata = [{'url' : url, 'name': current_parliament.short_name, 'node': node }]
            data = [{'url' : rooturl + '/parliament/', 'name': 'Parliament', 'node': pdata }]
            return simplejson.dumps(data) 
        else:
            data = [{'url' : rooturl + '/parliament/', 'name': 'Parliament', node: None}]
            return simplejson.dumps(data)          
           
                       


