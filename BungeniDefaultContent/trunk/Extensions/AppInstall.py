from StringIO import StringIO
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName
from Products.BungeniDefaultContent.config import *

new_actions = (
        {'id': 'glossary',
         'name': 'Glossary',
         'action': 'string:${portal_url}/help/glossary',
         'permission': View,
         'category': 'site_actions',},
        {'id': 'faq',
         'name': 'FAQ',
         'action': 'string:${portal_url}/help/faq',
         'permission': View,
         'category': 'site_actions',},
        {'id': 'help',
         'name': 'Help',
         'action': 'string:${portal_url}/help',
         'permission': View,
         'category': 'site_actions',},
        )

def get_id(d):
    """ Look for an id in a dictionary
    """
    id = d.get('id', d.get('title'))
    if id:
        return id
    if d.has_key('firstname'):
        return ' '.join([n for n in [d['firstname'], d['surname']] if n])

def do_transition(root, structure, transition):
    """ Perform the initial workflow transition(s)
    """
    normalizeString = getToolByName(root, 'plone_utils').normalizeString
    folderish_ids = []
    for d in structure:
        id = normalizeString(get_id(d))
        if d.get('children'):
            folderish_ids.append(id)
        else:
            obj = root.get(id, None)
            if obj:
                obj.content_status_modify(transition,
                        'Installer: %s'%transition, None, None,)
    paths = ['/'.join(root[i].getPhysicalPath()) for i in folderish_ids]
    if paths:
        root.folder_publish(workflow_action=transition, paths=paths,
                comment="Installer: %s."%transition, include_children=True)

def add_default_content(root, structure, initial_transitions=['publish']):
    """ Create default content
    """
    out = StringIO()
    plone = getToolByName(root, 'portal_url').getPortalObject()
    normalizeString = getToolByName(plone, 'plone_utils').normalizeString

    def add_object(parent, d):
        obj_id = normalizeString(get_id(d))
        if 'Criteri' in d['type']:
            obj = parent.addCriterion(d['field'], d['type'])
            obj.edit(**d)
        elif d['type'] == 'Team Membership':
            obj = parent.addMember(obj_id)
            do_transition(parent, [d], 'activate')
        else:
            parent.invokeFactory(d['type'], obj_id,)
            obj = parent[obj_id]
            layout = d.get('layout', None)
            if layout:
                obj.setLayout(layout)
            if obj.portal_type == 'Team':
                roles = list(obj.getAllowedTeamRoles())
                roles.extend(d.get('allowed_team_roles', []))
                obj.setAllowedTeamRoles(roles)
                roles = list(obj.getDefaultRoles())
                roles.extend(d.get('default_team_roles', []))
                obj.setDefaultRoles(roles)
            if obj.portal_type == 'TeamSpace':
                team_ids = [normalizeString(d['title'])]
                team_ids.extend(d.get('team_ids', []))
                obj.editTeams(team_ids)
        if not 'Criteri' in d['type']:
            # Criterions shouldn't get cataloged, and processForm does this.
            obj.processForm(data=1, values=d)
        return obj

    def add_structure(root, structure):
        """ Recursively add content as specified in tuples of dicts.
        """
        for d in structure:
            obj = add_object(root, d)
            if d.get('children', None):
                add_structure(obj, d['children'])
    add_structure(root, structure)

    if initial_transitions:
        for t in initial_transitions:
            do_transition(root, structure, t)

    print >>out, 'Created testing content'

    return out.getvalue()

def install(self):
    """ Do stuff that GS will do for us soon ..
    """
    out = StringIO()
    plone = getToolByName(self, 'portal_url').getPortalObject()
    normalizeString = getToolByName(plone, 'plone_utils').normalizeString

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

    # Add some of the new content to the site actions
    actions_tool = getToolByName(self, 'portal_actions')
    for action in new_actions:
        actions_tool.addAction(
                action.get('id'),
                action.get('name'),
                action.get('action'),
                action.get('condition'),
                action.get('permission'),
                action.get('category'),
                visible=1,
                )

    #
    # Add default members
    #
    properties_tool = getToolByName(self, 'portal_properties')
    # Don't send mail while adding
    properties_tool.site_properties.manage_changeProperties(validate_email=0)
    memberdata_tool = getToolByName(self, 'portal_memberdata')
    result = add_default_content(memberdata_tool, DEFAULT_MEMBERS,
            initial_transitions=['trigger',])
    # OK, start sending mail again
    properties_tool.site_properties.manage_changeProperties(validate_email=1)
    print >>out, result

    # Add default groups
    portal_groups = getToolByName(self, 'portal_groups')
    portal_groupdata = getToolByName(self, 'portal_groupdata')
    for group_dict in DEFAULT_GROUPS:
        group_id = group_dict['title']
        group = portal_groups.getGroupById(group_id)
        if not group:
            portal_groups.addGroup(group_id)
            group = portal_groups.getGroupById(group_id)

        processed={}
        for id, property in portal_groupdata.propertyItems():
            processed[id]=group_dict.get(id, None)
        group.setGroupProperties(processed)

        for member_title in group_dict['members']:
            member_id = normalizeString(member_title)
            group.addMember(member_id)
        roles = group_dict.get('roles', None)
        if roles:
            portal_groups.editGroup(group_id,
                    roles=[r for r in group_dict['roles']])

    # Rename the teams tool: ?
    # TODO teams_tool = getToolByName(self, 'portal_teams')

    # Add default committees
    teams_tool = getToolByName(self, 'portal_teams')
    result = add_default_content(teams_tool, DEFAULT_TEAMS, initial_transitions=[])
    print >>out, result

    # Add default content
    result = add_default_content(self, DEFAULT_SITE_CONTENT)
    print >>out, result
    result = add_default_content(self, DEFAULT_WORKSPACES, initial_transitions=[])
    print >>out, result

    # Publish existing content
    # We don't want this content to be deleted upon uninstallation
    do_transition(self, EXISTING_SITE_CONTENT, transition='publish')
    print >>out, 'Published existing content'

    # Filter the global tabs
    # TODO

    # Hide from navigation
    for obj in [self.Members, self.workspace, self.help, ]:
        obj.setExcludeFromNav(True)
        obj.reindexObject()


def uninstall(self):
    out = StringIO()

    plone = getToolByName(self, 'portal_url').getPortalObject()
    normalizeString = getToolByName(self, 'plone_utils').normalizeString

    # Delete the content we added
    ids = [normalizeString(get_id(d)) for d in DEFAULT_SITE_CONTENT+DEFAULT_WORKSPACES]
    ids = [i for i in ids if plone.get(i, None)]
    plone.manage_delObjects(ids) 
    print >>out, 'Deleted our testing content'

    # Delete the members we added
    membership_tool = getToolByName(self, 'portal_membership')
    membership_tool.deleteMembers([
            normalizeString(get_id(d)) for d in DEFAULT_MEMBERS])
    print >>out, 'Deleted our testing members'

    # Delete the groups we added
    portal_groups = getToolByName(self, 'portal_groups')
    group_ids = [normalizeString(group['title']) for group in DEFAULT_GROUPS]
    group_ids = [i for i in group_ids if portal_groups.getGroupById(i)]
    portal_groups.removeGroups(group_ids)

    # Delete the teams we added
    teams_tool = getToolByName(self, 'portal_teams')
    ids = [normalizeString(get_id(d)) for d in DEFAULT_TEAMS]
    ids = [i for i in ids if teams_tool.get(i, None)]
    teams_tool.manage_delObjects(ids) 
    print >>out, 'Deleted our testing teams'

    # Automatic?
    # # Remove the new actions
    # REMOVE_ACTIONS=[a['id'] for a in new_actions]
    # idxs = []
    # idx = 0
    # actions_tool = getToolByName(self, 'portal_actions')
    # for action in actions_tool.listActions():
    #     if action.getId() in REMOVE_ACTIONS:
    #         idxs.append(idx)
    #         print >>out, 'Will remove action %s'%action.getId()
    #     idx += 1
    # actions_tool.deleteActions(idxs)
    # print >>out, 'Removed our actions'

    return out.getvalue()
