from Products.CMFCore.utils import getToolByName

def install(self):
    """ Do stuff that GS will do for us soon ..
    """
    out = StringIO()

    setup_tool = getToolByName(self, 'portal_setup')

    for p in ('membrane', 'remember', ):
        setup_tool.setImportContext('profile-%s:default' % p)
        out.write( 'Switched to profile: %s \n' % p)
        result = setup_tool.runAllImportSteps()
        out.write( 'Steps run: %s \n' % ', '.join(result['steps']) )

    return out.getvalue()
