from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.remember.utils import getAdderUtility, getRememberTypes

def install(self):
    """ Do stuff that GS will do for us soon ..
    """
    out = StringIO()

    # Apply membrane and remember profiles (we can't QI them)
    setup_tool = getToolByName(self, 'portal_setup')
    for p in ('membrane', 'remember', ):
        setup_tool.setImportContext('profile-%s:default' % p)
        out.write( 'Switched to profile: %s \n' % p)
        result = setup_tool.runAllImportSteps()
        print >>out,  'Steps run: %s \n' % ', '.join(result['steps'])

    # Change default member to MemberOfPublic
    plone = getToolByName(self, 'portal_url').getPortalObject()
    adder = getAdderUtility(plone)
    adder.default_member_type = 'MemberOfPublic'

    # Require approval for the adding of plain old members
    wft = getToolByName(self, 'portal_workflow')
    wft.setChainForPortalTypes( ['Member'], "member_approval_workflow")

    # Allow member data container to store the new member types
    types_tool = getToolByName(self, 'portal_types')
    memberdata_tool = getToolByName(self, 'portal_memberdata')
    fti = types_tool.getTypeInfo(memberdata_tool)
    fti.manage_changeProperties(allowed_content_types=getRememberTypes(self))

    return out.getvalue()
