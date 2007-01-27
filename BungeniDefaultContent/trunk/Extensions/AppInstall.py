from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.BungeniDefaultContent.config import DEFAULT_SITE_CONTENT

def install(self):
    """ Do stuff that GS will do for us soon ..
    """
    out = StringIO()

    plone = getToolByName(self, 'portal_url').getPortalObject()

    # Filter the global tabs
    plone.Members

    # Create default content
    def add_structure(root, structure):
        """ Recursively add content as specified in tuples of dicts.
        """
        for d in structure:
            root.invokeFactory(d['type'], d['id'])
            obj = root[d['id']]
            obj.edit(**d)
            # recatalog?
            if d['children']:
                add_structure(obj, d['children'])
    add_structure(plone, DEFAULT_SITE_CONTENT)

    paths = ['/'.join(plone[d['id']].getPhysicalPath()) for d in DEFAULT_SITE_CONTENT]
    plone.folder_publish(workflow_action='publish', paths=paths,
            comment="Published by installer.", include_children=True)
    print >>out, 'Created default folders'

    return out.getvalue()

def uninstall(self):
    out = StringIO()

    plone = getToolByName(self, 'portal_url').getPortalObject()
    ids = [d['id'] for d in DEFAULT_SITE_CONTENT]
    plone.manage_delObjects(ids) 
    print >>out, 'Deleted our folders'

    return out.getvalue()
