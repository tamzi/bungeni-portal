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
    url = interface.Attribute(
        """Hello, world!""")

    start_block = interface. Attribute(
        """Hello, world!""")

    start_xpath = interface.Attribute(
        """Hello, world!""")

    start_word = interface.Attribute(
        """Hello, world!""")

    start_char = interface.Attribute(
        """Hello, world!""")

    end_block = interface.Attribute(
        """Hello, world!""")

    end_xpath = interface.Attribute(
        """Hello, world!""")

    end_word = interface.Attribute(
        """Hello, world!""")

    end_char = interface.Attribute(
        """Hello, world!""")

    note = interface.Attribute(
        """Hello, world!""")

    edit_type = interface.Attribute(
        """Hello, world!""")

    quote = interface.Attribute(
        """Hello, world!""")

    quote_title = interface.Attribute(
        """Hello, world!""")

    quote_author = interface.Attribute(
        """Hello, world!""")

    quote_authorid = interface.Attribute(
        """Hello, world!""")

    link_title = interface.Attribute(
        """Hello, world!""")


class IMarginaliaTool(interface.Interface):
    def create_annotation(self, **kw):
        """Adds annotation to the global pool of marginalia content
        annotations."""
    
    




