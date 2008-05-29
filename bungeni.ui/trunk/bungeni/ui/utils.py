# encoding: utf-8

import datetime
import pdb
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
                print DisplayDate
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
