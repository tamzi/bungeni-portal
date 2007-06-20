from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr
from Products.membrane.interfaces import ICategoryMapper
from Products.membrane.config import ACTIVE_STATUS_CATEGORY
from Products.membrane.utils import getAllWFStatesForType
from Products.membrane.utils import generateCategorySetIdForType
from Products.remember.utils import getAdderUtility
from Products.Bungeni.config import ACTIVE_MEMBRANE_STATES 

def install(self):
    """ Do stuff that GS will do for us soon ..
    """
    out = StringIO()

    # XXX: this doesn't actually work, as it steps on work done in
    # Install.py
    #
    # Note that we can apply profiles after adding a Plone site using
    # instancemanager: does it make more sense to leave it to
    # instancemanager?
    #
    # # Apply membrane and remember profiles (we can't QI them)
    # membrane_tool = getToolByName(self, 'membrane_tool')
    # if not membrane_tool:
    #     setup_tool = getToolByName(self, 'portal_setup')
    #     for p in ('membrane', 'remember', ):
    #         setup_tool.setImportContext('profile-%s:default' % p)
    #         out.write( 'Switched to profile: %s \n' % p)
    #         result = setup_tool.runAllImportSteps()
    #         print >>out,  'Steps run: %s \n' % ', '.join(result['steps'])

    # Change default member to MemberOfPublic
    plone = getToolByName(self, 'portal_url').getPortalObject()
    adder = getAdderUtility(plone)
    adder.default_member_type = 'MemberOfPublic'

    # Require approval for the adding of plain old members
    workflow_tool = getToolByName(self, 'portal_workflow')
    workflow_tool.setChainForPortalTypes( ['Member'], "MemberApprovalWorkflow")

    # Repair status_map for our new types.
    # TODO: setting their workflow *after* registering the types in
    # TODO: Install.py messes with the default active state(s) of the
    # TODO: members. Fix AGX to generate them after workflow
    # TODO: registration.
    membrane_tool = getToolByName(self, 'membrane_tool')
    cat_map = ICategoryMapper(membrane_tool)
    for portal_type in ['MemberOfParliament', 'Clerk', 'MemberOfPublic']:
        cat_set = generateCategorySetIdForType(portal_type)
        # states = getAllWFStatesForType(self, portal_type)
        states = ACTIVE_MEMBRANE_STATES[portal_type]
        cat_map.replaceCategoryValues(cat_set, ACTIVE_STATUS_CATEGORY, states)

    # Change the default workflow
    workflow_tool = getToolByName(self, 'portal_workflow')
    workflow_tool.setDefaultChain('BungeniWorkflow')
    workflow_tool.setChainForPortalTypes( ['Folder', 'Large Plone Folder'], "BungeniWorkflow")
    workflow_tool.updateRoleMappings()

    # Enable syndication
    # XXX: Figure out a better way to identify the content that needs syndication
    syndication_tool = getToolByName(self, 'portal_syndication')
    if not syndication_tool.isSiteSyndicationAllowed():
        syndication_tool.editProperties(isAllowed=1)
    if not syndication_tool.isSyndicationAllowed(self.events):
        syndication_tool.enableSyndication(self.events)

    # # Change the default roles managed by teams
    # teams_tool = getToolByName(self, 'portal_teams')
    # allowed_roles = teams_tool.getDefaultAllowedRoles()
    # teams_tool.setDefaultAllowedRoles(
    #         allowed_roles+['ReviewerForSpeaker', 'CurrentMP'])

    # Replace the default MailHost with a MaildropHost
    if (shasattr(plone, 'MailHost') and 
            plone.MailHost.meta_type != 'Secure Maildrop Host'):
        plone.manage_delObjects('MailHost')
    if not shasattr(plone, 'MailHost'):
        plone.manage_addProduct['SecureMaildropHost'].manage_addSecureMaildropHost('MailHost')

    return out.getvalue()

