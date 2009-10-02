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
from bungeni.models.utils import get_db_user_id, get_group_ids_for_user_in_parliament
from bungeni.core.globalsettings import getCurrentParliamentId

import interfaces


def add_roles(principal, prms, roles):
    for prm in prms:
        l_roles = prm.getRolesForPrincipal(principal)
        for role in l_roles:
            if role[1] == Allow:
                if not(role[0] in roles):
                    roles.append(role[0])
            elif role[1] == Deny:
                if role[0] in roles:
                    roles.remove(role[0])
    return roles                


def getRoles(context, request):
    #return [role_id for role_id, role in \
    #        component.getUtilitiesFor(IRole, context)]
    # eeks we have to loop through all groups of the
    # principal and al PrincipalRoleMaps to get all roles 
    ctx = context
    prms = []
    while ctx:    
        prms.append(IPrincipalRoleMap(ctx))
        ctx = getattr(ctx,'__parent__', None)                                
    pg = request.principal.groups.keys()
    roles = []
    for pn in pg:
        roles = add_roles(pn,prms,roles)         
    pn = request.principal.id
    roles = add_roles(pn,prms,roles)  
    return roles

role_interface_mapping = {
    u'bungeni.Admin': interfaces.IAdministratorWorkspace,
    u'bungeni.Minister': interfaces.IMinisterWorkspace,
    u'bungeni.MP': interfaces.IMPWorkspace,
    u'bungeni.Speaker': interfaces.ISpeakerWorkspace,
    u'bungeni.Clerk': interfaces.IClerkWorkspace
    }

class WorkspaceView(BrowserView):
    interface.implements(IViewView)
    
    def __init__(self, context, request):
        super(WorkspaceView, self).__init__(context, request)
        parliament_id = getCurrentParliamentId()
        if parliament_id:
            session = Session()
            parliament = session.query(domain.Parliament).get(parliament_id)
            self.context = parliament
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
            else:
                self.government_id = None
                                               
        roles = getRoles(self.context, self.request)

        for role_id in roles:
            iface = role_interface_mapping.get(role_id)
            if iface is not None:
                interface.alsoProvides(self, iface)

                
                
                
                
