from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.BungeniDefaultContent.config import DEFAULT_SITE_CONTENT

def install(self):
    """ Do stuff that GS will do for us soon ..
    """
    out = StringIO()

    plone = getToolByName(self, 'portal_url').getPortalObject()

    # Filter the global tabs
    plone.Members # hide ...

    #
    # Create default content
    #
    def add_object(parent, d):
        id = d.get('id', None)
        if id is None:
            id = self.generateUniqueId(d['type'])
        parent.invokeFactory(d['type'], id,)
        obj = parent[id]
        layout = d.get('layout', None)
        if layout:
            obj.setLayout(layout)
        obj.processForm(data=1, values=d)

    def add_structure(root, structure):
        """ Recursively add content as specified in tuples of dicts.
        """
        for d in structure:
            add_object(root, d)
            if d.get('children', None):
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
