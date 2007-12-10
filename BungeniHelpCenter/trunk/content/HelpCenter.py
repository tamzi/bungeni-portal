# -*- coding: utf-8 -*-
try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *
try:
    import Products.CMFCore.permissions as CMFCorePermissions
except ImportError:
    from Products.CMFCore import CMFCorePermissions

from Products.BungeniHelpCenter.config import *
from Products.PloneHelpCenter.content.PHCContent import PHCContent

from Products.PloneHelpCenter.content import ReferenceManual, Tutorial
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin, fti_meta_type

HelpCenterReferenceManual = ReferenceManual.HelpCenterReferenceManual

class BungeniHelpCenterReferenceManual(BrowserDefaultMixin,  HelpCenterReferenceManual):
    """A reference manual containing ReferenceManualPages,
    ReferenceManualSections, Files and Images.
    """

    __implements__ =(PHCContent.__implements__,
                      OrderedBaseFolder.__implements__,)

    archetype_name = 'Reference Manual'
    meta_type='HelpCenterReferenceManual'
    content_icon = 'referencemanual_icon.gif'

    global_allow = 0
    filter_content_types = 1
    allowed_content_types =('HelpCenterReferenceManualPage', 
                             'HelpCenterReferenceManualSection', 
                             'Image', 'File')
    # allow_discussion = IS_DISCUSSABLE

    typeDescription= 'A Reference Manual can contain Reference Manual Pages and Sections, Images and Files. Index order is decided by the folder order, use the normal up/down arrow in the folder content view to rearrange content.'
    typeDescMsgId  = 'description_edit_referencemanual'

    default_view = 'referencemanual_view'
    suppl_views = ('referencemanual_view_roman', 'referencemanual_view_letter',)

    actions = (
        {'id'          : 'view',
         'name'        : 'View',
         'action'      : 'string:${object_url}',
         'permissions' : (CMFCorePermissions.View,)
         },
        {'id'          : 'edit',
         'name'        : 'Edit',
         'action'      : 'string:${object_url}/edit',
         'permissions' : (CMFCorePermissions.ModifyPortalContent,),
         },
        {'id'          : 'metadata',
         'name'        : 'Properties',
         'action'      : 'string:${object_url}/properties',
         'permissions' : (CMFCorePermissions.ModifyPortalContent,),
         },
        {'id'          : 'local_roles',
         'name'        : 'Sharing',
         'action'      : 'string:${object_url}/sharing',
         'permissions' : (CMFCorePermissions.ManageProperties,),
         },
        )

    aliases = {
        '(Default)'  : '(dynamic view)',
        'view'       : '(selected layout)',
        'index.html' : '',
        'edit'       : 'base_edit',
        'properties' : 'base_metadata',
        'sharing'    : 'folder_localrole_form',
        'stats'      : 'phc_stats',
        'gethtml'    : '',
        'mkdir'      : '',
        }

registerType(BungeniHelpCenterReferenceManual, PROJECTNAME)

HelpCenterTutorial = Tutorial.HelpCenterTutorial

class BungeniHelpCenterTutorial(BrowserDefaultMixin, HelpCenterTutorial):
    """A tutorial containing TutorialPages, Files and Images."""

    __implements__ = (PHCContent.__implements__,
                      OrderedBaseFolder.__implements__,)

    archetype_name = 'Tutorial'
    meta_type = portal_type = 'HelpCenterTutorial'
    content_icon = 'tutorial_icon.gif'

    global_allow = 0
    filter_content_types = 1
    allowed_content_types = ('HelpCenterTutorialPage', 'Image', 'File')
    # allow_discussion = IS_DISCUSSABLE

    typeDescription= 'A Tutorial can contain Tutorial Pages, Images and Files. Index order is decided by the folder order, use the normal up/down arrow in the folder content view to rearrange content.'
    typeDescMsgId  = 'description_edit_tutorial'

    default_view = 'tutorial_view'
    suppl_views = ('tutorial_view_roman', 'tutorial_view_letter',)

    actions = (
        {'id'          : 'view',
         'name'        : 'View',
         'action'      : 'string:${object_url}',
         'permissions' : (CMFCorePermissions.View,)
         },
        {'id'          : 'edit',
         'name'        : 'Edit',
         'action'      : 'string:${object_url}/edit',
         'permissions' : (CMFCorePermissions.ModifyPortalContent,),
         },
        {'id'          : 'metadata',
         'name'        : 'Properties',
         'action'      : 'string:${object_url}/properties',
         'permissions' : (CMFCorePermissions.ModifyPortalContent,),
         },
        {'id'          : 'local_roles',
         'name'        : 'Sharing',
         'action'      : 'string:${object_url}/sharing',
         'permissions' : (CMFCorePermissions.ManageProperties,),
         },
        )

    aliases = {
        '(Default)'  : '(dynamic view)',
        'view'       : '(selected layout)',
        'index.html' : '',
        'edit'       : 'base_edit',
        'properties' : 'base_metadata',
        'sharing'    : 'folder_localrole_form',
        'stats'      : 'phc_stats',
        'gethtml'    : '',
        'mkdir'      : '',
        }

registerType(BungeniHelpCenterTutorial, PROJECTNAME)
