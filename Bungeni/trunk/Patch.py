from DateTime import DateTime
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.PlonePAS.tools.membership import MembershipTool as PAS_MembershipTool 
from Products.CMFCore.MembershipTool import MembershipTool as CMFCore_MembershipTool 
from Products.PloneHelpCenter.Patch import monkeyPatch
from config import *
import zLOG

PATCH_PREFIX = '_monkey_'

__refresh_module__ = 0

class Patched_CMFCore_MembershipTool:
    #
    #   Squash getMemberareaCreationFlag: we ask BungeniMembership
    #

    security = ClassSecurityInfo()

    security.declareProtected(permissions.ManagePortal, 'getMemberareaCreationFlag')
    def getMemberareaCreationFlag(self):
        return True


class Patched_PAS_MembershipTool:
    #
    #   Introduce per-member-type member area creation.
    #

    security = ClassSecurityInfo()

    security.declarePublic('createMemberarea')
    def createMemberarea(self, member_id=None, minimal=True):
        """ Introduce per-member-type member area creation, and delegate
        to original.

        Ask portal_bungenimembership if our member type gets a home
        folder. If not, return immediately. Otherwise, let things take
        their course.
        """
        # Grovel for the member .. 
        membership = getToolByName(self, 'portal_membership')
        member = None

        if member_id:
            member = membership.getMemberById(member_id)
        else:
            member = membership.getAuthenticatedMember()

        if member:
            bmt = getToolByName(self, 'portal_bungenimembership')
            tt = getToolByName(self, 'portal_types')
            member_types_with_home_folders = bmt.getCreateMemberareaFor()
            fti = tt.getTypeInfo(member)
            if not fti.title in member_types_with_home_folders :
                return None

        self._monkey_createMemberarea(member_id, minimal)

zLOG.LOG('Bungeni', zLOG.INFO, 'Monkey patching PlonePAS.tools.membership.MembershipTool')
monkeyPatch(CMFCore_MembershipTool, Patched_CMFCore_MembershipTool)
zLOG.LOG('Bungeni', zLOG.INFO, 'Monkey patching CMFCore.MembershipTool')
monkeyPatch(PAS_MembershipTool, Patched_PAS_MembershipTool)
