from zope import interface
from zope import component
from zope.publisher.browser import BrowserView
from zope.securitypolicy.interfaces import IRole, IPrincipalRoleMap
from zope.securitypolicy.settings import Allow, Deny
from zope.security.proxy import ProxyFactory
from ploned.ui.interfaces import IViewView

from ore.alchemist import Session
import sqlalchemy.sql.expression as sql

from bungeni.models import domain
from bungeni.models.utils import get_db_user_id
from bungeni.models.utils import get_roles
from bungeni.models.utils import get_group_ids_for_user_in_parliament 
from bungeni.models.utils import get_ministry_ids_for_user_in_government
from bungeni.core.globalsettings import getCurrentParliamentId

from workspace import role_interface_mapping, WorkspaceView

import interfaces


class WorkspaceArchiveView(WorkspaceView):
    interface.implements(IViewView)
    ministry_ids = []
    provider_name = "bungeni.workspace-archive"
    page_title = u"Bungeni Workspace Archive"
    
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

                
                
                
                
