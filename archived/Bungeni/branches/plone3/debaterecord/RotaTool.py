# -*- coding: utf-8 -*-
#
# File: RotaTool.py
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

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Relations.field import RelationField
from Products.Bungeni.config import *

# additional imports from tagged value 'import'
from Products.OrderableReferenceField import OrderableReferenceField


from Products.CMFCore.utils import UniqueObject

    
##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import DisplayList

from Products.validation.config import validation
from Products.validation.validators.RangeValidator import RangeValidator
validation.register(RangeValidator('isPositiveNumber', 1, 600))
##/code-section module-header

schema = Schema((

    IntegerField(
        name='ReportingLeadTime',
        widget=IntegerField._properties['widget'](
            description="How many minutes before the take the reporters have to be in the Chamber/Committee Room",
            label="Reporting Lead Time",
            label_msgid='Bungeni_label_ReportingLeadTime',
            description_msgid='Bungeni_help_ReportingLeadTime',
            i18n_domain='Bungeni',
        ),
        required=1,
        validators=('isPositiveNumber',)
    ),

    IntegerField(
        name='TakeLength',
        widget=IntegerField._properties['widget'](
            description="The length of a take in minutes",
            label='Takelength',
            label_msgid='Bungeni_label_TakeLength',
            description_msgid='Bungeni_help_TakeLength',
            i18n_domain='Bungeni',
        ),
        required=1,
        validators=('isPositiveNumber',)
    ),

    IntegerField(
        name='ExtraTakes',
        widget=IntegerField._properties['widget'](
            description="The allowance of extra takes to cater for sitting overrunning",
            label='Extratakes',
            label_msgid='Bungeni_label_ExtraTakes',
            description_msgid='Bungeni_help_ExtraTakes',
            i18n_domain='Bungeni',
        ),
        required=1,
        validators=('isPositiveNumber',)
    ),

    OrderableReferenceField(
        name='AvailableReporters',
        vocabulary='getAvailableReportersVocab',
        widget=OrderableReferenceField._properties['widget'](
            label='Availablereporters',
            label_msgid='Bungeni_label_AvailableReporters',
            i18n_domain='Bungeni',
        ),
        allowed_types=['Staff',],
        relationship="rotatool_availablereporters",
        relation_implementation="basic"
    ),

    RelationField(
        name='RotaSubscribers',
        widget=ReferenceWidget(
            label='Rotasubscribers',
            label_msgid='Bungeni_label_RotaSubscribers',
            i18n_domain='Bungeni',
        ),
        relationship='rotatool_rotasubscribers',
        multiValued=1,
        vocabulary='getRotaSubscribersVocab',
        default_method='setRotaSubscribersDefault',
        allowed_types="['MemberOfParliament', 'Staff']"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

RotaTool_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class RotaTool(UniqueObject, BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IRotaTool)

    meta_type = 'RotaTool'
    _at_rename_after_creation = True

    schema = RotaTool_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # tool-constructors have no id argument, the id is fixed
    def __init__(self, id=None):
        BaseContent.__init__(self,'portal_rotatool')
        self.setTitle('')
        
        ##code-section constructor-footer #fill in your manual code here
        ##/code-section constructor-footer


    # tool should not appear in portal_catalog
    def at_post_edit_script(self):
        self.unindexObject()
        
        ##code-section post-edit-method-footer #fill in your manual code here
        ##/code-section post-edit-method-footer


    # Methods

    security.declarePublic('getAvailableReportersVocab')
    def getAvailableReportersVocab(self):
        """ Get the current parliament's team of reporters, and return
        the active memberships.
        """
        members = self.getReporters()
        return DisplayList([(m.UID(), m.Title()) for m in members])

    security.declarePublic('getRotaSubscribersVocab')
    def getRotaSubscribersVocab(self):
        """
        """
        members = self.getReporters() + self.getMPs()
        return DisplayList([(m.UID(), m.Title()) for m in members])

    security.declarePublic('getReporters')
    def getReporters(self):
        """
        """
        # TODO: this looks for all Reporters in all teams. If someone is
        # a Reporter in more than one team, this can return duplicates.
        # Is that a bug?
        catalog = getToolByName(self, 'portal_catalog')
        reporter_proxies = catalog.search(
                {'allowedRolesAndUsers': 'Reporter', 'review_state': 'active',
                    'portal_type': 'Team Membership'}
                )
        reporters = [p.getObject() for p in reporter_proxies]
        members = [r.getMember() for r in reporters]
        return members

    security.declarePublic('getMPs')
    def getMPs(self):
        """
        """
        catalog = getToolByName(self, 'portal_catalog')
        mp_proxies = catalog.search(
                {'allowedRolesAndUsers': 'MemberOfParliament',
                    'review_state': 'active',
                    'portal_type': 'Team Membership'}
                )
        mps = [p.getObject() for p in mp_proxies]
        members = [r.getMember() for r in mps]
        return members


registerType(RotaTool, PROJECTNAME)
# end of class RotaTool

##code-section module-footer #fill in your manual code here
##/code-section module-footer



