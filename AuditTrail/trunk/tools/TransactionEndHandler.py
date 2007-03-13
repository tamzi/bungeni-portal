# -*- coding: utf-8 -*-
#
# File: TransactionEndHandler.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 1.5.1-svn
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

##code-section module-header #fill in your manual code here
import Products.AuditTrail.patches
##/code-section module-header

import logging, transaction
from logging.handlers import BufferingHandler
from transaction.interfaces import ISynchronizer
import zope

class TransactionEndHandler(logging.handlers.MemoryHandler):
    """ MacYET suggested implementing IDataManager instead, and doing
    the work in 'commit'. I don't have time for that now, and this seems
    to work, so TODO.
    """
    # zope3 interfaces
    zope.interface.implements(ISynchronizer)

    ##code-section class-header_TransactionEndHandler #fill in your manual code here
    ##/code-section class-header_TransactionEndHandler


    def __init__(self, capacity=1000000, flushLevel=logging.ERROR, target=None):
        BufferingHandler.__init__(self, capacity)
        self.target = target
        logger = logging.getLogger('AuditTrail')
        logger.info('AuditTrail.TransactionEndHandler> Registering with TM')
        transaction.manager.registerGlobalSynch(self)

    def beforeCompletion(self, transaction):
        logger = logging.getLogger('AuditTrail')
        logger.info('AuditTrail.TransactionEndHandler.beforeCompletion> Flushing')
        self.flush()

    def afterCompletion(self, transaction):
        pass

    def newTransaction(self, transaction):
        pass

    def shouldFlush(self, record):
        """ We're flushed explicitly on transaction boundary.
        """
        return False


##code-section module-footer #fill in your manual code here
##/code-section module-footer


