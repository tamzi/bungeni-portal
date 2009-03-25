# encoding: utf-8

import datetime
from bungeni.ui.i18n import _

def is_ajax_request(request):
    return request.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def urljoin(base, action):
    if action is None:
        return
    if action.startswith('http://') or action.startswith('https://'):
        return action
    if action.startswith('/'):
        raise NotImplementedError(action)

    return "/".join((base, action.lstrip('./')))

def makeList( itemIds ):

    if type(itemIds) == ListType:
        return itemIds            
    elif type(itemIds) in StringTypes:
        # only one item in this list
        return [itemIds,]
    else:
         raise TypeError( _("Form values must be of type string or list"))

def get_date( date):
    if type(date) == datetime.datetime:
        return date.date()
    elif type(date) == datetime.date:
        return date
    else:
        raise TypeError (_("date must be of type datetime or date"))                


def getDisplayDate(request):   
    """
    get the date for which to display the data.
    #SQL WHERE:
    # displayDate BETWEEN start_date and end_date
    # OR
    # displayDate > start_date and end_date IS NULL   
    """ 
    filter_by = ''
    DisplayDate = request.get('date', None)
    if not DisplayDate:
        if request.has_key('display_date'):
            DisplayDate = request['display_date']
    else:
        if request.has_key('display_date'):
            if DisplayDate != request['display_date']:         
                request.response.setCookie('display_date', DisplayDate, path='/')               
        else:
            request.response.setCookie('display_date', DisplayDate, path='/' )          
    displayDate = None
    if DisplayDate:
        try:
            y, m, d = (int(x) for x in DisplayDate.split('-'))
            displayDate = datetime.date(y,m,d)
        except:
            #displayDate = datetime.date.today()              
            displayDate = None
    else:
        #displayDate = datetime.date.today() 
        displayDate=None
    return displayDate

def getFilter(displayDate):                   
    if displayDate:
        filter_by = """
        ( ('%(displayDate)s' BETWEEN start_date AND end_date )
        OR
        ( '%(displayDate)s' > start_date AND end_date IS NULL) )
        """ % ({ 'displayDate' : displayDate})        
    else:
        filter_by = ""            
    return filter_by    
