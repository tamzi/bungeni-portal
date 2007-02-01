from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.remember.utils import getAdderUtility

def install(self):
    """ Do stuff that GS will do for us soon ..
    """
    out = StringIO()

    # XXX: this doesn't actually work, as it steps on work done in
    # Install.py
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
    wft = getToolByName(self, 'portal_workflow')
    wft.setChainForPortalTypes( ['Member'], "MemberApprovalWorkflow")

    # Change the default workflow
    wft = getToolByName(self, 'portal_workflow')
    wft.setDefaultChain('BungeniWorkflow')
    wft.setChainForPortalTypes( ['Folder', 'Large Plone Folder'], "BungeniWorkflow")
    wft.updateRoleMappings()

    return out.getvalue()

