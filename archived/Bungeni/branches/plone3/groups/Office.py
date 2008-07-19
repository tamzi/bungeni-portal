# -*- coding: utf-8 -*-
#
# File: Office.py
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
from Products.Bungeni.groups.BungeniTeam import BungeniTeam
from Products.Bungeni.groups.BungeniTeam import BungeniTeam
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Relations.field import RelationField
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
from Products.TeamSpace.permissions import *
##/code-section module-header

schema = Schema((

    RelationField(
        name='Chairperson',
        vocabulary='getMembershipVocab',
        widget=ReferenceWidget(
            label='Chairperson',
            label_msgid='Bungeni_label_Chairperson',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='office_chairperson'
    ),

    RelationField(
        name='DeputyChairperson',
        vocabulary='getMembershipVocab',
        widget=ReferenceWidget(
            label='Deputychairperson',
            label_msgid='Bungeni_label_DeputyChairperson',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='office_deputychairperson'
    ),

    RelationField(
        name='Secretary',
        vocabulary='getMembershipVocab',
        widget=ReferenceWidget(
            label='Secretary',
            label_msgid='Bungeni_label_Secretary',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='office_secretary'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Office_schema = BaseSchema.copy() + \
    getattr(BungeniTeam, 'schema', Schema(())).copy() + \
    getattr(BungeniTeam, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Office(BungeniTeam, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IOffice)

    meta_type = 'Office'
    _at_rename_after_creation = True

    schema = Office_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('setChairperson')
    def setChairperson(self,value,**kw):
        """
        """
        # Team:
        if value:
            member_roles = self._get_member_roles_from_UIDs(
                    value, ['Chairperson'])
            self.manage_updateRoles(member_roles)
        # Field:
        field = self.Schema()['Chairperson']
        return field.set(self, value, **kw)

    security.declarePublic('setDeputyChairperson')
    def setDeputyChairperson(self,value,**kw):
        """
        """
        # Team:
        if value:
            member_roles = self._get_member_roles_from_UIDs(
                    value, ['DeputyChairperson'])
            uid = value[0]
            self.manage_updateRoles(member_roles)
        # Field:
        field = self.Schema()['DeputyChairperson']
        return field.set(self, value, **kw)

    security.declarePublic('setSecretary')
    def setSecretary(self,value,**kw):
        """
        """
        # Team:
        if value:
            member_roles = self._get_member_roles_from_UIDs(
                    value, ['Secretary'])
            self.manage_updateRoles(member_roles)
        # Field:
        field = self.Schema()['Secretary']
        return field.set(self, value, **kw)

    security.declareProtected(ManageTeam, 'manage_updateRoles')
    def manage_updateRoles(self,member_roles,REQUEST=None):
        """ Constrain some roles
        """
        constrained_roles = {
                'Chairperson': 1,
                'DeputyChairperson': 1, # TODO: verify
                'Secretary': 1,
                }
        self._constrainMembershipRoles(constrained_roles, member_roles)
        # Delegate to super
        BungeniTeam.manage_updateRoles(self,member_roles,REQUEST=None)


registerType(Office, PROJECTNAME)
# end of class Office

##code-section module-footer #fill in your manual code here
##/code-section module-footer



