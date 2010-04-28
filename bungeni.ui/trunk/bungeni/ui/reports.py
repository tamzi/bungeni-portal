import re
import os
from appy.pod.renderer import Renderer
from zope.publisher.browser import BrowserView
import time
import datetime
import tempfile
from zope.security.proxy import removeSecurityProxy
import htmlentitydefs

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)


class DownloadODT(BrowserView):
    def __call__(self):
        body_text = removeSecurityProxy(self.context.body_text)
        odt_file = os.path.dirname(__file__) + '/calendar/agenda.odt'
        #appy.Renderer expects a file name of a file that does not exist.
        tempFileName = '/tmp/%f.odt' % ( time.time())
        params = {}
        params['body_text'] = unescape(body_text)
        renderer = Renderer(odt_file, params, tempFileName)
        #import pdb; pdb.set_trace()
        renderer.run()
        self.request.response.setHeader('Content-type', 'application/vnd.oasis.opendocument.text')
        self.request.response.setHeader('Content-disposition', 'inline;filename="'+
                                            removeSecurityProxy(self.context.report_type)+"_"+
                                            removeSecurityProxy(self.context.start_date).strftime('%Y-%m-%d')+'.odt"')
        f = open(tempFileName, 'rb')
        doc = f.read()
        f.close()
        os.remove(tempFileName)
        return doc
    
class  DownloadPDF(BrowserView):
    
    def __call__(self): 
        body_text = self.context.body_text
        odt_file = os.path.dirname(__file__) + '/calendar/agenda.odt'
        #appy.Renderer expects a file name of a file that does not exist.
        tempFileName = '/tmp/%f.pdf' % ( time.time())
        params = {}
        params['body_text'] = unescape(body_text)
        
        #uses system open office and python uno to generate pdf
        #TO DO : fix this to use user python
        renderer = Renderer(odt_file, params, tempFileName, pythonWithUnoPath="/usr/bin/python2.5")
        renderer.run()
        self.request.response.setHeader('Content-type', 'application/pdf')
        self.request.response.setHeader('Content-disposition', 'inline;filename="'
                            +removeSecurityProxy(self.context.report_type)+"_"
                            +removeSecurityProxy(self.context.start_date).strftime('%Y-%m-%d')+'.pdf"')
        f = open(tempFileName, 'rb')
        doc = f.read()
        f.close()
        os.remove(tempFileName)
        return doc 
        
