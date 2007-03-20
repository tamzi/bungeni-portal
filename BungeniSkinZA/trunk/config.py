## PLONE AND SKIN PRODUCT SPECIFIC CONSTANTS
GLOBALS = globals()
GENERATOR_PRODUCT = "qPloneSkinDump"
PRODUCT_NAME = "BungeniSkinZA"
SKIN_NAME = "BungeniSkinZA"
BASE_SKIN_NAME = "Plone Default"


##
## SLOT FORMING CONSTANTS
##
## Skin Product's portlet lists for left and right columns.
## 'None' - mean that on installation slot will not be changed.
## ['some/portlet1','some/portlet2'] - will change appropriate (left or right)
##                                     slot to listed portlets
LEFT_SLOTS = ['here/portlet_navigation/macros/portlet', 'here/theme_portlet/macros/portlet', 'here/portlet_login/macros/portlet', 'here/global_searchbox/macros/quick_search']
RIGHT_SLOTS = ['here/sections_portlet/macros/portlet', 'here/portlet_calendar/macros/portlet', 'here/portlet_news/macros/portlet', 'here/portlet_events/macros/portlet']

## Slot's list forming procedure.
## "blend_with_skin" [default]- to SKIN PRODUCT'S slots list added unknown slots from SITE.
## "blend_with_site" - to SITE's slots list added unknown slots from SKIN PRODUCT.
## "replace" - in left and right site's columns placed ONLY SKIN PRODUCT's slots.
#SLOT_FORMING = "blend_with_skin"
#SLOT_FORMING = "blend_with_site"
#SLOT_FORMING = "replace"
SLOT_FORMING = "blend_with_skin"

## Favour column for slots forming procedure. IMPORTANT only for 'Blend with...' 
## Slot's list forming procedure.
## "left" OR "right" - if find same slots in left and right columns - than 
##                     slots move accordingly to left/right column.
## "both" - if find same slots in left and right columns - than slots 
##          positionings as in Master's slots lists - 
##          from SKIN PRODUCT's slots for 'Blend with skin' procedure
##          and SITE's slots for 'Blend with site' one.
#MAIN_COLUMN = "left"
#MAIN_COLUMN = "right"
#MAIN_COLUMN = "both"
MAIN_COLUMN = "both"


##
## CSS AND JAVASCRIPTS RESOURCES CONSTANTS
## Actual only for 2.1+ Plone. For older Plone version - this data not used.
## Work only if at least one of (DOES_COSTOMIZE_CSS, DOES_COSTOMIZE_JS)
## constant(s) set to True
##
## Does customize CSS or Javascripts resources - define if perform corresponding 
## registry customization.
#DOES_COSTOMIZE_CSS = True # Do portal_css customization
#DOES_COSTOMIZE_CSS = False # Do NOT portal_css customization
DOES_COSTOMIZE_CSS = True
#DOES_COSTOMIZE_JS = True # Do portal_javascripts customization
#DOES_COSTOMIZE_JS = False # Do NOT portal_javascripts customization
DOES_COSTOMIZE_JS = True

## Skin Product's CSS and Javascript lists.
CSS_LIST = ['public.css']
JS_LIST = []

## CSS and Javascript registries settings for Skin Product.
## Actual for right functionality css-es and ECMA scripts.
## For manually changing you must know what you do.
SKIN_CSS_REGDATA = [{'cacheable': True, 'compression': 'safe', 'title': '', 'expression': '', 'enabled': 1, 'rendering': 'import', 'rel': 'stylesheet', 'media': 'screen', 'cookable': True, 'id': 'base.css'}, {'cacheable': True, 'compression': 'safe', 'title': '', 'expression': '', 'enabled': 1, 'rendering': 'import', 'rel': 'stylesheet', 'media': 'screen', 'cookable': True, 'id': 'public.css'}, {'cacheable': True, 'compression': 'safe', 'title': '', 'expression': '', 'enabled': 1, 'rendering': 'import', 'rel': 'stylesheet', 'media': 'screen', 'cookable': True, 'id': 'columns.css'}, {'cacheable': True, 'compression': 'safe', 'title': '', 'expression': '', 'enabled': 1, 'rendering': 'import', 'rel': 'stylesheet', 'media': 'screen', 'cookable': True, 'id': 'authoring.css'}, {'cacheable': True, 'compression': 'safe', 'title': '', 'expression': '', 'enabled': 1, 'rendering': 'import', 'rel': 'stylesheet', 'media': 'screen', 'cookable': True, 'id': 'portlets.css'}, {'cacheable': True, 'compression': 'safe', 'title': '', 'expression': '', 'enabled': 1, 'rendering': 'import', 'rel': 'stylesheet', 'media': 'projection', 'cookable': True, 'id': 'presentation.css'}, {'cacheable': True, 'compression': 'safe', 'title': '', 'expression': '', 'enabled': 1, 'rendering': 'import', 'rel': 'stylesheet', 'media': 'print', 'cookable': True, 'id': 'print.css'}, {'cacheable': True, 'compression': 'safe', 'title': '', 'expression': '', 'enabled': 1, 'rendering': 'import', 'rel': 'stylesheet', 'media': 'handheld', 'cookable': True, 'id': 'mobile.css'}, {'cacheable': True, 'compression': 'safe', 'title': '', 'expression': '', 'enabled': 1, 'rendering': 'import', 'rel': 'stylesheet', 'media': 'screen', 'cookable': True, 'id': 'deprecated.css'}, {'cacheable': True, 'compression': 'safe', 'title': '', 'expression': '', 'enabled': 1, 'rendering': 'import', 'rel': 'stylesheet', 'media': 'screen', 'cookable': True, 'id': 'generated.css'}, {'cacheable': True, 'compression': 'safe', 'title': '', 'expression': 'not: portal/portal_membership/isAnonymousUser', 'enabled': 1, 'rendering': 'import', 'rel': 'stylesheet', 'media': 'screen', 'cookable': True, 'id': 'member.css'}, {'cacheable': True, 'compression': 'safe', 'title': '', 'expression': 'object/@@plone/isRightToLeft', 'enabled': 1, 'rendering': 'import', 'rel': 'stylesheet', 'media': 'screen', 'cookable': True, 'id': 'RTL.css'}, {'cacheable': True, 'compression': 'safe', 'title': 'Small Text', 'expression': '', 'enabled': 1, 'rendering': 'link', 'rel': 'alternate stylesheet', 'media': 'screen', 'cookable': True, 'id': 'textSmall.css'}, {'cacheable': True, 'compression': 'safe', 'title': 'Large Text', 'expression': '', 'enabled': 1, 'rendering': 'link', 'rel': 'alternate stylesheet', 'media': 'screen', 'cookable': True, 'id': 'textLarge.css'}, {'cacheable': True, 'compression': 'safe', 'title': '', 'expression': 'python:portal.kupu_library_tool.isKupuEnabled(REQUEST=request)', 'enabled': True, 'rendering': 'import', 'rel': 'stylesheet', 'media': '', 'cookable': True, 'id': 'kupustyles.css'}, {'cacheable': True, 'compression': 'safe', 'title': '', 'expression': 'python:portal.kupu_library_tool.isKupuEnabled(REQUEST=request)', 'enabled': True, 'rendering': 'import', 'rel': 'stylesheet', 'media': '', 'cookable': True, 'id': 'kupuplone.css'}, {'cacheable': True, 'compression': 'safe', 'title': '', 'expression': 'python:portal.kupu_library_tool.isKupuEnabled(REQUEST=request)', 'enabled': True, 'rendering': 'import', 'rel': 'stylesheet', 'media': '', 'cookable': True, 'id': 'kupudrawerstyles.css'}, {'cacheable': True, 'compression': 'safe', 'title': '', 'expression': '', 'enabled': True, 'rendering': 'import', 'rel': 'stylesheet', 'media': 'all', 'cookable': True, 'id': 'bungeni.css'}, {'cacheable': True, 'compression': 'safe', 'title': '', 'expression': 'object/isAnnotatable|nothing', 'enabled': True, 'rendering': 'import', 'rel': 'stylesheet', 'media': 'all', 'cookable': True, 'id': 'marginalia.css'}, {'cacheable': True, 'compression': 'safe', 'title': '', 'expression': '', 'enabled': 1, 'rendering': 'import', 'rel': 'stylesheet', 'media': 'all', 'cookable': True, 'id': 'ploneCustom.css'}]
SKIN_JS_REGDATA = [{'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'event-registration.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'register_function.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'cssQuery.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'plone_javascript_variables.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'nodeutilities.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'cookie_functions.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'livesearch.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'fullscreenmode.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'select_all.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'dropdown.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'dragdropreorder.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'mark_special_links.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'collapsiblesections.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'highlightsearchterms.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'se-highlight.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'first_input_focus.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'folder_contents_filter.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'folder_contents_hideAddItems.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'styleswitcher.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'table_sorter.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'calendar_formfield.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'calendarpopup.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'ie5fixes.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'formUnload.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'sarissa.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': '', 'inline': '', 'cookable': True, 'id': 'plone_minwidth.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': '', 'inline': '', 'cookable': True, 'id': 'correctPREformatting.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'login.js'}, {'cacheable': True, 'compression': 'safe', 'expression': '', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'formsubmithelpers.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'python:portal.kupu_library_tool.isKupuEnabled(REQUEST=request)', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'kupunoi18n.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'python:portal.kupu_library_tool.isKupuEnabled(REQUEST=request)', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'sarissa_ieemu_xpath.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'python:portal.kupu_library_tool.isKupuEnabled(REQUEST=request)', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'kupuhelpers.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'python:portal.kupu_library_tool.isKupuEnabled(REQUEST=request)', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'kupueditor.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'python:portal.kupu_library_tool.isKupuEnabled(REQUEST=request)', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'kupubasetools.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'python:portal.kupu_library_tool.isKupuEnabled(REQUEST=request)', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'kupuloggers.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'python:portal.kupu_library_tool.isKupuEnabled(REQUEST=request)', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'kupucontentfilters.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'python:portal.kupu_library_tool.isKupuEnabled(REQUEST=request)', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'kupucontextmenu.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'python:portal.kupu_library_tool.isKupuEnabled(REQUEST=request)', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'kupuploneeditor.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'python:portal.kupu_library_tool.isKupuEnabled(REQUEST=request)', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'kupuploneui.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'python:portal.kupu_library_tool.isKupuEnabled(REQUEST=request)', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'kupusourceedit.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'python:portal.kupu_library_tool.isKupuEnabled(REQUEST=request)', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'kupudrawers.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'python:portal.kupu_library_tool.isKupuEnabled(REQUEST=request)', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'kupuploneinit.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'object/isAnnotatable|nothing', 'enabled': True, 'inline': '', 'cookable': True, 'id': '3rd-party.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'object/isAnnotatable|nothing', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'log.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'object/isAnnotatable|nothing', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'config.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'object/isAnnotatable|nothing', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'prefs.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'object/isAnnotatable|nothing', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'html-model.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'object/isAnnotatable|nothing', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'domutil.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'object/isAnnotatable|nothing', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'ranges.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'object/isAnnotatable|nothing', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'post-micro.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'object/isAnnotatable|nothing', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'linkable.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'object/isAnnotatable|nothing', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'marginalia.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'object/isAnnotatable|nothing', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'annotation.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'object/isAnnotatable|nothing', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'rest-annotate.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'object/isAnnotatable|nothing', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'static-annotate.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'object/isAnnotatable|nothing', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'rest-prefs.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'object/isAnnotatable|nothing', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'rest-keywords.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'object/isAnnotatable|nothing', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'strings.js'}, {'cacheable': True, 'compression': 'safe', 'expression': 'object/isAnnotatable|nothing', 'enabled': True, 'inline': '', 'cookable': True, 'id': 'static-prefs.js'}]


##
## IMPORTING OBJECTS TO PORTAL ROOT
##
## *IMPORT_POLICY* define importing behavior in case of presenting identical 
## ids among both - portal root objects and imported objects from 
## <SkinProduct>/import subdirectory.
## "only_new" [default]- imported objects with same ids are ignored - not imported.
## "backup" - in case of presenting same id objects, in portal root creates
##            back_[date] directory, where moved all same id's objects from
##            portal root. Then all objects are imported to portal root.
## "overwrite" - all objects in portal root with same ids are deleted. Then all 
##               objects are imported to portal root.
#
#IMPORT_POLICY = "backup"
#IMPORT_POLICY = "overwrite"
#IMPORT_POLICY = "only_new"
IMPORT_POLICY = "None"


##
## CUSTOMIZATION FUNCTIONS
##
## FINAL_CUSTOMIZATION_FUNCTIONS - list of additional customization functions.
## For perform additional customization in the SkinProduct - write in this config.py
## module a customization function(s) and add its name(s) to FINAL_CUSTOMIZATION_FUNCTIONS
## constant list. Customization function must acept 2 parameters: 'portal' and 'out'.
## Example:    
## def myCustomization(portal, out):
##     # Clear right slots for portal
##     portal.manage_addProperty('my_prop', 'my_value', type='string')
##     print >> out, "right slots deleted for portal."
## FINAL_CUSTOMIZATION_FUNCTIONS = [myCustomization]
from Products.CMFCore.utils import getToolByName
FINAL_CUSTOMIZATION_FUNCTIONS = []
