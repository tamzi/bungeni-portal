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
from Products.Archetypes.utils import log
##/code-section module-header

copied_fields = {}
copied_fields['title'] = BaseSchema['title'].copy()
copied_fields['title'].default = "Rota"
schema = Schema((

    OrderableReferenceField(
        name='ReportersForSitting',
        vocabulary='getReportersForSittingVocab',
        widget=OrderableReferenceField._properties['widget'](
            macro_edit="reportersforsitting_edit",
            label='Reportersforsitting',
            label_msgid='Bungeni_label_ReportersForSitting',
            i18n_domain='Bungeni',
        ),
        allowed_types=['Staff'],
        relationship="rotafolder_reportersforsitting",
        relation_implementation="basic"
    ),

    ComputedField(
        name='RotaFrom',
        widget=ComputedField._properties['widget'](
            label='Rotafrom',
            label_msgid='Bungeni_label_RotaFrom',
            i18n_domain='Bungeni',
        )
    ),

    ComputedField(
        name='RotaTo',
        widget=ComputedField._properties['widget'](
            label='Rotato',
            label_msgid='Bungeni_label_RotaTo',
            i18n_domain='Bungeni',
        )
    ),

    copied_fields['title'],

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

RotaFolder_schema = OrderedBaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class RotaFolder(OrderedBaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),)
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

    security.declarePublic('getRotaFrom')
    def getRotaFrom(self):
        """
        """
        parent = self
        while parent.portal_type != 'Sitting':
            parent = parent.aq_parent
        return parent.start()

    security.declarePublic('getRotaTo')
    def getRotaTo(self):
        """
        """
        parent = self
        while parent.portal_type != 'Sitting':
            parent = parent.aq_parent
        return parent.end()


registerType(RotaFolder, PROJECTNAME)
# end of class RotaFolder

##code-section module-footer #fill in your manual code here
def addedRotaFolder(obj, event):
    """ After the folder has been added, populate it with RotaItems
    based on the AvailableReporters.
    """
    if obj.isTemporary():
        log('addedRotaFolder> Not yet!')
        return

    rt = getToolByName(obj, 'portal_rotatool')

    obj.setReportersForSitting(obj.REQUEST.form['ReportersForSitting'])
    reporters = obj.getReportersForSitting()

    # Get the lead/extra times as a fraction of a day (1440 minutes)
    lead_time_fraction = rt.getReportingLeadTime() / 1440.00
    extra_time_fraction = (rt.getExtraTakes() * rt.getTakeLength()) / 1440.00

    start_time = obj.getRotaFrom() - lead_time_fraction 
    end_time = obj.getRotaTo() + extra_time_fraction
    duration_in_minutes = (end_time - start_time) * 1440.00
    iterations = duration_in_minutes / rt.getTakeLength()
    reporter_index = 0

    # Generate the rota
    for n in range(iterations):
        if reporter_index == len(reporters):
            reporter_index = 0
        r = reporters[reporter_index]
        reporter_index += 1
        ri_id = obj.generateUniqueId('RotaItem')
        obj.invokeFactory('RotaItem', ri_id, Reporter=r.UID())
##/code-section module-footer



