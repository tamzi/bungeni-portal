# Integrated in Bungeni product. 
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
