from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from ploned.ui.interfaces import IPlonedSkin
from ore.yui.interfaces import IYUILayer

class IBungeniSkin(IPlonedSkin, IYUILayer):
    """Bungeni application skin."""

class IBungeniAuthenticatedSkin(IBungeniSkin):
    """Skin for authenticated users."""

class ISpeakerWorkspace(IBrowserView):
    """Speaker's workspace."""

class IClerkWorkspace(IBrowserView):
    """Clerk's workspace."""

class IAdministratorWorkspace(IBrowserView):
    """Administrator's workspace."""

class IMinisterWorkspace(IBrowserView):
    """Minister's workspace."""

class IMPWorkspace(IBrowserView):
    """MP's workspace."""

class IArchiveSectionLayer(IDefaultBrowserLayer):
    """Requests for an object within the archive."""

class IBusinessSectionLayer(IDefaultBrowserLayer):
    """Requests for an object within the business section."""

