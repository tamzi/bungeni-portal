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
copied_fields['title'].default_method = "defaultTitle"
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

    security.declarePublic('publishRota')
    def publishRota(self, state_change, kw):
        """ Do everything that needs to be done when the Rota is
        published.
        """
        # Finalize RotaItems (make them non-editable).
        items = self.contentValues(
                    filter={'portal_type': 'RotaItem'})
        workflow_tool = getToolByName(self, 'portal_workflow')
        for item in items:
            workflow_tool.doActionFor(item, 'finalize',
                    comment='Finalize as part of Rota publication')

        self._createRotaDocument()
        self._notifySubscribers()

    security.declarePublic('retractRota')
    def retractRota(self, state_change, kw):
        """
        """
        # Retract RotaItems (make them editable again).
        items = self.contentValues(
                    filter={'portal_type': 'RotaItem'})
        workflow_tool = getToolByName(self, 'portal_workflow')
        for item in items:
            workflow_tool.doActionFor(item, 'retract',
                    comment='Retract as part of Rota retraction')

        self.manage_delObjects('rota-document')

    security.declarePublic('defaultTitle')
    def defaultTitle(self):
        """
        """
        parent = self.aq_parent
        while parent.Type() != 'Sitting':
            parent = parent.aq_parent
        return 'Rota for %s'%(parent.Title())

    security.declarePublic('reindexOnReorder')
    def reindexOnReorder(self, parent):
        """ Catalog ordering support """
        # Copied from PloneTool.reindexOnReorder
        # We're just indexing some more.
        mtool = getToolByName(self, 'portal_membership')
        if not mtool.checkPermission(permissions.ModifyPortalContent, parent):
            return
        cat = getToolByName(self, 'portal_catalog')
        cataloged_objs = cat(path = {'query':'/'.join(parent.getPhysicalPath()),
                                     'depth': 1})
        for brain in cataloged_objs:
            obj = brain.getObject()
            # Don't crash when the catalog has contains a stale entry
            if obj is not None:
                cat.reindexObject(obj,['getObjPositionInParent', 'Title'],)
            else:
                # Perhaps we should remove the bad entry as well?
                log('Object in catalog no longer exists, cannot reindex: %s.'%
                                    brain.getPath())
    security.declarePrivate('_createRotaDocument')
    def _createRotaDocument(self):
        """
        """
        items = self.contentValues(
                    filter={'portal_type': 'RotaItem'})
        paragraph = "%s: %s (for %s to %s)\n %s\n\n"
        title = "Rota for %s on %s"%(
            self.aq_parent.aq_parent.Title(),
            self.getRotaFrom().Date())
        paragraphs = ["%s\n%s\n\n"%(title, '='*len(title))]
        for item in items:
            paragraphs.append(paragraph%(
                item.getItemOrder()+1,
                item.getItemFromWithLead().TimeMinutes(),
                item.getItemFrom().TimeMinutes(),
                item.getItemTo().TimeMinutes(),
                item.getReporter().Title(),
                ))
        portal_types = getToolByName(self, 'portal_types')
        # Use constructContent to bypass allowed types constraint.
        did = portal_types.constructContent('Document', self,
                'rota-document',
                title=title,
                text=''.join(paragraphs))
        document = getattr(self, did)
        plone_utils = getToolByName(self, 'plone_utils')
        plone_utils.editMetadata(document, format='text/x-rst')

        # XXX
        self.REQUEST.RESPONSE.redirect(document.absolute_url())

    security.declarePrivate('_notifySubscribers')
    def _notifySubscribers(self):
        """ Send the summary rota document to all the subscribers
        """
        # TODO Consider making this more sophisticated: allow teams as
        # subscribers (mail to all team members); maybe use one of the
        # newsletter products to do the sending more reliably, with more
        # features ..
        rota_tool = getToolByName(self, 'portal_rotatool')
        properties_tool = getToolByName(self, 'portal_properties')
        subscribers = rota_tool.getRotaSubscribers()
        rota_document = getattr(self, 'rota-document')
        if not rota_document:
            return
        for s in subscribers:
            email = s.getEmail()
            if email:
                self.MailHost.send(rota_document.getRawText(), email,
                        properties_tool.email_from_address,
                        subject=rota_document.Title())
            else:
                log('notifySubscribers> %s has no email address'%s.Title())


registerType(RotaFolder, PROJECTNAME)
# end of class RotaFolder

##code-section module-footer #fill in your manual code here
def addedRotaFolder(obj, event):
    """ After the folder has been added, populate it with RotaItems
    based on the AvailableReporters.
    """
    if obj.isTemporary():
        #DBG log('addedRotaFolder> Not yet!')
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



