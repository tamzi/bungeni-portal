# encoding: utf-8
# download view to download a file or image
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from zope.app.publisher.browser import BrowserView
from zope.security import proxy
from tempfile import TemporaryFile


class RawView(BrowserView):
    implements(IPublishTraverse)
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.traverse_subpath = []

    def publishTraverse(self, request, name):
        self.traverse_subpath.append(name)
        return self

    def __call__(self):
        """Return File/Image Raw Data"""
        context = proxy.removeSecurityProxy( self.context )        
        response = self.request.response
        #response.setHeader('Content-Type', 'application/octect-stream')
        if len(self.traverse_subpath) != 1:
            return
        fname = self.traverse_subpath[0]     
        tempfile = TemporaryFile()
        data =  getattr(context,fname,None)
        if type(data) == buffer:
            tempfile.write(data)        
            return tempfile
 

