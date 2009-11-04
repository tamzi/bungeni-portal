## Script (Python) "notifyMemberAreaCreated"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Modify new member area
##

# script to automatically create a private and a public folder in member's user area

from Products.CMFCore.utils import getToolByName
wftool = getToolByName(context, 'portal_workflow')

folders = [["private_folder", "Private Folder", 'private'], ["web_pages", "WebPages", 'public']]
for folder in folders:
    context.invokeFactory('Folder', id=folder[0])
    newfolder = getattr(context, folder[0])
    newfolder.setTitle(folder[1])
    if folder[2] =="public":
        wftool.doActionFor(newfolder, 'publish')
        newfolder.update
    newfolder.reindexObject()




