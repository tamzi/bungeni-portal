# -*- coding: utf-8 -*-
#
# File: BungeniMember.py
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
from zope import interface
from zope.interface import implements
import interfaces
from Products.Bungeni.interfaces.IBungeniMember import IBungeniMember
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
##/code-section module-header

schema = Schema((

    StringField(
        name='salutation',
        widget=StringWidget(
            label="Title or salutation",
            label_msgid='Bungeni_label_salutation',
            i18n_domain='Bungeni',
        ),
        user_property=True,
        regfield=1
    ),

    StringField(
        name='firstname',
        widget=StringWidget(
            label="First name",
            label_msgid='Bungeni_label_firstname',
            i18n_domain='Bungeni',
        ),
        user_property=True,
        regfield=1
    ),

    StringField(
        name='middlename',
        widget=StringWidget(
            label='Middlename',
            label_msgid='Bungeni_label_middlename',
            i18n_domain='Bungeni',
        )
    ),

    StringField(
        name='surname',
        widget=StringWidget(
            label="Surname",
            label_msgid='Bungeni_label_surname',
            i18n_domain='Bungeni',
        ),
        user_property=True,
        regfield=1
    ),

    StringField(
        name='maidenname',
        widget=StringWidget(
            label='Maidenname',
            label_msgid='Bungeni_label_maidenname',
            i18n_domain='Bungeni',
        )
    ),

    ComputedField(
        name='fullname',
        widget=ComputedField._properties['widget'](
            label="Full name",
            label_msgid='Bungeni_label_fullname',
            i18n_domain='Bungeni',
        )
    ),

    StringField(
        name='placeOfBirth',
        widget=StringWidget(
            label='Placeofbirth',
            label_msgid='Bungeni_label_placeOfBirth',
            i18n_domain='Bungeni',
        )
    ),

    DateTimeField(
        name='dateOfBirth',
        widget=CalendarWidget(
            label='Dateofbirth',
            label_msgid='Bungeni_label_dateOfBirth',
            i18n_domain='Bungeni',
        )
    ),

    DateTimeField(
        name='dateOfDeath',
        widget=CalendarWidget(
            label='Dateofdeath',
            label_msgid='Bungeni_label_dateOfDeath',
            i18n_domain='Bungeni',
        )
    ),

    StringField(
        name='gender',
        widget=SelectionWidget(
            label='Gender',
            label_msgid='Bungeni_label_gender',
            i18n_domain='Bungeni',
        ),
        vocabulary=['M','F']
    ),

    StringField(
        name='nationalIdNumber',
        widget=StringWidget(
            label='Nationalidnumber',
            label_msgid='Bungeni_label_nationalIdNumber',
            i18n_domain='Bungeni',
        )
    ),

    BooleanField(
        name='ext_editor',
        widget=BooleanField._properties['widget'](
            label='Ext_editor',
            label_msgid='Bungeni_label_ext_editor',
            i18n_domain='Bungeni',
        )
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

BungeniMember_schema = schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class BungeniMember(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IBungeniMember, IBungeniMember)

    _at_rename_after_creation = True

    schema = BungeniMember_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('isAuto')
    def isAuto(self):
        """ Are we in an auto-approved workflow?
        """
        # XXX: This is pretty hacky (peering at the workflow name), but
        # we need some way of knowing whether our workflow is auto or
        # approval.
        wft = getToolByName(self, 'portal_workflow')
        workflow_names = wft.getChainForPortalType(self.portal_type)
        auto = False
        for workflow_name in workflow_names:
            auto = 'auto' in workflow_name.lower()
            if auto: break
        return auto

    # Methods from Interface IBungeniMember

    security.declarePublic('setFullname')
    def setFullname(self, name=None):
        """ Stub for BaseMember.register
        """
        pass

    security.declarePublic('getFullname')
    def getFullname(self):
        """
        """
        # XXX unicode names break sending the email
        unicode_name = ' '.join([n for n in
                [self.getSalutation(), self.getFirstname(), self.getMiddlename(), self.getSurname()]
                if n])
        return str(unicode_name)

# end of class BungeniMember

##code-section module-footer #fill in your manual code here
##/code-section module-footer



