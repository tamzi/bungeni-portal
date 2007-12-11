# -*- coding: utf-8 -*-
# Dependend products - not quick-installed - used in testcase
# override in custom configuration
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
PROJECTNAME = "BungeniHelpCenter"
product_globals = globals()
PRODUCT_DEPENDENCIES = []
DEPENDENCIES = ['PloneHelpCenter', 'AddRemoveWidget', 'PortalTaxonomy']

RESOURCES_CSS = {'TabbedSubpages.css' : 'screen'}
RESOURCES_JS = ('TabbedSubpages.js',)
TYPE_PARAMS = {}
TYPE_PARAMS['TabbedSubpages'] = { 'portal_type' : 'TabbedSubpages'
                                , 'archetype_name' : 'Tabbed Subpages'
                                , 'default_view' : 'tabbed_subpages_view'
                                }

