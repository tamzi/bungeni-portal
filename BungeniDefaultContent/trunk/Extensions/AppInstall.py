from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.BungeniDefaultContent.config import *

def add_default_content(root, structure, initial_transitions=['publish']):
    """ Create default content
    """
    out = StringIO()
    plone = getToolByName(root, 'portal_url').getPortalObject()

    def add_object(parent, d):
        obj_id = d.get('id', None)
        if obj_id is None:
            obj_id = plone.generateUniqueId(d['type'])
        if d['type'].endswith('Criterion'):
            obj = parent.addCriterion(d['field'], d['type'])
        elif d['type'] == 'Team Membership':
            obj = parent.addMember(obj_id)
        else:
            parent.invokeFactory(d['type'], obj_id,)
            obj = parent[obj_id]
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
    add_structure(plone, structure)

    def do_transition(root, structure, transition):
        """ Perform the initial workflow transition(s)
        """
        normalizeString = getToolByName(plone, 'plone_utils').normalizeString
        ids = [d.get('id', normalizeString(d['title'])) for d in structure]
        paths = ['/'.join(root[i].getPhysicalPath()) for i in ids]
        root.folder_publish(workflow_action=transition, paths=paths,
                comment="Installer: %s."%transition, include_children=True)

    if initial_transitions:
        for t in initial_transitions:
            do_transition(root, structure, t)

    print >>out, 'Created testing content'

    return out.getvalue()

def install(self):
    """ Do stuff that GS will do for us soon ..
    """
    out = StringIO()

    #
    # Filter the navigation
    #
    ntp = getToolByName(self, 'portal_properties').navtree_properties

    # Repeat from Products/TeamSpace/Extensions/Install.py .. it gets
    # squashed by remember/profiles/default/propertiestool.xml
    prop_name = 'metaTypesNotToList'
    blacklist = ntp.getProperty(prop_name)
    if blacklist is not None:
        blacklist = list(blacklist)
        if not 'TeamsTool' in blacklist:
            blacklist.append('TeamsTool')
        ntp.manage_changeProperties(**{prop_name:tuple(blacklist)})

    # Rename the teams tool: ?
    # TODO tt = getToolByName(self, 'portal_teams')

    # Filter the global tabs
    # TODO

    # Add default content
    result = add_default_content(self, DEFAULT_SITE_CONTENT)
    print >>out, result

    # Add default committees
    tt = getToolByName(self, 'portal_teams')
    result = add_default_content(tt, DEFAULT_TEAMS, initial_transitions=[])
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
