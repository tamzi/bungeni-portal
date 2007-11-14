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
import os, os.path, sys

from appy.shared.utils import FolderDeleter
from appy.pod.renderer import Renderer

# Tests definitions ------------------------------------------------------------
class Person:
    def __init__(self, name):
        self.name = name
        self.lastName = '%s last name' % name
        self.firstName = '%s first name' % name
        self.address = '%s address' % name

class Group:
    def __init__(self, name):
        self.name = name
        if name == 'group1':
            self.persons = [Person('P1'), Person('P2'), Person('P3')]
        elif name == 'group2':
            self.persons = [Person('RA'), Person('RB')]
        else:
            self.persons = []

tests = {'NoPython': {},
         'OnlyExpressions': {'expr1': 'hello', 'i1': 45, 'f1': 78.05},
         'SimpleIfIsTrue': {'c1': True},
         'SimpleIfIsFalse': {'c1': False},
         'SimpleForEmptyList': {'list1': []},
         'SimpleForFilledList': {'list1': ['Hello', 'World', 45, True]},
         'SimpleForRow': {'persons': [Person('Mr 1'), Person('Ms One'),
                                      Person('Misss two')]},
         'IfAndFors1': {'groups': [Group('group1'), Group('group2'),
                                   Group('toto')]},
         'ForCellCorrectNumber': {'persons': [Person('P1'), Person('P2'),
                                              Person('P3'), Person('P4')]},
         'ForCellNotEnough': {'persons': [Person('P1'), Person('P2'),
                                          Person('P3')]},
         'ForCellTooMuch1': {'persons': [Person('P1'), Person('P2')]},
         'ForCellTooMuch2': {'persons': [Person('P1'), Person('P2'),
                                         Person('P3')]},
         'ForCellTooMuch3': {'persons': [Person('P1'), Person('P2')]},
         'ForCellTooMuch4': {'persons': [Person('P1'), Person('P2'),
                                         Person('P3')]},
         'ForCellOnlyOne': {'persons': [Person('P1'), Person('P2'),
                                        Person('P3'), Person('P4'),
                                        Person('P5'), Person('P6'),
                                        Person('P7'), Person('P8'),
                                        ]},
         'ForTable': {'persons': [Person('P1'), Person('P2'),
                                  Person('P3'), Person('P4'),
                                  Person('P5'), Person('P6'),
                                  Person('P7'), Person('P8'),
                                  ]},
         'ForTableMinus': {'persons': [Person('P1'), Person('P2'),
                                       Person('P3'), Person('P4'),
                                       Person('P5'), Person('P6'),
                                       Person('P7'), Person('P8'),
                                       ]},
         'ForTableMinus2': {'persons': [Person('P1'), Person('P2')]},
         'WithAnImage': {},
         'ErrorExpression': {},
         'ErrorIf': {},
         'ErrorForRuntime': {},
         'ErrorForParsetime': {},
         'ForTableMinusError': {'persons': [Person('P1'), Person('P2')]},
         'ForTableMinusError2': {'persons': [Person('P1'), Person('P2')]},
         'SimpleMinusError': {'c1': True},
         'SimpleTest': {'IWillTellYouWhatInAMoment' : 'return',
                        'beingPaidForIt': True },
         }

# ------------------------------------------------------------------------------
class PodTester:
    def __init__(self):
        if len(sys.argv) != 2:
            self.printUsage()
        self.test = os.path.splitext(sys.argv[1])[0]
        self.context = tests[self.test]
    def printUsage(self):
        print 'In order to run a test, go to appy/pod/test and run the ' \
              'following command:'
        print 'python tester.py <odtFileName>'
        print '  where <odtFileName> is the name of an ODT file in this folder.'
        print 'The tester will generate "result.odt" in the current folder.'
        sys.exit(0)
    def cleanPreviousResult(self):
        if os.path.exists('result.odt'):
            os.remove('result.odt')
        if os.path.exists('result.odt.temp'):
            FolderDeleter.delete('result.odt.temp')
    def run(self):
        self.cleanPreviousResult()
        print 'Rendering %s.odt... ' % self.test,
        Renderer('%s.odt' % self.test, self.context, 'result.odt').run()
        print 'done.'

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    PodTester().run()
# ------------------------------------------------------------------------------
