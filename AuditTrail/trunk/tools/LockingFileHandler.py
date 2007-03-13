# -*- coding: utf-8 -*-
#
# File: LockingFileHandler.py
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
# Locking code from
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/65203
import os
import fcntl

def lock(file, flags):
    fcntl.flock(file.fileno(), flags)

def unlock(file):
    fcntl.flock(file.fileno(), fcntl.LOCK_UN)
##/code-section module-header

import logging


class LockingFileHandler(logging.FileHandler):
    """
    """

    ##code-section class-header_LockingFileHandler #fill in your manual code here
    ##/code-section class-header_LockingFileHandler

    def emit(self, record):
        """ Make sure no one reads a halfwritten record ..
        """
        lock(self.stream, fcntl.LOCK_EX)
        logging.FileHandler.emit(self, record)
        self.flush()
        unlock(self.stream)


##code-section module-footer #fill in your manual code here
##/code-section module-footer


