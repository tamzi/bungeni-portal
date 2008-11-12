# File: SearchReferenceWidget.py
#
# Copyright (c) 2007 by ['Dylan Jay']
# Generator: ArchGenXML Version 1.4.1
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

__author__ = """Dylan Jay <software@pretaweb.com>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Acquisition import aq_base

from Products.CMFCore.utils import getToolByName

from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.utils import DisplayList
from Products.Archetypes import config as atconfig
from Products.Archetypes.Widget import *
from Products.Archetypes.Widget import TypesWidget
from Products.generator import i18n

from Products.SearchReferenceWidget import config

##code-section module-header #fill in your manual code here
from Products.Archetypes.Widget import ReferenceWidget
##/code-section module-header



class SearchReferenceWidget(ReferenceWidget):
    ''' '''

    ##code-section class-header #fill in your manual code here
    def getDestination(self, instance):
        if not self.destination:
            purl = getToolByName(instance, 'portal_url')
            return purl.getRelativeUrl(aq_parent(instance))
        else:
            value = getattr(aq_base(instance), self.destination,
                            self.destination)
            if callable(value):
                value = value()

            return value
    ##/code-section class-header

    __implements__ = (getattr(TypesWidget,'__implements__',()),) + (getattr(ReferenceWidget,'__implements__',()),)

    _properties = ReferenceWidget._properties.copy()
    _properties.update({
        'macro' : 'searchreference_widget',
        ##code-section widget-properties #fill in your manual code here
        'addable' : 0, # create createObject link for every addable type
        'destination' : None, # may be:
                              # - ".", context object;
                              # - None, any place where
                              #   Field.allowed_types can be added;
                              # - string path;
                              # - name of method on instance
                              #   (it can be a combination list);
                              # - a list, combining all item above;
                              # - a dict, where
                              #   {portal_type:<combination of the items above>}
                              # destination is relative to portal root

        'base_search' : None,      # dictionary suitable for passing to catalog search. Unused if None.
        ##/code-section widget-properties

        })

    security = ClassSecurityInfo()


    def getDestination(self, instance):
        if not self.destination:
            purl = getToolByName(instance, 'portal_url')
            return purl.getRelativeUrl(aq_parent(instance))
        else:
            value = getattr(aq_base(instance), self.destination,
                            self.destination)
            if callable(value):
                value = value()

            return value
    ##/code-section class-header

registerWidget(SearchReferenceWidget,
               title='SearchReferenceWidget',
               description=('Renders a reference widget + input fields'),
               used_for=('Products.Archetypes.Field.ReferenceField',)
               )
##code-section module-footer #fill in your manual code here
##/code-section module-footer



