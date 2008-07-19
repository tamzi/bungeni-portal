# -*- coding: utf-8 -*-
#
# File: AuditorTool.py
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

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.AuditTrail.config import *

# additional imports from tagged value 'import'
from LockingFileHandler import LockingFileHandler
from TransactionEndHandler import TransactionEndHandler


from Products.CMFCore.utils import UniqueObject

    
##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from zope.app.container.interfaces import IObjectModifiedEvent
from zope.app.container.interfaces import IObjectRemovedEvent

FORMAT = """------ %(asctime)s ------ %(levelname)s ------
%(message)s
"""

import logging
logger = logging.getLogger('AuditTrailLog')
logger.propagate = 0
filehandler = LockingFileHandler(LOG_PATH)
filehandler.setFormatter(logging.Formatter(FORMAT))
memoryhandler = TransactionEndHandler(target=filehandler)
logger.addHandler(memoryhandler)
logger.setLevel(logging.INFO)
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

AuditorTool_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class AuditorTool(UniqueObject, BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(UniqueObject,'__implements__',()),) + (getattr(BaseContent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'AuditorTool'

    meta_type = 'AuditorTool'
    portal_type = 'AuditorTool'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'AuditorTool.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "AuditorTool"
    typeDescMsgId = 'description_edit_auditortool'
    #toolicon = 'AuditorTool.gif'

    _at_rename_after_creation = True

    schema = AuditorTool_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # tool-constructors have no id argument, the id is fixed
    def __init__(self, id=None):
        BaseContent.__init__(self,'portal_auditortool')
        self.setTitle('AuditorTool')
        
        ##code-section constructor-footer #fill in your manual code here
        ##/code-section constructor-footer


    # tool should not appear in portal_catalog
    def at_post_edit_script(self):
        self.unindexObject()
        
        ##code-section post-edit-method-footer #fill in your manual code here
        ##/code-section post-edit-method-footer


    # Methods

    security.declarePublic('logEvent')
    def logEvent(self,ob,event):
        """
        """
        msg = ['uid: %s' % ob.UID(),
              'portal_type: %s' % ob.portal_type,
              ]

        if IAfterTransitionEvent.providedBy(event):
            if not event.transition:
                return # Ignore null transitions
            msg.append( "transition: %s" % event.transition.id )
        if IObjectRemovedEvent.providedBy(event):
            msg.append( 'removed: 1\nid: %s\n' % ob.getId() )
        else:
            marshaller = ob.Schema().getLayerImpl('marshall')
            msg.append( marshaller.marshall(ob)[2] )

        logger.info('\n'.join(msg))


registerType(AuditorTool, PROJECTNAME)
# end of class AuditorTool

##code-section module-footer #fill in your manual code here
def auditHandler(ob, event):
    """
    """
    auditor_tool = getToolByName(ob, 'portal_auditortool', None)
    if auditor_tool:
        auditor_tool.logEvent(ob, event)
##/code-section module-footer



