from zope import interface
from zope.publisher.browser import BrowserView
from zope.security.proxy import ProxyFactory
from ploned.ui.interfaces import IViewView

from ore.alchemist import Session
import sqlalchemy.sql.expression as sql

from bungeni.models import domain
from bungeni.models.utils import get_principal
from bungeni.models.utils import get_db_user_id
from bungeni.models.utils import get_roles
from bungeni.models.utils import get_group_ids_for_user_in_parliament 
from bungeni.models.utils import get_ministry_ids_for_user_in_government
from bungeni.core.globalsettings import getCurrentParliamentId

import interfaces

role_interface_mapping = {
    u'bungeni.Admin': interfaces.IAdministratorWorkspace,
    u'bungeni.Minister': interfaces.IMinisterWorkspace,
    u'bungeni.MP': interfaces.IMPWorkspace,
    u'bungeni.Speaker': interfaces.ISpeakerWorkspace,
    u'bungeni.Clerk': interfaces.IClerkWorkspace
}

class WorkspaceView(BrowserView):
    interface.implements(IViewView)
    ministry_ids = []
    page_title = u"Bungeni Workspace"
    
    def __init__(self, context, request):
        super(WorkspaceView, self).__init__(context, request)
        parliament_id = getCurrentParliamentId()
        if parliament_id:
            session = Session()
            parliament = session.query(domain.Parliament).get(parliament_id)
            self.context = parliament
            self.ministry_ids = []
            self.context.__parent__ = context
            self.context.__name__ = ""
            self.request = request
            self.user_id = get_db_user_id()
            self.user_group_ids = get_group_ids_for_user_in_parliament(
                    self.user_id, parliament_id)
            governments = session.query(domain.Government).filter(
                sql.and_(
                    domain.Government.parent_group_id == parliament.group_id,
                    domain.Government.status == 'active')
                    ).all()
            if len(governments) == 1:
                self.government_id =  governments[0].group_id
                self.ministry_ids = get_ministry_ids_for_user_in_government(
                    self.user_id, self.government_id)
                if self.ministry_ids:
                    interface.alsoProvides(self, interfaces.IMinisterWorkspace)
            else:
                self.government_id = None
        
        roles = get_roles(self.context)
        
        for role_id in roles:
            iface = role_interface_mapping.get(role_id)
            if iface is not None:
                interface.alsoProvides(self, iface)
    
    
    provider_name = "bungeni.workspace"
    
    def provide(self):
        """ () -> str
        
        To give view templates the ability to call on a view-defined provider, 
        without having to hard-wire the provider name in the template itself
        i.e. this is to be able to replace template calls such as:
            <div tal:replace="structure provider:HARD_WIRED_PROVIDER_NAME" />
        with:
            <div tal:replace="structure python:view.provide() />
        The provider_name attribute is factored out so that it is trivial 
        for view subclasses to specify a provider name.
        """
        from zope.component import getMultiAdapter
        from zope.viewlet.interfaces import IViewletManager
        provider = getMultiAdapter(
                            (self.context, self.request, self),
                            IViewletManager,
                            name=self.provider_name)
        provider.update()
        return provider.render()
    
    
    def __call__(self):
        session = Session()
        call = super(WorkspaceView, self).__call__()
        session.close()
        return call

