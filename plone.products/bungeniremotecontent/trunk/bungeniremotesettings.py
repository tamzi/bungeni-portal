# -*- coding: utf-8 -*-
#
# File: bungeniremotesettings.py
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


from Products.CMFCore.utils import UniqueObject

    
##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='host_url',
        widget=StringField._properties['widget'](
            label='Host_url',
            label_msgid='bungeniremotecontent_label_host_url',
            i18n_domain='bungeniremotecontent',
        ),
        required=True,
        title="Remote Host",
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

bungeniremotesettings_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class bungeniremotesettings(UniqueObject, BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.Ibungeniremotesettings)

    meta_type = 'bungeniremotesettings'
    _at_rename_after_creation = True

    schema = bungeniremotesettings_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # tool-constructors have no id argument, the id is fixed
    def __init__(self, id=None):
        BaseContent.__init__(self,'portal_bungeniremotesettings')
        self.setTitle('')
        
        ##code-section constructor-footer #fill in your manual code here
        ##/code-section constructor-footer


    # tool should not appear in portal_catalog
    def at_post_edit_script(self):
        self.unindexObject()
        
        ##code-section post-edit-method-footer #fill in your manual code here
        ##/code-section post-edit-method-footer


    # Methods


registerType(bungeniremotesettings, PROJECTNAME)
# end of class bungeniremotesettings

##code-section module-footer #fill in your manual code here
##/code-section module-footer



