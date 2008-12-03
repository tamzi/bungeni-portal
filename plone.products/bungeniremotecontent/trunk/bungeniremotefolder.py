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
from Products.CMFCore.utils import getToolByName
import urllib, simplejson
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
        read_permission="Add portal content",
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

    # Manually created methods

    security.declarePublic('getRemoteFolderListing')
    def getRemoteFolderListing(self):
        """
        """
        bungeni_tool = getToolByName(self, "portal_bungeniremotesettings")
        lurl = bungeni_tool.host_url + self.source_url + bungeni_tool.json_listing
        turl = bungeni_tool.host_url + self.source_url + bungeni_tool.json_headers
        lf = urllib.urlopen(lurl)
        results = simplejson.load(lf)
        tf = urllib.urlopen(turl)
        ths = simplejson.load(tf)
        rs = "<table> <thead> <tr>"
        for th in ths:
            rs = rs + "<th> " + th['title'] +" </th>"
        rs = rs + "</tr> </thead> <tbody>"
        if results.has_key("nodes"):
            for tr in results['nodes']:
                rs = rs + "<tr>"
                for th in ths:                    
                        rs = rs + "<td> " + tr[th['name']] + " </td>"
                rs = rs + "</tr>"
        rs = rs + "</tbody></table>"   
        return rs        



registerType(bungeniremotefolder, PROJECTNAME)
# end of class bungeniremotefolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



