from Products.CMFCore.permissions import setDefaultRoles

product_globals = globals()

PROJECTNAME = "bungeni.marginalia"
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))

