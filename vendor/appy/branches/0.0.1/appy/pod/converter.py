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
import sys, os, os.path, time, signal
from optparse import OptionParser

import uno
from com.sun.star.connection import NoConnectException
from com.sun.star.lang import IllegalArgumentException
from com.sun.star.beans import PropertyValue

# ------------------------------------------------------------------------------
class ConverterError(Exception): pass

# ConverterError-related messages ----------------------------------------------
DOC_NOT_FOUND = 'Document "%s" was not found.'
URL_NOT_FOUND = 'Doc URL "%s" is wrong. %s'
BAD_RESULT_TYPE = 'Bad result type "%s". Available types are %s.'
CANNOT_WRITE_RESULT = 'I cannot write result "%s". %s'
CONNECT_ERROR = 'Could not connect to OpenOffice on port %d. UNO ' \
                '(OpenOffice API) says: %s.'

# Some constants ---------------------------------------------------------------
DEFAULT_PORT = 2002

# ------------------------------------------------------------------------------
class Converter:
    '''Converts an ODT document into pdf, doc, txt or rtf.'''
    filters = {'doc': 'MS Word 97', # Could be 'MS Word 2003 XML'
               'pdf': 'writer_pdf_Export',
               'rtf': 'Rich Text Format',
               'txt': 'Text'}
    exeVariants = ('soffice.exe', 'soffice')
    pathReplacements = {'program files': 'progra~1',
                        'openoffice.org 1': 'openof~1',
                        'openoffice.org 2': 'openof~1',
                        }
    def __init__(self, docPath, resultType, port=DEFAULT_PORT):
        self.port = port
        self.docUrl = self.getDocUrl(docPath)
        self.resultFilter = self.getResultFilter(resultType)
        self.resultUrl = self.getResultUrl(resultType)
        self.ooContext = None
        self.oo = None # OpenOffice application object
        self.doc = None # OpenOffice loaded document
    def getDocUrl(self, docPath):
        if not os.path.exists(docPath) and not os.path.isfile(docPath):
            raise ConverterError(DOC_NOT_FOUND % docPath)
        docAbsPath = os.path.abspath(docPath)
        docUrl = 'file:///' + docAbsPath.replace('\\', '/')
        return docUrl
    def getResultFilter(self, resultType):
        if Converter.filters.has_key(resultType):
            res = Converter.filters[resultType]
        else:
            raise ConverterError(BAD_RESULT_TYPE % (resultType,
                                                    Converter.filters.keys()))
        return res
    def getResultUrl(self, resultType):
        res = '%s.%s' % (os.path.splitext(self.docUrl)[0], resultType)
        fileName = res[8:] 
        try:
            f = open(fileName, 'w')
            f.write('Hello')
            f.close()
            os.remove(fileName)
            return res
        except OSError, oe:
            raise ConverterError(CANNOT_WRITE_RESULT % (res, oe))
    def connect(self):
        '''Connects to OpenOffice'''
        try:
            # Get the uno component context from the PyUNO runtime
            localContext = uno.getComponentContext()
            # Create the UnoUrlResolver
            resolver = localContext.ServiceManager.createInstanceWithContext(
                "com.sun.star.bridge.UnoUrlResolver", localContext)
            # Connect to the running office
            self.ooContext = resolver.resolve(
                'uno:socket,host=localhost,port=%d;urp;StarOffice.' \
                'ComponentContext' % self.port)
            # Is seems that we can't define a timeout for this method.
            # I need it because, for example, when a web server already listens
            # to the given port (thus, not a OpenOffice instance), this method
            # blocks.
            smgr = self.ooContext.ServiceManager
            # Get the central desktop object
            self.oo = smgr.createInstanceWithContext(
                'com.sun.star.frame.Desktop', self.ooContext)
        except NoConnectException, nce:
            raise ConverterError(CONNECT_ERROR % (self.port, nce))
    def disconnect(self):
        self.doc.close(True)
        # Do a nasty thing before exiting the python process. In case the
        # last call is a oneway call (e.g. see idl-spec of insertString),
        # it must be forced out of the remote-bridge caches before python
        # exits the process. Otherwise, the oneway call may or may not reach
        # the target object.
        # I do this here by calling a cheap synchronous call (getPropertyValue).
        self.ooContext.ServiceManager
    def loadDocument(self):
        try:
            # Load the document to convert in a new hidden frame
            prop = PropertyValue()
            prop.Name = 'Hidden'
            prop.Value = True
            self.doc = self.oo.loadComponentFromURL(self.docUrl, "_blank", 0,
                                                    (prop,))
        except IllegalArgumentException, iae:
            raise ConverterError(URL_NOT_FOUND % (self.docUrl, iae))
    def convertDocument(self):
        prop = PropertyValue()
        prop.Name = 'FilterName'
        prop.Value = self.resultFilter
        self.doc.storeToURL(self.resultUrl, (prop,))
    def run(self):
        self.connect()
        self.loadDocument()
        self.convertDocument()
        self.disconnect()

# ConverterScript-related messages ---------------------------------------------
WRONG_NB_OF_ARGS = 'Wrong number of arguments.'
ERROR_CODE = 1

# Class representing the command-line program ----------------------------------
class ConverterScript:
    usage = 'usage: python converter.py fileToConvert outputType [options]\n' \
            '   where fileToConvert is the absolute or relative pathname of\n' \
            '         the ODT file you want to convert;\n'\
            '   and   outputType is the output format, that must be one of\n' \
            '         %s.\n' \
            ' "python" should be a UNO-enabled Python interpreter (ie the one\n' \
            ' which is included in the OpenOffice.org distribution).' % \
            str(Converter.filters.keys())
    def run(self):
        optParser = OptionParser(usage=ConverterScript.usage)
        optParser.add_option("-p", "--port", dest="port",
                             help="The port on which OpenOffice runs " \
                             "Default is %d." % DEFAULT_PORT, 
                             default=DEFAULT_PORT, metavar="PORT", type='int')
        (options, args) = optParser.parse_args()
        if len(args) != 2:
            sys.stderr.write(WRONG_NB_OF_ARGS)
            sys.stderr.write('\n')
            optParser.print_help()
            sys.exit(ERROR_CODE)
        converter = Converter(args[0], args[1], options.port)
        try:
            converter.run()
        except ConverterError, ce:
            sys.stderr.write(str(ce))
            sys.stderr.write('\n')
            optParser.print_help()
            sys.exit(ERROR_CODE)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    ConverterScript().run()
# ------------------------------------------------------------------------------
