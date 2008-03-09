from zope import     schema
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.viewlet.interfaces import IViewletManager
from z3c.menu.ready2go import interfaces as imenu

class IPlonedSkin( IDefaultBrowserLayer ):
    """ plone skin for zope3  """

class ICSSManager( IViewletManager ):
    """ viewlet manager for css """

class IJavaScriptManager( IViewletManager ):
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

class IPersonalBarMenu( imenu.IMenuManager ):
    """ personalized site actions, login, logout, dashboard"""
    
class IPersonalTasksMenu( imenu.IMenuManager ):
    """ personalized site actions, login, logout, dashboard"""

class IPersonalActionItem( imenu.ISiteMenuItem ):
    """ we register various role required """
    groups = schema.List( value_type=schema.Int() )
    roles = schema.List( value_type=schema.Int() )

class IContentViews( IViewletManager ):
    """ """

class IDocumentActions( IViewletManager ):
    """ """
