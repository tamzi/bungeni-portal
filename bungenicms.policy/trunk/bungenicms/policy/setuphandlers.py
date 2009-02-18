import logging

def setup_members_folder(context):
    """Set up the members folder at <root>/members.

    These are the steps:
    
    1.  Create a large plone folder in public home /members (or
    whatever you wish to call it)

    2.  ( If there is no large plone folder in drop down go to add
    large plone folder)

    3.  Then goto root and then bring your new /members/ folder from
    public home to Plone root at aq_parent. The Members folder has to
    be at the root, not public_home.

    4.  Goto portal membership properties at
    /aq_parent/portal_membership/manage_mapRoles

    5.  Set Member type to Large Plone folder if that is what you
    want.

    6.  Set Members folder to desired url e.g. /members or /artists

    7.  If desired cut and paste members from old Members folder and
    place them in new folder.

    8.  If you wish the new Members folder can be excluded from
    navigation bar.
    """

    if context.readDataFile('marker.txt') is None:
        return

    portal = context.getSite()

    if 'members' in portal.objectIds():
        return logging.warn("Members folder already exists.")

    # create members folder (Large Plone Folder)
    pt = portal['portal_types']
    old_global_allow = pt['Large Plone Folder'].global_allow
    pt['Large Plone Folder'].global_allow = True
    members = portal[
        portal.invokeFactory(
            "Large Plone Folder",
            id="members")]
    pt['Large Plone Folder'].global_allow = old_global_allow
    
    # set default properties
    members.setTitle("Members")
    members.setDescription("Members of parliaments")
    members.reindexObject()    

    # set members folder
    pm = portal['portal_membership']
    pm.setMembersFolderById('members')
