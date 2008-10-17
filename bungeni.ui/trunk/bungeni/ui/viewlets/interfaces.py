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
    
class ICurrentGovernment( IViewletManager ):    
    """ Current Government """

class ITabManager( IViewletManager ):
    """ Create YUI Tabs """        
