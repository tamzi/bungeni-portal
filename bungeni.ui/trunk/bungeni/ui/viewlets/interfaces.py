from zope.viewlet.interfaces import IViewletManager


class IWorkspace(IViewletManager):
    """Workspace viewlet manager."""
    
class ICurrent( IViewletManager ):    
    """ Current Objects viewlet manager """
