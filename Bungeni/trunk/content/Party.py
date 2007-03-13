# -*- coding: utf-8 -*-
#
# File: Party.py
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

__author__ = """Jean Jordaan <jean.jordaan@gmail.com>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.TeamSpace.team import Team
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='shortTitle',
        widget=StringWidget(
            label='Shorttitle',
            label_msgid='Bungeni_label_shortTitle',
            i18n_domain='Bungeni',
        )
    ),

    DateTimeField(
        name='registrationDate',
        widget=CalendarWidget(
            label='Registrationdate',
            label_msgid='Bungeni_label_registrationDate',
            i18n_domain='Bungeni',
        )
    ),

    DateTimeField(
        name='cessationDate',
        widget=CalendarWidget(
            label='Cessationdate',
            label_msgid='Bungeni_label_cessationDate',
            i18n_domain='Bungeni',
        )
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Party_schema = BaseSchema.copy() + \
    getattr(Team, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Party(BaseContent, Team):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),) + (getattr(Team,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Party'

    meta_type = 'Party'
    portal_type = 'Party'
    allowed_content_types = [] + list(getattr(Team, 'allowed_content_types', []))
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'Party.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Party"
    typeDescMsgId = 'description_edit_party'

    _at_rename_after_creation = True

    schema = Party_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(Party, PROJECTNAME)
# end of class Party

##code-section module-footer #fill in your manual code here
##/code-section module-footer



