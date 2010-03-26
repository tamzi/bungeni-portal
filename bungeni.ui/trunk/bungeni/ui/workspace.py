# Bungeni Parliamentary Information System - http://www.bungeni.org/
# Copyright (C) 2010 Africa i-Parliaments Action Plan - http://www.parliaments.info/
# Licensed under GNU GPL v2 - http://www.gnu.org/licenses/gpl-2.0.txt

"""Workspace Views

$Id$
"""

from zope import interface
from zope.publisher.browser import BrowserView
from ploned.ui.interfaces import IViewView

from ore.alchemist import Session

from bungeni.models.utils import get_db_user_id
from bungeni.models.utils import get_roles
from bungeni.models.utils import get_group_ids_for_user_in_parliament 
from bungeni.models.utils import get_ministry_ids_for_user_in_government
from bungeni.models.utils import get_current_parliament
from bungeni.models.utils import get_current_parliament_governments

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

#

role_interface_mapping = {
    u'bungeni.Admin': interfaces.IAdministratorWorkspace,
    u'bungeni.Minister': interfaces.IMinisterWorkspace,
    u'bungeni.MP': interfaces.IMPWorkspace,
    u'bungeni.Speaker': interfaces.ISpeakerWorkspace,
    u'bungeni.Clerk': interfaces.IClerkWorkspace
}

class WorkspaceView(BungeniBrowserView):

    page_title = u"Bungeni Workspace"
    provider_name = "bungeni.workspace"
    
    user_id = None
    user_group_ids = None
    government_id = None
    ministry_ids = None
    
    def __init__(self, context, request):
        super(WorkspaceView, self).__init__(context, request)
        parliament = get_current_parliament(context)
        if parliament:
            self.context = parliament
            self.context.__parent__ = context
            self.context.__name__ = ""
            self.user_id = get_db_user_id()
            self.user_group_ids = get_group_ids_for_user_in_parliament(
                    self.user_id, parliament.parliament_id)
            try:
                self.government_id = \
                    get_current_parliament_governments(parliament)[0].group_id
                self.ministry_ids = get_ministry_ids_for_user_in_government(
                    self.user_id, self.government_id)
            except (Exception,):
                # !+ log.debug(e)
                import sys; print "WorkspaceView: %s" % sys.exc_info()[1]
                pass
            if self.ministry_ids:
                    interface.alsoProvides(self, interfaces.IMinisterWorkspace)
        
        roles = get_roles(self.context)
        for role_id in roles:
            iface = role_interface_mapping.get(role_id)
            if iface is not None:
                interface.alsoProvides(self, iface)
    
    def __call__(self):
        session = Session()
        call = super(WorkspaceView, self).__call__()
        session.close()
        return call


class WorkspaceArchiveView(WorkspaceView):
    
    provider_name = "bungeni.workspace-archive"
    page_title = u"Bungeni Workspace Archive"
    
