from zope.viewlet.interfaces import IViewletManager


class IWorkspace(IViewletManager):
    """Workspace viewlet manager."""
    
class ICurrent( IViewletManager ):    
    """ Current Objects viewlet manager """
    
class ICurrentMinistries( IViewletManager ):  
    """ Ministries in current government """      
    
class IDateChooser( IViewletManager ):    
    """ Date Chooser viewlet manager """    

class ISittingCalendar( IViewletManager ):    
    """ Sitting Calendar viewlet manager """     

class IScheduleCalendar( IViewletManager ):    
    """ Schedule Calendar viewlet manager """    

class IScheduleHolydayCalendar( IViewletManager ):    
    """ Schedule Hollydays viewlet manager """       

class IScheduleSittingCalendar( IViewletManager ):    
    """ Schedule sittings for all sessions and committees viewlet manager """       
    
class IScheduleGroupCalendar( IViewletManager ):
    """
    schedule items for group sittings
    """    
    
class IScheduleItems( IViewletManager ):    
    """ Schedule Calendar items viewlet manager """    

class IWeekSittingCalendar( IViewletManager ):    
    """ Week Calendar show all items viewlet manager """        
    
class IPlenaryCalendar( IViewletManager ):    
    """ monthly Calendar show all plenary sittings viewlet manager """     


    
class ICurrentGovernment( IViewletManager ):    
    """ Current Government """

class ITabManager( IViewletManager ):
    """ Create YUI Tabs """        
