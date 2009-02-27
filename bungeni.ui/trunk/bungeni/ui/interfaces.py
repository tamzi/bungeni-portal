from zope.viewlet.interfaces import IViewletManager
from zope.publisher.interfaces.browser import IBrowserView

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


