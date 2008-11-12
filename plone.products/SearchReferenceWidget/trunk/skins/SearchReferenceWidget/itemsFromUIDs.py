## Script (Python) "itemsFromUIDs"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=value
##title=Return a set of items from a UID or list of UIDs

from Products.CMFCore.utils import getToolByName
url_tool = getToolByName(context, 'portal_url')
portal = url_tool.getPortalObject()
rootLookupObject = portal.reference_catalog.lookupObject;
nearLookupObject = context.reference_catalog.lookupObject;

uids = same_type(value, []) and value or [value]
items = [nearLookupObject(uid) or rootLookupObject(uid) for uid in uids]

return items