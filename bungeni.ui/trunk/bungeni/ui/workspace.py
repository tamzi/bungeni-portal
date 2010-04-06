# Bungeni Parliamentary Information System - http://www.bungeni.org/
# Copyright (C) 2010 Africa i-Parliaments Action Plan - http://www.parliaments.info/
# Licensed under GNU GPL v2 - http://www.gnu.org/licenses/gpl-2.0.txt

"""Workspace Views

$Id$
"""
log = __import__("logging").getLogger("bungeni.ui.workspace")

import sys
from zope import interface
from zope.publisher.browser import BrowserView
from ploned.ui.interfaces import IViewView

from ore.alchemist import Session

from bungeni.models.utils import get_db_user_id
from bungeni.models.utils import get_roles
from bungeni.models.utils import get_group_ids_for_user_in_parliament 
from bungeni.models.utils import get_ministries_for_user_in_government
from bungeni.models.utils import get_current_parliament
from bungeni.models.utils import get_current_parliament_governments
from bungeni.ui.utils import url as ui_url, misc

from bungeni.models import interfaces as model_interfaces
from bungeni.ui import interfaces


class BungeniBrowserView(BrowserView): 
    interface.implements(IViewView)
    
    page_title = u" :BungeniBrowserView.page_title: "
    provider_name = None # str, to be set by subclass, to specify the 
    # ViewletManager.name for the viewlet manager that is providing the 
    # viewlets for this view
    
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



# make dynamic lookup of child workspaces

def prepare_user_workspaces(event):
    """Determine the current principal's workspaces, depending on roles and
    group memberships. 
    
    "bungeni.Clerk", "bungeni.Speaker", "bungeni.MP"
        these roles get a parliament-level workspace
    
    "bungeni.Minister"
        "implied" role (by being a member of a ministry group) 
        gets a ministry-level workspace (for each ministry)
    
    "zope.Manager", "bungeni.Admin", "bungeni.Owner", "bungeni.Everybody", 
    "bungeni.Anybody"
        not relevant for user workspaces, no workspaces
        !+ should these get an owner-level (user) workspace?
    
    """
    def is_traversing_workspace_root(obj, req):
        return (
            # obj should be the BungeniApplication
            model_interfaces.IBungeniApplication.providedBy(obj)
            and
            # the request should be for a view within /workspace
            # note: IWorkspaceSectionLayer is applied to the request by 
            # publication.apply_request_layers_by_url() that therefore must 
            # have already been called
            interfaces.IWorkspaceSectionLayer.providedBy(req)
        )
    if not is_traversing_workspace_root(event.object, event.request):
        return
    
    app = event.object # bungeni.core.app.BungeniApp
    request = event.request
    path = "/".join(reversed(request.getTraversalStack()))
    log.debug ("prepare_user_workspaces: app:%s path:%s" % (app, path))
    log.debug ("    app.items:%s" % (app.items()))
    
    # initialize a layer data object, for the views in the layer
    LD = request._layer_data = misc.bunch(
        workspaces=[], # (unique) workspace containers
        
        # these are needed by the views, as we need them also here, we just
        # remember them to not need to calculate them again
        user_id=None,
        user_group_ids=None,
        government_id=None,
        ministry_ids=None        
    )
    #LD['app'] = app
    
    parliament = get_current_parliament(None)
    roles = get_roles(parliament)
    log.debug("roles: %s" % roles)
    
    # "bungeni.Clerk", "bungeni.Speaker", "bungeni.MP"
    for role_id in roles:
        if role_id in ("bungeni.Clerk", "bungeni.Speaker", "bungeni.MP"):
            log.debug("adding parliament workspace %s (for role %s)" % (
                                                        parliament, role_id))
            LD.workspaces.append(parliament)
    
    # "bungeni.Minister"
    # need to check for ministry groups to which the principal belongs, and 
    # for each such ministry assign a ministry workspace
    LD.user_id = get_db_user_id()
    LD.user_group_ids = get_group_ids_for_user_in_parliament(
                                        LD.user_id, parliament.group_id)
    try:
        LD.government_id = get_current_parliament_governments(
                                                parliament)[0].group_id
        ministries = get_ministries_for_user_in_government(
                                            LD.user_id, LD.government_id)
        log.debug("parliament:(%s, %s) / government_id:%s / ministries:%s" % (
             parliament.full_name, parliament.group_id, 
             LD.government_id, 
             [(m.full_name, m.group_id) for m in ministries] ))
        for ministry in ministries:
            log.debug("adding ministry workspace %s" % ministry)
            LD.workspaces.append(ministry)
    except (Exception,):
        name, exc = sys.exc_info()[0].__name__,  sys.exc_info()[1]
        log.debug("prepare_user_workspaces: %s: %s" % (name, exc))

    # ensure unique workspaces, preserving the order
    LD.workspaces = [ workspace for workspace in LD.workspaces
                      if workspace in set(LD.workspaces) ]

#

class WorkspaceView(BungeniBrowserView):
    #interface.implements(interfaces.IWorkspace)
    
    # set on request._layer_data
    user_id = None
    user_group_ids = None
    government_id = None
    ministry_ids = None
    
    role_interface_mapping = {
        u'bungeni.Admin': interfaces.IAdministratorWorkspace,
        u'bungeni.Minister': interfaces.IMinisterWorkspace,
        u'bungeni.MP': interfaces.IMPWorkspace,
        u'bungeni.Speaker': interfaces.ISpeakerWorkspace,
        u'bungeni.Clerk': interfaces.IClerkWorkspace
    }

    def __init__(self, context, request):
        """self:zope.app.pagetemplate.simpleviewclass.SimpleViewClass -> 
                    templates/workspace-index.pt
           context:bungeni.core.content.Section
        """
        assert interfaces.IWorkspaceSectionLayer.providedBy(request)
        LD = request._layer_data
        assert LD.get("workspaces") is not None
        
        super(WorkspaceView, self).__init__(context, request)
        
        # context may change per user workspace, so we always recalculate
        self.push_context(get_current_parliament(context))
        
        # transfer layer data items, for the view
        self.user_id = LD.user_id
        self.user_group_ids = LD.user_group_ids
        self.government_id = LD.government_id # may be None
        self.ministry_ids = LD.ministry_ids # may be None
        if self.ministry_ids:
            interface.alsoProvides(self, interfaces.IMinisterWorkspace)
        
        # roles are function of the context, so always recalculate
        roles = get_roles(self.context)
        for role_id in roles:
            iface = self.role_interface_mapping.get(role_id)
            if iface is not None:
                interface.alsoProvides(self, iface)
    
    def push_context(self, ctx):
        if ctx:
            last_ctx = self.context
            self.context = ctx
            self.context.__parent__ = last_ctx
            self.context.__name__ = ""
            
    
    def __call__(self):
        session = Session()
        call = super(WorkspaceView, self).__call__()
        return call

#

class WorkspacePIView(WorkspaceView):
    page_title = u"Bungeni Workspace"
    provider_name = "bungeni.workspace"
    
class WorkspaceArchiveView(WorkspaceView):
    provider_name = "bungeni.workspace-archive"
    page_title = u"Bungeni Workspace Archive"
    
#

