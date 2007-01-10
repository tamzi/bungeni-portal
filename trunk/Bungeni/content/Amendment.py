# -*- coding: utf-8 -*-
#
# File: Amendment.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 1.5.1-svn
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    ReferenceField(
        name='bills',
        widget=ReferenceWidget(
            label='Bills',
            label_msgid='Bungeni_label_bills',
            i18n_domain='Bungeni',
        ),
        allowed_types=('Bill',),
        multiValued=0,
        relationship='amendment_bill'
    ),

    ReferenceField(
        name='billsections',
        widget=ReferenceWidget(
            label='Billsections',
            label_msgid='Bungeni_label_billsections',
            i18n_domain='Bungeni',
        ),
        allowed_types=('BillSection',),
        multiValued=0,
        relationship='amendment_billsection'
    ),

    ReferenceField(
        name='billpages',
        widget=ReferenceWidget(
            label='Billpages',
            label_msgid='Bungeni_label_billpages',
            i18n_domain='Bungeni',
        ),
        allowed_types=('BillPage',),
        multiValued=0,
        relationship='amendment_billpage'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Amendment_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Amendment(BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Amendment'

    meta_type = 'Amendment'
    portal_type = 'Amendment'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 1
    #content_icon = 'Amendment.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Amendment"
    typeDescMsgId = 'description_edit_amendment'

    _at_rename_after_creation = True

    schema = Amendment_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(Amendment, PROJECTNAME)
# end of class Amendment

##code-section module-footer #fill in your manual code here
##/code-section module-footer



