from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.BungeniDefaultContent.config import DEFAULT_SITE_CONTENT

def add_default_content(self):
    #
    # Create default content
    #
    def add_object(parent, d):
        id = d.get('id', None)
        if id is None:
            id = self.generateUniqueId(d['type'])
        if d['type'].endswith('Criterion'):
            obj = parent.addCriterion(d['field'], d['type'])
        else:
            parent.invokeFactory(d['type'], id,)
            obj = parent[id]
            layout = d.get('layout', None)
            if layout:
                obj.setLayout(layout)
        obj.processForm(data=1, values=d)
        return obj

    def add_structure(root, structure):
        """ Recursively add content as specified in tuples of dicts.
        """
        for d in structure:
            obj = add_object(root, d)
            if d.get('children', None):
                add_structure(obj, d['children'])
    add_structure(plone, DEFAULT_SITE_CONTENT)

    normalizeString = getToolByName(self, 'plone_utils').normalizeString
    ids = [d.get('id', normalizeString(d['title'])) for d in DEFAULT_SITE_CONTENT]
    paths = ['/'.join(plone[i].getPhysicalPath()) for i in ids]
    plone.folder_publish(workflow_action='publish', paths=paths,
            comment="Published by installer.", include_children=True)
    print >>out, 'Created testing content'

    return out.getvalue()

def install(self):
    """ Do stuff that GS will do for us soon ..
    """
    out = StringIO()

    plone = getToolByName(self, 'portal_url').getPortalObject()

    # Filter the global tabs
    plone.Members # hide ...

    # Add default content
    result = add_default_content(self)
    print >>out, result


def uninstall(self):
    out = StringIO()

    plone = getToolByName(self, 'portal_url').getPortalObject()
    normalizeString = getToolByName(self, 'plone_utils').normalizeString
    ids = [d.get('id', normalizeString(d['title'])) for d in DEFAULT_SITE_CONTENT]
    ids = [i for i in ids if plone.get(i, None)]
    plone.manage_delObjects(ids) 
    print >>out, 'Deleted our testing content'

    return out.getvalue()
