
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.viewlet.interfaces import IViewletManager

class IBungeniSkin( IDefaultBrowserLayer ):
    """ skin for bungeni """

class ICSSManager( IViewletManager ):
    """ viewlet manager for css """

class IJavaScriptManger( IViewletManager ):
    """ viewlet manager for js """


class ILeftColumnManager( IViewletManager ):
    """ """

class IRightColumnManager( IViewletManager ):
    """ """

class IAboveContentManager( IViewletManager ):
    """ """

class IBelowContentManager( IViewletManager ):
    """ """

class IContentViewsManager( IViewletManager ):
    """ """

class IPortalHeaderManager( IViewletManager ):
    """ """
    
class IPortalFooterManager( IViewletManager ):
    """ """

class IContentViews( IViewletManager ):
    """ """

class IDocumentActions( IViewletManager ):
    """ """
