# Permissions we want globally available
from Products.CMFCore import CMFCorePermissions

# Products that are integrated in Bungeni product. 
# The Plone site should be a membrane/remember site.
DEPENDENCIES = ['AddRemoveWidget', 'PloneHelpCenter',]

# Products that we want to use alongside Bungeni
DEPENDENCIES += [
    'iterate', # Installs CMFEditions, CMFDiffTool
    'Hornet', # Requires ZMySQLdb
    'TeamSpace',
    'LinguaPlone', # Installs PloneLanguageTool
    'CMFNotification', 
    'Plone4ArtistsCalendar', # Installs CMFonFive
    ]

# Note that though we need PloneHelpCenter in the Products dir, we don't
# want to install it, as we don't use its content types -- only the ones
# that we derive from it.
