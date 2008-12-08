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
import urllib, simplejson, feedparser
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
        required=True,
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

    security.declarePublic('getRemoteContent')
    def getRemoteContent(self):
        """
        gets the data from a remote site (as a rss or atom feed)
        and returns it as html
        """
        bungeni_tool = getToolByName(self, "portal_bungeniremotesettings")
        h_url = bungeni_tool.host_url
        s_url = self.source_url
        ac = bungeni_tool.atom_content
        sp = self.REQUEST.traverse_subpath[0]
        url = h_url + s_url + '/' + sp + '/' + ac
        results = feedparser.parse(url)
        if results['status'] != 200:
            print results
            entries = results['entries']
            entries.append ({'title' : 'error: ' + str(results['status']), 'content': [{'value':'Error retriving data'}]})
            return entries
        return results['entries']

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
        length = '1'
        if results.has_key("sort"):
            sort_by = results['sort']
        if results.has_key("dir"):
            sort_order = results['dir']
        if results.has_key("start"):
            start=results['start']
        if results.has_key("limit"):
            limit=results['limit']
        if results.has_key("length"):
            length = results['length']
        rs = '<table class="remote-table" id="bungeni-remote-listing"> <thead> <tr>'
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
            i = 0
            for tr in results['nodes']:
                i = i + 1
                if i % 2 == 0:
                    css_class = "even"
                else:
                    css_class = "odd"
                rs = rs + '<tr class="' + css_class+ '" >'
                for th in ths:
                        rs = rs + "<td> "
                        if tr[th['name']] is not None:
                            rs = rs + '<a href="bungeniremotepage_view/' + tr['object_id'] + '">'
                            rs = rs + str(tr[th['name']])
                            rs = rs + '</a>'
                        rs = rs +  " </td>"
                rs = rs + "</tr>"
        rs = rs + "</tbody></table>"
        pages = int(length) / int(limit)
        currpage = int(start) 
        pl = range(0,int(length), int(limit))
        #rs = rs + str(pl)
        i = 0
        prevpage = (((int(start) ) / int(limit)) -1) * int(limit)
        nextpage = (((int(start)) / int(limit)) + 1) * int(limit)
        if sort_by is None:
            sort_by = ''
        rs = rs + '<table id="remote-listing-pager"><tr>'
        if prevpage >= 0:
            lnk = '?dir=' + sort_order + '&sort=' + sort_by + "&limit=" + limit +"&start=" + str(prevpage) 
            rs = rs + '<td class="next-remote-page"> <a href="' + lnk + '" > &lt;&lt; </a> </td>'
        for p in pl:
            i = i + 1
            if i < len(pl):
                if p <= currpage < pl[i]:
                    css_class = "this-remote-page"
                else:
                    css_class =''
            else:
                if p <= currpage:
                    css_class = "this-remote-page"
                else:
                    css_class =''    
                    
            lnk = '?dir=' + sort_order + '&sort=' + sort_by + "&limit=" + limit +"&start=" + str(p)        
            rs = rs + '<td class="' + css_class + '"> <a href="' + lnk + '" >' + str(i) + '</a> </td>'
        if nextpage <= int(length):    
            lnk = '?dir=' + sort_order + '&sort=' + sort_by + "&limit=" + limit +"&start=" + str(nextpage) 
            rs = rs + '<td class="next-remote-page"> <a href="' + lnk + '" > &gt;&gt; </a> </td>'    
        rs = rs + '</tr></table>'    
        return rs


registerType(bungeniremotefolder, PROJECTNAME)
# end of class bungeniremotefolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



