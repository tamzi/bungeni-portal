# -*- coding: utf-8 -*-
#
# File: bungeniremotefolder.py
#
# Copyright (c) 2008 by []
# Generator: ArchGenXML Version 2.1
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.bungeniremotecontent.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    TextField(
        name='body_text',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label='Body_text',
            label_msgid='bungeniremotecontent_label_body_text',
            i18n_domain='bungeniremotecontent',
        ),
        required=False,
        description="Detailed description of this folder listing",
        title="Body Text",
        default_output_type='text/html',
    ),
    StringField(
        name='source_url',
        widget=StringField._properties['widget'](
            label='Source_url',
            label_msgid='bungeniremotecontent_label_source_url',
            i18n_domain='bungeniremotecontent',
        ),
        required=True,
        title="remote URL",
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

bungeniremotefolder_schema = ATFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class bungeniremotefolder(ATFolder):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.Ibungeniremotefolder)

    meta_type = 'bungeniremotefolder'
    _at_rename_after_creation = True

    schema = bungeniremotefolder_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(bungeniremotefolder, PROJECTNAME)
# end of class bungeniremotefolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



