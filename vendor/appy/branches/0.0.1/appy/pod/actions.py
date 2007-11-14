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
from appy.pod.elements import *
try:
    from appy.shared.aql import QueriableList
except ImportError:
    # Standalone POD does not have aql module
    QueriableList = list
from UserList import UserList

# ------------------------------------------------------------------------------
EVAL_ERROR = 'Error while evaluating expression "%s".'
WRONG_SEQ_TYPE = 'Expression "%s" does not represent a sequence.'
TABLE_NOT_ONE_CELL = "The table you wanted to populate with '%s' " \
                     "can\'t be dumped with the '-' option because it has " \
                     "more than one cell in it."

# ------------------------------------------------------------------------------
class BufferAction:
    '''Abstract class representing a action (=statement) that must be performed
    on the content of a buffer: if or for.'''
    def __init__(self, buffer, expr, elem, minus):
        self.buffer = buffer # The object of the action
        self.expr = expr # Python expression to evaluate
        self.elem = elem # The element within the buffer that is the object
        # of the action.
        self.minus = (minus != None) # If True, the main buffer element(s)
        # must not be dumped.
        self.result = self.buffer.getFileBuffer()
    def writeError(self, errorMessage):
        # Empty the buffer
        self.buffer.__init__({}, self.buffer.parent)
        PodError.dump(self.buffer, errorMessage, withinElement=self.elem)
        self.buffer.evaluate()
    def execute(self):
        # Check that if minus is set, we have an element which can accept it
        if self.minus and isinstance(self.elem, Table) and \
           (not self.elem.tableInfo.isOneCell()):
            self.writeError(TABLE_NOT_ONE_CELL % self.expr)
        else:
            exprResult = None
            errorOccurred = False
            try:
                exprResult = eval(self.expr, self.buffer.env.context)
            except:
                self.writeError(EVAL_ERROR % self.expr)
                errorOccurred = True
            if not errorOccurred:
                self.do(exprResult)
    def evaluateBuffer(self):
        self.buffer.evaluate(removeMainElems = self.minus)

class IfAction(BufferAction):
    '''Action that determines if we must include the content of the buffer in
    the result or not.'''
    def do(self, exprResult):
        if exprResult:
            self.evaluateBuffer()
        else:
            if self.buffer.isMainElement(Cell.OD):
                # Don't leave the current row with a wrong number of cells
                self.result.dumpElement(Cell.OD)

class ForAction(BufferAction):
    '''Actions that will include the content of the buffer as many times as
    specified by the action parameters.'''
    sequenceTypes = (list, tuple, basestring, QueriableList, UserList)
    def __init__(self, buffer, expr, elem, minus, iter):
        BufferAction.__init__(self, buffer, expr, elem, minus)
        self.iter = iter # Name of the iterator variable used in the each loop
    def do(self, exprResult):
        context = self.buffer.env.context
        # Check exprResult type
        wrongType = True
        for seqType in ForAction.sequenceTypes:
            if isinstance(exprResult, seqType):
                wrongType = False
                break
        if wrongType:
            self.writeError(WRONG_SEQ_TYPE % self.expr)
        else:
            # Remember variable hidden by iter if any
            hasHiddenVariable = False
            if context.has_key(self.iter):
                hiddenVariable = context[self.iter]
                hasHiddenVariable = True
            # In the case of cells, initialize some values
            isCell = False
            if isinstance(self.elem, Cell):
                isCell = True
                nbOfColumns = self.elem.tableInfo.nbOfColumns
                initialColIndex = self.elem.tableInfo.curColIndex
                currentColIndex = initialColIndex
                rowAttributes = self.elem.tableInfo.curRowAttrs
                # If exprResult is empty, dump an empty cell to avoid having the
                # wrong number of cells for the current row
                if not exprResult:
                    self.result.dumpElement(Cell.OD)
            # Enter the "for" loop
            for item in exprResult:
                context[self.iter] = item
                # Cell: add a new row if we are at the end of a row
                if isCell and (currentColIndex == nbOfColumns):
                    self.result.dumpEndElement(Row.OD)
                    self.result.dumpStartElement(Row.OD, rowAttributes)
                    currentColIndex = 0
                self.evaluateBuffer()
                # Cell: increment the current column index
                if isCell:
                    currentColIndex += 1
            # Cell: leave the last row with the correct number of cells
            if isCell and exprResult:
                wrongNbOfCells = (currentColIndex-1) - initialColIndex
                if wrongNbOfCells < 0: # Too few cells for last row
                    for i in range(abs(wrongNbOfCells)):
                        context[self.iter] = ''
                        self.buffer.evaluate(subElements=False)
                        # This way, the cell is dumped with the correct styles
                elif wrongNbOfCells > 0: # Too many cells for last row
                    # Finish current row
                    nbOfMissingCells = 0
                    if currentColIndex < nbOfColumns:
                        nbOfMissingCells = nbOfColumns - currentColIndex
                        context[self.iter] = ''
                        for i in range(nbOfMissingCells):
                            self.buffer.evaluate(subElements=False)
                    self.result.dumpEndElement(Row.OD)
                    # Create additional row with remaining cells
                    self.result.dumpStartElement(Row.OD, rowAttributes)
                    nbOfRemainingCells = wrongNbOfCells + nbOfMissingCells
                    nbOfMissingCellsLastLine = nbOfColumns - nbOfRemainingCells
                    context[self.iter] = ''
                    for i in range(nbOfMissingCellsLastLine):
                        self.buffer.evaluate(subElements=False)
            # Restore hidden variable if any
            if hasHiddenVariable:
                context[self.iter] = hiddenVariable
            else:
                if exprResult:
                    del context[self.iter]
# ------------------------------------------------------------------------------
