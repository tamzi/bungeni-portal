## Controller Python Script "logged_in"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Initial post-login actions
##

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
REQUEST=context.REQUEST


group_tool = getToolByName(context, 'portal_groups') 
parentGroup = group_tool.getGroupWorkspacesFolder()
grouplist = group_tool.searchGroups()

def createGroupArea(groupid, grouptitle, parentFolder):
    """Use the log-in as a hook to create group workspaces.
    The groups are created from the bungeni application and
    not through the traditional Groups tab.
    """
    
    if groupid not in context.groups.objectIds(): 
     
        group = context.portal_groups.getGroupById(groupid)
        members = [group.id for group in group.getGroupMembers()]
        if groupid not in parentFolder.objectIds():
            parentFolder.invokeFactory('Folder', groupid, title=grouptitle)
            obj = getattr(parentFolder, groupid, None)
            obj.setTitle("%s workspace" %grouptitle)
            obj.setDescription("Container for objects shared by this group")
            obj.manage_setLocalRoles(groupid, ['Owner'])
            #obj._getWorkflowTool().doActionFor(obj, 'publish' '')
            obj.update
            obj.reindexObject()

        
for group in grouplist:
    if group.has_key('plugin'):
        if group['groupid'].rsplit('.')[1] == 'parliament':
            createGroupArea(group['groupid'], group['title'], parentGroup)
            parentFolder = getattr(parentGroup, group['groupid'])

[createGroupArea(group['groupid'], group['title'], parentFolder ) for group in grouplist if group.has_key('plugin') and group['groupid'].rsplit('.')[1] != 'parliament']


membership_tool=getToolByName(context, 'portal_membership')
if membership_tool.isAnonymousUser():
    REQUEST.RESPONSE.expireCookie('__ac', path='/')
    context.plone_utils.addPortalMessage(_(u'Login failed. Both login name and password are case sensitive, check that caps lock is not enabled.'), 'error')
    return state.set(status='failure')

member = membership_tool.getAuthenticatedMember()
login_time = member.getProperty('login_time', '2000/01/01')
initial_login = int(str(login_time) == '2000/01/01')
state.set(initial_login=initial_login)

must_change_password = member.getProperty('must_change_password', 0)
state.set(must_change_password=must_change_password)

if initial_login:
    state.set(status='initial_login')
elif must_change_password:
    state.set(status='change_password')

membership_tool.loginUser(REQUEST)


return state



