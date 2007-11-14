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
import zipfile, shutil, xml.sax, os, os.path
from xml.sax.handler import ContentHandler

from UserDict import UserDict

import appy
from appy.pod import PodError
from appy.pod.buffers import FileBuffer, MemoryBuffer
from appy.pod.elements import *
from appy.shared.utils import FolderDeleter

# ------------------------------------------------------------------------------
BAD_CONTEXT = 'Context must be either a dict, a UserDict or an instance.'
RESULT_FILE_EXISTS = 'Result file "%s" exists.'
CANT_WRITE_RESULT = 'I cannot write result file "%s". %s'
TEMP_FOLDER_EXISTS = 'I need to use a temp folder "%s" but this folder ' \
                     'already exists.'
CANT_WRITE_TEMP_FOLDER = 'I cannot create temp folder "%s". %s'
NO_PY_PATH = 'Extension of result file is "%s". In order to perform ' \
             'conversion from ODT to this format we need to call OpenOffice. ' \
             'But the Python interpreter which runs the current script does ' \
             'not knows about UNO, the library that allows to connect to ' \
             'OpenOffice in server mode. If you can\'t install UNO in this ' \
             'Python interpreter, you can specify, in parameter ' \
             '"pythonWithUnoPath", the path to a UNO-enabled Python ' \
             'interpreter. One such interpreter may be found in ' \
             '<open_office_path>/program.'
NO_PYTHON = 'A python interpreter was not found in "%s". Please make sure ' \
            'you specified the right folder.'
BLANKS_IN_PATH = 'Blanks were found in path "%s". Please use the DOS-names ' \
                 '(ie, "progra~1" instead of "Program files" or "docume~1" ' \
                 'instead of "Documents and settings".'
BAD_RESULT_TYPE = 'Please specify an extension for your result file "%s".'
CONVERT_ERROR = 'An error occurred during the conversion. %s'
BAD_OO_PORT = 'Bad OpenOffice port "%s". Make sure it is an integer.'

# ------------------------------------------------------------------------------
class OdTable:
    '''Informations about the currently parsed Open Document (Od)table.'''
    def __init__(self):
        self.nbOfColumns = 0
        self.nbOfRows = 0
        self.curColIndex = None
        self.curRowAttrs = None
    def isOneCell(self):
        return (self.nbOfColumns == 1) and (self.nbOfRows == 1)

class Environment:
    '''Contains all elements representing the current parser state during
    parsing.'''
    # Elements we must ignore (they will not be included in the result
    ignorableElements = ('text:tracked-changes', 'text:change')
    # Elements that may be impacted by POD statements
    impactableElements = (Text.OD, Title.OD, Table.OD, Row.OD, Cell.OD,
                          Section.OD)
    # Possibles modes
    # ADD_IN_BUFFER: when encountering an impactable element, we must
    #                continue to dump it in the current buffer
    ADD_IN_BUFFER = 0
    # ADD_IN_SUBBUFFER: when encountering an impactable element, we must
    #                   create a new subbuffer and dump it in it.
    ADD_IN_SUBBUFFER = 1
    # Possible states
    IGNORING = 0 # We are ignoring what we are currently reading
    READING_CONTENT = 1 # We are reading "normal" content
    READING_STATEMENT = 2
    # We are reading a POD statement (for, if...), which is located within a
    # office:annotation element
    READING_EXPRESSION = 3
    # We are reading a POD expression, which is located between
    # a text:change-start and a text:change-end elements
    def __init__(self, context):
        # XML element currently parsed
        self.currentElement = None
        # Buffer where we must dump the content we are currently reading
        self.currentBuffer = None
        # XML element content we are currently reading
        self.currentContent = ''
        # Current mode
        self.mode = Environment.ADD_IN_SUBBUFFER
        # Current state
        self.state = Environment.READING_CONTENT
        # Stack of currently visited tables
        self.tableStack = []
        self.tableIndex = -1
        # Evaluation context
        self.context = context
        # For the currently read expression, is there style-related information
        # associated with it?
        self.exprHasStyle = False
    def getTable(self):
        '''Gets the currently parsed table.'''
        res = None
        if self.tableIndex != -1:
            res = self.tableStack[self.tableIndex]
        return res
    def onStartElement(self, elem, attrs):
        self.currentElement = elem
        if elem == Table.OD:
            self.tableStack.append(OdTable())
            self.tableIndex += 1
        elif elem == Row.OD:
            self.getTable().nbOfRows += 1
            self.getTable().curColIndex = -1
            self.getTable().curRowAttrs = attrs
        elif elem == Cell.OD:
            self.getTable().curColIndex += 1
        elif elem == 'table:table-column':
            if attrs.has_key('table:number-columns-repeated'):
                self.getTable().nbOfColumns += int(
                    attrs['table:number-columns-repeated'])
            else:
                self.getTable().nbOfColumns += 1
    def onEndElement(self, elem):
        if elem == Table.OD:
            self.tableStack.pop()
            self.tableIndex -= 1
    def addSubBuffer(self):
        subBuffer = self.currentBuffer.addSubBuffer()
        self.currentBuffer = subBuffer
        self.mode = self.ADD_IN_BUFFER

# ------------------------------------------------------------------------------
class SaxHandler(ContentHandler):
    def __init__(self, renderer, env):
        ContentHandler.__init__(self)
        self.locator = None
        self.environment = env
        self.renderer = renderer
    def setDocumentLocator(self, locator):
        self.locator = locator
    def endDocument(self):
        curBuf = self.environment.currentBuffer
        self.renderer.finalize()
    def startElement(self, elem, attrs):
        env = self.environment
        env.onStartElement(elem, attrs)
        if elem in env.ignorableElements:
            env.state = env.IGNORING
        elif elem == 'office:annotation':
            env.state = env.READING_STATEMENT
        elif elem == 'text:change-start':
            env.state = env.READING_EXPRESSION
            env.exprHasStyle = False
        else:
            if env.state == env.IGNORING:
                pass
            elif env.state == env.READING_CONTENT:
                if elem in env.impactableElements:
                    #print 'Start -', elem,
                    #if elem == Table.OD: print attrs['table:name'],
                    if env.mode == env.ADD_IN_SUBBUFFER:
                        env.addSubBuffer()
                    env.currentBuffer.addElement(elem)
                    #print 'id:', id(env.currentBuffer)
                env.currentBuffer.dumpStartElement(elem, attrs)
            elif env.state == env.READING_STATEMENT:
                pass
            elif env.state == env.READING_EXPRESSION:
                if elem == 'text:span' and not env.currentContent.strip():
                    env.currentBuffer.dumpStartElement(elem, attrs)
                    env.exprHasStyle = True
    def endElement(self, elem):
        env = self.environment
        env.onEndElement(elem)
        if elem in env.ignorableElements:
            env.state = env.READING_CONTENT
        elif elem == 'office:annotation':
            env.state = env.READING_CONTENT
        else:
            if env.state == env.IGNORING:
                pass
            elif env.state == env.READING_CONTENT:
                env.currentBuffer.dumpEndElement(elem)
                if elem in env.impactableElements:
                    if isinstance(env.currentBuffer, MemoryBuffer):
                        #print 'End -', elem, \
                        #      env.currentBuffer.content.encode('utf-8'), 'id:', \
                        #      id(env.currentBuffer)
                        isMainElement = env.currentBuffer.isMainElement(elem)
                        # Unreference the element among the 'elements' attribute
                        env.currentBuffer.unreferenceElement(elem)
                        if isMainElement:
                            parent = env.currentBuffer.parent
                            if not env.currentBuffer.action:
                                #print 'Delete subbuffer & transfer to parent'
                                # Delete this buffer and transfer content to parent
                                env.currentBuffer.transferAllContent()
                                parent.removeLastSubBuffer()
                                env.currentBuffer = parent
                            else:
                                #print 'Action linked to this buffer'
                                if isinstance(parent, FileBuffer):
                                    # Execute buffer action and delete the buffer
                                    env.currentBuffer.action.execute()
                                    parent.removeLastSubBuffer()
                                env.currentBuffer = parent
                            env.mode = env.ADD_IN_SUBBUFFER
            elif env.state == env.READING_STATEMENT:
                if elem == Text.OD:
                    statement = env.currentContent.strip()
                    env.currentContent = ''
                    # Manage statement
                    oldCb = env.currentBuffer
                    actionElemIndex = oldCb.createAction(statement)
                    if actionElemIndex != -1:
                        env.currentBuffer = oldCb.\
                                            transferActionIndependentContent(
                                                actionElemIndex)
                        if env.currentBuffer == oldCb:
                            env.mode = env.ADD_IN_SUBBUFFER
                        else:
                            env.mode = env.ADD_IN_BUFFER
            elif env.state == env.READING_EXPRESSION:
                if elem == 'text:change-end':
                    expression = env.currentContent.strip()
                    env.currentContent = ''
                    # Manage expression
                    env.currentBuffer.addExpression(expression)
                    if env.exprHasStyle:
                        env.currentBuffer.dumpEndElement('text:span')
                    env.state = env.READING_CONTENT
    def characters(self, content):
        env = self.environment
        if env.state == env.IGNORING:
            pass
        elif env.state == env.READING_CONTENT:
            env.currentBuffer.dumpContent(content)
        elif env.state == env.READING_STATEMENT:
            if env.currentElement == Text.OD:
                env.currentContent += content
        elif env.state == env.READING_EXPRESSION:
            env.currentContent += content

# ------------------------------------------------------------------------------
class Renderer:
    def __init__(self, template, context, result, pythonWithUnoPath=None,
                 ooPort=2002):
        '''This Python Open Document Renderer (PodRenderer) loads a document
        template (p_template) which is a OpenDocument file with some elements
        written in Python. Based on this template and some Python objects
        defined in p_context, the renderer generates an OpenDocument file
        (p_result) that instantiates the p_template and fills it with objects
        from the p_context. If p_result does not end with .odt, the Renderer
        will call OpenOffice to perform a conversion. If the Python interpreter
        which runs the current script is not UNO-enabled, this script will
        run, in another process, a UNO-enabled Python interpreter (whose path
        is p_pythonWithUnoPath) which will call OpenOffice. In both cases, we
        will try to connect to OpenOffice in server mode on port p_ooPort.'''
        self.template = template
        self.templateZip = zipfile.ZipFile(template)
        self.result = result
        self.resultContent = None
        self.tempFolder = None
        self.curdir = os.getcwd()
        self.env = None
        self.pyPath = pythonWithUnoPath
        self.ooPort = ooPort
        self.prepareFolders()
        # Unzip template
        self.unzipFolder = os.path.join(self.tempFolder, 'unzip')
        os.mkdir(self.unzipFolder)
        for zippedFile in self.templateZip.namelist():
            fileName = os.path.basename(zippedFile)
            folderName = os.path.dirname(zippedFile)
            # Create folder if needed
            fullFolderName = self.unzipFolder
            if folderName:
                fullFolderName = os.path.join(fullFolderName, folderName)
                if not os.path.exists(fullFolderName):
                    os.makedirs(fullFolderName)
            # Unzip file
            if fileName:
                fullFileName = os.path.join(fullFolderName, fileName)
                f = open(fullFileName, 'wb')
                fileContent = self.templateZip.read(zippedFile)
                f.write(fileContent)
                if fileName == 'content.xml':
                    self.resultContent = fileContent
                f.close()
        self.templateZip.close()
        # Initialise environment
        if hasattr(context, '__dict__'):
            evalContext = context.__dict__.copy()
        elif isinstance(context, dict) or isinstance(context, UserDict):
            evalContext = context.copy()
        else:
            raise PodError(BAD_CONTEXT)
        self.env = Environment(context)
        fileBuffer = FileBuffer(self.env, os.path.join(self.tempFolder,
                                                       'content.xml'))
        self.env.currentBuffer = fileBuffer
        # Initialise sax handler
        self.saxHandler = SaxHandler(self, self.env)
    def prepareFolders(self):
        # Check if I can write the result
        if os.path.exists(self.result):
            raise PodError(RESULT_FILE_EXISTS % self.result)
        try:
            f = open(self.result, 'w')
            f.write('Hello')
            f.close()
        except OSError, oe:
            raise PodError(CANT_WRITE_RESULT % (self.result, oe))
        self.result = os.path.abspath(self.result)
        os.remove(self.result)
        # Check that temp folder does not exist
        self.tempFolder = os.path.abspath(self.result) + '.temp'
        if os.path.exists(self.tempFolder):
            raise PodError(TEMP_FOLDER_EXISTS % self.tempFolder)
        try:
            os.mkdir(self.tempFolder)
        except OSError, oe:
            raise PodError(CANT_WRITE_TEMP_FOLDER % (self.result, oe))
    def run(self):
        xml.sax.parseString(self.resultContent, self.saxHandler)
    def finalize(self):
        self.env.currentBuffer.content.close()
        shutil.copy(os.path.join(self.tempFolder, 'content.xml'),
                    os.path.join(self.unzipFolder, 'content.xml'))
        resultOdtName = os.path.join(self.tempFolder, 'result.odt')
        resultOdt = zipfile.ZipFile(resultOdtName, 'w')
        os.chdir(self.unzipFolder)
        for dir, dirnames, filenames in os.walk('.'):
            for f in filenames:
                resultOdt.write(os.path.join(dir, f)[2:])
                # [2:] is there to avoid havin './' in the path in the zip file.
        resultOdt.close()
        resultType = os.path.splitext(self.result)[1]
        try:
            if resultType == '.odt':
                # Simply move the ODT result to the result
                os.rename(resultOdtName, self.result)
            else:
                if len(resultType) < 1:
                    raise PodError(BAD_RESULT_TYPE % self.result)
                # Call OpenOffice to perform the conversion
                if (not isinstance(self.ooPort, int)) and \
                   (not isinstance(self.ooPort, long)):
                    raise PodError(BAD_OO_PORT % str(self.ooPort))
                try:
                    from appy.pod.converter import Converter, ConverterError
                    try:
                        Converter(resultOdtName,resultType[1:],
                                  self.ooPort).run()
                    except ConverterError, ce:
                        raise PodError(CONVERT_ERROR % str(ce))
                except ImportError:
                    # I do not have UNO. So try to launch a UNO-enabled Python
                    # interpreter which should be in self.pyPath.
                    if not self.pyPath:
                        raise PodError(NO_PY_PATH % resultType)
                    if self.pyPath.find(' ') != -1:
                        raise PodError(BLANKS_IN_PATH % self.pyPath)
                    ooPyExe = os.path.join(self.pyPath, 'python')
                    if (not os.path.exists('%s.bat' % ooPyExe)) and \
                       (not os.path.exists('%s.exe' % ooPyExe)) and \
                       (not os.path.exists('%s' % ooPyExe)):
                        raise PodError(NO_PYTHON % ooPyExe)
                    if resultOdtName.find(' ') != -1:
                        qResultOdtName = '"%s"' % resultOdtName
                    else:
                        qResultOdtName = resultOdtName
                    convScript = '%s/pod/converter.py' % \
                                 os.path.dirname(appy.__file__)
                    if convScript.find(' ') != -1:
                        convScript = '"%s"' % convScript
                    cmd = '%s %s %s %s -p%d' % \
                        (ooPyExe, convScript, qResultOdtName, resultType[1:],
                         self.ooPort)
                    prgPipes = os.popen3(cmd)
                    convertOutput = prgPipes[2].read()
                    for pipe in prgPipes:
                        pipe.close()
                    if convertOutput:
                        raise PodError(CONVERT_ERROR % convertOutput)
                # Ok I have the result. Move it to the correct name
                resultName = os.path.splitext(resultOdtName)[0] + resultType
                os.rename(resultName, self.result)
        finally:
            os.chdir(self.curdir)
            FolderDeleter.delete(self.tempFolder)
# ------------------------------------------------------------------------------
