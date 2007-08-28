# -*- coding: utf-8 -*-
#
# File: RotaFolder.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 1.6.0-beta-svn
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
from zope import interface
from Products.Bungeni.interfaces.IRotaFolder import IRotaFolder
from Products.Bungeni.config import *

# additional imports from tagged value 'import'
from Products.OrderableReferenceField import OrderableReferenceField

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr
##/code-section module-header

schema = Schema((

    OrderableReferenceField(
        name='AvailableReporters',
        vocabulary='getReportersVocab',
        widget=OrderableReferenceField._properties['widget'](
            label='Availablereporters',
            label_msgid='Bungeni_label_AvailableReporters',
            i18n_domain='Bungeni',
        ),
        allowed_types=['Staff'],
        relationship="rotafolder_availablereporters",
        relation_implementation="basic"
    ),

    DateTimeField(
        name='RotaFrom',
        widget=CalendarWidget(
            label='Rotafrom',
            label_msgid='Bungeni_label_RotaFrom',
            i18n_domain='Bungeni',
        )
    ),

    DateTimeField(
        name='RotaTo',
        widget=CalendarWidget(
            label='Rotato',
            label_msgid='Bungeni_label_RotaTo',
            i18n_domain='Bungeni',
        )
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

RotaFolder_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class RotaFolder(BaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseFolder,'__implements__',()),)
    # zope3 interfaces
    interface.implements(IRotaFolder)

    # This name appears in the 'add' box
    archetype_name = 'RotaFolder'

    meta_type = 'RotaFolder'
    portal_type = 'RotaFolder'
    allowed_content_types = ['RotaItem']
    filter_content_types = 1
    global_allow = 0
    #content_icon = 'RotaFolder.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "RotaFolder"
    typeDescMsgId = 'description_edit_rotafolder'


    actions =  (


       {'action': "string:${object_url}/generateRota",
        'category': "object",
        'id': 'generateRota',
        'name': 'generateRota',
        'permissions': ("View",),
        'condition': 'python:1'
       },


    )

    _at_rename_after_creation = True

    schema = RotaFolder_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(RotaFolder, PROJECTNAME)
# end of class RotaFolder

##code-section module-footer #fill in your manual code here
def addedRotaFolder(obj, event):
    """ After the folder has been added, populate it with RotaItems
    based on the AvailableReporters.
    """
    from ipdb import set_trace; set_trace()
    normalizeString = getToolByName(obj, 'plone_utils').normalizeString
    reporters = obj.getReporters()
    # TODO order reporters by weight.
    obj.setAvailableReporters(reporters)
    for r in reporters:
        title = 'Reporter: %s'%r.Title()
        ri_id = normalizeString(title)
        if not shasattr(obj, ri_id):
            obj.invokeFactory('RotaItem', ri_id, title=title, Reporters=r.UID())
##/code-section module-footer



