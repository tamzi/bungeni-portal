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

class IBusinessWhatsOnSectionLayer(IDefaultBrowserLayer):
    """Requests for an object within the whats on page of the business section."""

class IMembersSectionLayer(IDefaultBrowserLayer):
    """Requests for an object within the members section."""

class IAdminSectionLayer(IDefaultBrowserLayer):
    """Requests for an object within the admin section."""

class IWorkspaceSectionLayer(IDefaultBrowserLayer):
    """Requests for an object within the workspace section."""

class IAddParliamentaryContentLayer(IDefaultBrowserLayer):
    """Add Paliamentary Content menu... only: 
        workspace/ and workspace/calandar 
    """

