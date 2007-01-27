from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.remember.utils import getAdderUtility

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

    # Change default Member type. Bungeni prefers MPs & clerks.
    wft = getToolByName(self, 'portal_workflow')
    wft.setChainForPortalTypes( ['Member'], "member_approval_workflow")
    plone = getToolByName(self, 'portal_url').getPortalObject()
    adder = getAdderUtility(plone)
    adder.default_member_type = 'MemberOfPublic'

    return out.getvalue()
