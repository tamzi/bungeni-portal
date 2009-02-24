#
# File: interfaces.py
#
# Copyright (c) 2009 by Millie Ngoka
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

from zope import interface

class IAnnotation(interface.Interface):
    start_xrange = interface.Attribute(
        """Hello, world!""")
    
    block_range = interface.Attribute(
        """Hello, world!""")
    
    xpath_range = interface.Attribute(
        """Hello, world!""")
    
    note = interface.Attribute(
        """Hello, world!""")
    
    access = interface.Attribute(
        """Hello, world!""") 

class IMarginaliaTool(interface.Interface):
    def create_annotation(self, **kw):
        """Adds annotation to the global pool of marginalia content
        annotations."""
    
    




