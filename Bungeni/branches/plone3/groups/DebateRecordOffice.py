# -*- coding: utf-8 -*-
#
# File: DebateRecordOffice.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 2.0-beta5
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Jean Jordaan <jean.jordaan@gmail.com>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.Bungeni.groups.Office import Office
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Relations.field import RelationField
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from Products.TeamSpace.permissions import *
##/code-section module-header

schema = Schema((

    RelationField(
        name='ChiefEditor',
        vocabulary='getMembershipVocab',
        widget=ReferenceWidget(
            label='Chiefeditor',
            label_msgid='Bungeni_label_ChiefEditor',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='debaterecordoffice_chiefeditor'
    ),

    RelationField(
        name='DeputyChiefEditor',
        vocabulary='getMembershipVocab',
        widget=ReferenceWidget(
            label='Deputychiefeditor',
            label_msgid='Bungeni_label_DeputyChiefEditor',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='debaterecordoffice_deputychiefeditor'
    ),

    RelationField(
        name='Editors',
        vocabulary='getMembershipVocab',
        widget=ReferenceWidget(
            label='Editors',
            label_msgid='Bungeni_label_Editors',
            i18n_domain='Bungeni',
        ),
        multiValued=1,
        relationship='debaterecordoffice_editors'
    ),

    RelationField(
        name='Reporters',
        vocabulary='getMembershipVocab',
        widget=ReferenceWidget(
            label='Reporters',
            label_msgid='Bungeni_label_Reporters',
            i18n_domain='Bungeni',
        ),
        multiValued=1,
        relationship='debaterecordoffice_reporters'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

DebateRecordOffice_schema = BaseSchema.copy() + \
    getattr(Office, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class DebateRecordOffice(BrowserDefaultMixin, Office):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IDebateRecordOffice)

    meta_type = 'DebateRecordOffice'
    _at_rename_after_creation = True

    schema = DebateRecordOffice_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('setChiefEditor')
    def setChiefEditor(self,value,**kw):
        """
        """
        # Team:
        if value:
            member_roles = self._get_member_roles_from_UIDs(
                    value, ['ChiefEditor'])
            self.manage_updateRoles(member_roles)
        # Field:
        field = self.Schema()['ChiefEditor']
        return field.set(self, value, **kw)

    security.declarePublic('setDeputyChiefEditor')
    def setDeputyChiefEditor(self,value,**kw):
        """
        """
        # Team:
        if value:
            member_roles = self._get_member_roles_from_UIDs(
                    value, ['DeputyChiefEditor'])
            self.manage_updateRoles(member_roles)
        # Field:
        field = self.Schema()['DeputyChiefEditor']
        return field.set(self, value, **kw)

    security.declarePublic('setEditors')
    def setEditors(self,value,**kw):
        """
        """
        # Team:
        if value:
            member_roles = self._get_member_roles_from_UIDs(
                    value, ['Editor'])
            self.manage_updateRoles(member_roles)
        # Field:
        field = self.Schema()['Editors']
        return field.set(self, value, **kw)

    security.declarePublic('setReporters')
    def setReporters(self,value,**kw):
        """
        """
        # Team:
        if value:
            member_roles = self._get_member_roles_from_UIDs(
                    value, ['Reporter'])
            self.manage_updateRoles(member_roles)
        # Field:
        field = self.Schema()['Reporters']
        return field.set(self, value, **kw)

    security.declareProtected(ManageTeam, 'manage_updateRoles')
    def manage_updateRoles(self,member_roles,REQUEST=None):
        """
        """
        constrained_roles = {
                'ChiefEditor': 1,
                'DeputyEditor': 1,
                }
        self._constrainMembershipRoles(constrained_roles, member_roles)
        # Delegate to super
        Office.manage_updateRoles(self,member_roles,REQUEST=None)


registerType(DebateRecordOffice, PROJECTNAME)
# end of class DebateRecordOffice

##code-section module-footer #fill in your manual code here
##/code-section module-footer



