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
from appy.pod import PodError

# ------------------------------------------------------------------------------
class PodElement:
    OD_TO_POD = {'text:p': 'Text', 'text:h': 'Title', 'text:section': 'Section',
                 'table:table': 'Table', 'table:table-row': 'Row',
                 'table:table-cell': 'Cell', None: 'Expression'}
    POD_ELEMS = ('text', 'title', 'section', 'table', 'row', 'cell')
    MINUS_ELEMS = ('section', 'table') # Elements for which the '-' operator can
    # be applied
    def create(elem):
        '''Used to create any POD elem that has a equivalent OD element. Not
        for creating expressions, for example.'''
        return eval(PodElement.OD_TO_POD[elem])()
    create = staticmethod(create)

class Text(PodElement):
    OD = 'text:p'
    subTags = [] # When generating an error we may need to surround the error
    # with a given tag and subtags

class Title(PodElement):
    OD = 'text:h'
    subTags = []

class Section(PodElement):
    OD = 'text:section'
    subtags = [Text.OD]
    DEEPEST_TO_REMOVE = OD # When we must remove the Section element from a
    # buffer, the deepest element to remove is the Section element itself

class Cell(PodElement):
    OD = 'table:table-cell'
    subTags = [Text.OD]
    def __init__(self):
        self.tableInfo = None # ~OdTable~

class Row(PodElement):
    OD = 'table:table-row'
    subTags = [Cell.OD, Text.OD]

class Table(PodElement):
    OD = 'table:table'
    subTags = [Row.OD, Cell.OD, Text.OD]
    DEEPEST_TO_REMOVE = Cell.OD # When we must remove the Table element from a
    # buffer, the deepest element to remove is the Cell (it can only be done for
    # one-row, one-cell tables
    def __init__(self):
        self.tableInfo = None # ~OdTable~

class Expression(PodElement):
    OD = None
    def __init__(self, pyExpr):
        self.expr = pyExpr
    def evaluate(self, context):
        res = None
        res = eval(self.expr, context)
        if res == None:
            res = ''
        elif isinstance(res, str):
            res = unicode(res.decode('utf-8'))
        elif not isinstance(res, unicode):
            res = unicode(res)
        return res
# ------------------------------------------------------------------------------