# -*- coding: utf-8 -*-
#
# File: Annotations.py
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

from zope import interface

from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from Products.CMFCore.utils import UniqueObject, getToolByName


from OFS.SimpleItem import SimpleItem

import config
import interfaces

schema = atapi.Schema((
    atapi.LinesField(
        name='keywords',
        default=('Agree:This is a good point', 'Disagree:I think this is wrong', 'More Info:I need more information on this',),
        widget=atapi.LinesField._properties['widget'](
            label='Keywords',
            label_msgid='Marginalia_label_keywords',
            i18n_domain='Marginalia',
        )
    ),
),
)

Annotations_schema = atapi.BaseBTreeFolderSchema.copy() + \
    schema.copy()

class Annotation(SimpleItem):
    interface.implements(interfaces.IAnnotation)
    
    def __init__(self, _id, path, **kwargs):
        self.id = _id
        self.path = path
        self.__dict__.update(**kwargs)

    def getPhysicalPath(self):
        return self.path + (self.id,)

class MarginaliaTool(UniqueObject, atapi.BaseBTreeFolder):
    """Annotations tool to keep Marginalia content."""

    interface.implements(interfaces.IMarginaliaTool)

    security = ClassSecurityInfo()
    __implements__ = (getattr(UniqueObject,'__implements__',()),) + \
                     (getattr(atapi.BaseBTreeFolder,'__implements__',()),)

    archetype_name = 'MarginaliaTool'
    meta_type = 'MarginaliaTool'
    portal_type = 'MarginaliaTool'
    allowed_content_types = []
    filter_content_types = 1
    global_allow = 0
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "MarginaliaTool"

    _at_rename_after_creation = True


    schema = Annotations_schema

    def at_post_edit_script(self):
        # tool should not appear in portal_catalog
        self.unindexObject()

    def create_annotation(self, **kw):
        # get first available id
        id_ = str(max(map(int, self.objectIds())) + 1)

        path = self.getPhysicalPath()
        annotation = Annotation(id_, path, **kw)
    
        self._set
        Object(id_, annotation)
        
        # todo: we'll need to add this to the catalog
        # catalog.catalog_object(annotation)
        
        catalog = getToolByName(context, 'marginalia_catalog')
        catalog.catalog_object(id_)

atapi.registerType(MarginaliaTool, config.PROJECTNAME)





