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
            label="About",
            description="Detailed description of this folder listing",
            label_msgid='bungeniremotecontent_label_body_text',
            description_msgid='bungeniremotecontent_help_body_text',
            i18n_domain='bungeniremotecontent',
        ),
        default_output_type='text/html',
        required=False,
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
    IntegerField(
        name='limit',
        default=20,
        widget=IntegerField._properties['widget'](
            description="maximum rows shown in the listing",
            label="Limit",
            label_msgid='bungeniremotecontent_label_limit',
            description_msgid='bungeniremotecontent_help_limit',
            i18n_domain='bungeniremotecontent',
        ),
        read_permission="Add portal content",
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
        request = self.REQUEST
        bungeni_tool = getToolByName(self, "portal_bungeniremotesettings")
        host_url = bungeni_tool.host_url
        if host_url[-1] !='/':
            host_url = host_url + '/'
        source_url =self.source_url
        if source_url[-1] != '/':
            source_url = source_url + '/'
        if source_url[0] == '/':
            source_url = source_url[1:]
        #get some info from the request
        sort_by = request.get('sort', '')
        sort_order = request.get('dir', 'asc')
        querystr = "?dir=" + sort_order
        start = request.get('start', '0')
        limit = request.get('limit', str(self.limit))
        if sort_by !='':
            querystr = querystr + '&sort=' + sort_by
        if limit !='':
            querystr = querystr + '&limit=' + limit
        querystr = querystr + '&start=' + start
        lurl = bungeni_tool.host_url + source_url + bungeni_tool.json_listing + querystr
        turl = bungeni_tool.host_url + source_url + bungeni_tool.json_headers
        lf = urllib.urlopen(lurl)
        results = simplejson.load(lf)
        tf = urllib.urlopen(turl)
        ths = simplejson.load(tf)
        if results.has_key("sort"):
            sort_by = results['sort']
        if results.has_key("dir"):
            sort_order = results['dir']
        if results.has_key("start"):
            start=results['start']
        if results.has_key("limit"):
            limit=results['limit']

        rs = '<table class="remote-table"> <thead> <tr>'
        for th in ths:
            css_class = ''
            collumn_sort_order = "asc"
            if th['name'] == sort_by:
                if sort_order == "desc":
                    css_class = "sorted_desc"
                else:
                    css_class = "sorted_asc"
                    collumn_sort_order = "desc"
            else:
                css_class = "sorted_unsorted"
            rs = rs + '<th class="' + css_class + '"> '
            lnk = '?dir=' + collumn_sort_order + '&sort=' + th['name'] + "&limit=" + limit +"&start=0"
            rs = rs + '<a href="' + lnk + '" >' + th['title'] + "</a> </th>"

        rs = rs + "</tr> </thead> <tbody>"
        if results.has_key("nodes"):
            for tr in results['nodes']:
                rs = rs + "<tr>"
                for th in ths:
                        rs = rs + "<td> " + str(tr[th['name']]) + " </td>"
                rs = rs + "</tr>"
        rs = rs + "</tbody></table>"
        return rs



registerType(bungeniremotefolder, PROJECTNAME)
# end of class bungeniremotefolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



