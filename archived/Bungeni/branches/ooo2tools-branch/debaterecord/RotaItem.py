# -*- coding: utf-8 -*-
#
# File: RotaItem.py
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
from Products.Bungeni.interfaces.IRotaItem import IRotaItem
from Products.Relations.field import RelationField
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
##/code-section module-header

schema = Schema((

    ComputedField(
        name='ItemOrder',
        widget=ComputedField._properties['widget'](
            label='Itemorder',
            label_msgid='Bungeni_label_ItemOrder',
            i18n_domain='Bungeni',
        )
    ),

    ComputedField(
        name='ItemFrom',
        widget=ComputedField._properties['widget'](
            label='Itemfrom',
            label_msgid='Bungeni_label_ItemFrom',
            i18n_domain='Bungeni',
        )
    ),

    ComputedField(
        name='ItemFromWithLead',
        widget=ComputedField._properties['widget'](
            label='Itemfromwithlead',
            label_msgid='Bungeni_label_ItemFromWithLead',
            i18n_domain='Bungeni',
        )
    ),

    ComputedField(
        name='ItemTo',
        widget=ComputedField._properties['widget'](
            label='Itemto',
            label_msgid='Bungeni_label_ItemTo',
            i18n_domain='Bungeni',
        )
    ),

    RelationField(
        name='Reporter',
        vocabulary='getReportersForSittingVocab',
        widget=ReferenceWidget(
            label='Reporter',
            label_msgid='Bungeni_label_Reporter',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='rotaitem_reporter'
    ),

    RelationField(
        name='Take',
        widget=ReferenceWidget(
            label='Take',
            label_msgid='Bungeni_label_Take',
            i18n_domain='Bungeni',
        ),
        multiValued=1,
        relationship='rotaitem_take'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

RotaItem_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class RotaItem(BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)
    # zope3 interfaces
    interface.implements(IRotaItem)

    # This name appears in the 'add' box
    archetype_name = 'RotaItem'

    meta_type = 'RotaItem'
    portal_type = 'RotaItem'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'RotaItem.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "RotaItem"
    typeDescMsgId = 'description_edit_rotaitem'

    _at_rename_after_creation = True

    schema = RotaItem_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('setReporter')
    def setReporter(self, value, **kw_args):
        """
        """
        catalog = getToolByName(self, 'portal_catalog')
        reporter_brains = catalog(UID=value)
        if reporter_brains:
            reporter = reporter_brains[0].getObject()
            self.setTitle('Reporter: %s'%reporter.Title())
            self.reindexObject()
        field = self.schema['Reporter']
        return field.set(self, value, **kw_args)

    security.declarePublic('getItemOrder')
    def getItemOrder(self):
        """
        """
        return self.aq_parent.getObjectPosition(self.getId())

    security.declarePublic('getItemFrom')
    def getItemFrom(self):
        """
        """
        rt = getToolByName(self, 'portal_rotatool')

        item_number = self.getItemOrder() + 1
        rota_start_time = self.aq_parent.getRotaFrom()
        item_start_time = rota_start_time + (
                item_number*rt.getTakeLength())/1440.00
        return item_start_time

    security.declarePublic('getItemFromWithLead')
    def getItemFromWithLead(self):
        """
        """
        rt = getToolByName(self, 'portal_rotatool')
        lead_time_fraction = rt.getReportingLeadTime() / 1440.00
        item_start_time = self.getItemFrom()
        return item_start_time - lead_time_fraction

    security.declarePublic('getItemTo')
    def getItemTo(self):
        """
        """
        rt = getToolByName(self, 'portal_rotatool')
        return self.getItemFrom() + rt.getTakeLength()/1440.00


registerType(RotaItem, PROJECTNAME)
# end of class RotaItem

##code-section module-footer #fill in your manual code here
##/code-section module-footer



