# ------------------------------------------------------------------------------
# Appy is a framework for building applications in the Python language.
# Copyright (C) 2007 Gaetan Delannay

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,USA.

# ------------------------------------------------------------------------------
import time
from appy.shared.utils import Traceback

# ------------------------------------------------------------------------------
class PodError(Exception):
    def dumpTraceback(buffer, tb):
        i = 0
        for tLine in tb.splitlines():
            i += 1
            if i > 3:
                buffer.write('<text:p>')
                buffer.dumpContent(tLine)
                buffer.write('</text:p>')
    dumpTraceback = staticmethod(dumpTraceback)
    def dump(buffer, message, withinElement=None):
        '''Dumps the error p_message in p_buffer.'''
        if withinElement:
            buffer.write('<%s>' % withinElement.OD)
            for subTag in withinElement.subTags:
                buffer.write('<%s>' % subTag)
        buffer.write('<office:annotation><dc:creator>POD</dc:creator>' \
                     '<dc:date>%s</dc:date><text:p>' % \
                     time.strftime('%Y-%m-%dT%H:%M:%S'))
        buffer.dumpContent(message)
        buffer.write('</text:p>')
        PodError.dumpTraceback(buffer, Traceback.get())
        buffer.write('</office:annotation>')
        if withinElement:
            subTags = withinElement.subTags[:]
            subTags.reverse()
            for subTag in subTags:
                buffer.write('</%s>' % subTag)
            buffer.write('</%s>' % withinElement.OD)
    dump = staticmethod(dump)
# ------------------------------------------------------------------------------
