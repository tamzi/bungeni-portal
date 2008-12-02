# -*- coding: utf-8 -*-
#
# File: bungeniremotepage.py
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

from Products.bungeniremotecontent.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='source_url',
        widget=StringField._properties['widget'](
            label='Source_url',
            label_msgid='bungeniremotecontent_label_source_url',
            i18n_domain='bungeniremotecontent',
        ),
        description="Relative URL to the remote page",
        title="Source URL",
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

bungeniremotepage_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class bungeniremotepage(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.Ibungeniremotepage)

    meta_type = 'bungeniremotepage'
    _at_rename_after_creation = True

    schema = bungeniremotepage_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(bungeniremotepage, PROJECTNAME)
# end of class bungeniremotepage

##code-section module-footer #fill in your manual code here
##/code-section module-footer



