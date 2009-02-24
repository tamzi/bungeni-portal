from zope import component

from Products.Five.browser import BrowserView

from bungeni.marginalia.tools import SequenceRange, SequencePoint
from bungeni.marginalia.tools import XPathRange
from bungeni.marginalia.tools import RangeInfo, mergeRangeInfos

import interfaces

class RESTView(BrowserView):
    def __call__(self, **kw):
        rest_verb_map = {
            'GET': self._listAnnotations, # Finds listAnnotations.pt in skins
            'POST': self._createAnnotation,
            'PUT': self._updateAnnotation,
            'DELETE': self._deleteAnnotation,
            }
        verb = rest_verb_map[self.request['REQUEST_METHOD']]
        return verb(**kw)

    @property
    def tool(self):
        return component.getUtility(interfaces.IMarginaliaTool)
    
    def _createAnnotation(self, url=None, block_range=None, xpath_range=None,
                          note=None, access=None, status=None, action=None,
                          quote=None, quote_title=None, quote_author=None,
                          quote_authorid=None, link=None, sequence_range=None):
        """Create an annotation from the POST request."""
    
        # TODO: do something useful with 'access'. Plone already
        # enforces security based on ownership, so access is 'private'
        # by default. 'public' access could mean sharing the annotation
        # with the 'Anonymous' role, though a more restrictive
        # implementation such as 'Member' or 'MemberOfParliament'
        # probably makes more sense.
        
        sequenceRange = SequenceRange(sequence_range)
        xpathRange = XPathRange(xpath_range)

        params = {}
        params['start_block'] = sequenceRange.start.getPaddedPathStr()
        params['start_xpath'] = xpathRange.start.getPathStr()
        params['start_word'] = xpathRange.start.words
        params['start_char'] = xpathRange.start.chars
        params['end_block'] = sequenceRange.end.getPaddedPathStr()
        params['end_xpath'] = xpathRange.end.getPathStr()
        params['end_word'] = xpathRange.end.words
        params['end_char'] = xpathRange.end.chars
        params['modified'] = datetime.now()
        params['quote_author'] = self._get_authenticated_user()
        params['quote_authorid'] = self._get_authenticated_userid()
        
        if params['quote_authorid'] == 'zope.anybody':
            params['access'] = 'public'

        annotation = self.tool.create_annotation(**params)
        unique_id = str(annotation.id)
        
        self.request.response.setStatus('Created')
        self.request.response.setHeader('location', unique_id)
        return unique_id

    def _updateAnnotation(self):
        """Updates an annotation."""
        params = {}
        params.update(self.request)
        params.update(parse_qsl(self.request['QUERY_STRING']))
        if self.request.environment.has_key('wsgi.input'):
            params.update(parse_qsl(self.request.environment['wsgi.input'].read()))
        params['modified'] = datetime.now()
        
        annotation = self.getAnnotation(params['id'])
        if not annotation:
            self.request.response.setStatus('BadRequest')
            return

        if annotation.quote_authorid != self.getAuthenticatedUserId() and \
               not self.isAdmin():
            self.request.response.setStatus('BadRequest')
            return

        session = Session()
        
#         if params.has_key('link'):
#             if  params['link'].startswith("http://"):
#                 annotation.hyper_link = params['link']
#                 params.pop('link')
#             else:
#                 if annotation.hyper_link:
#                     annotation.hyper_link = ''

        for key in annotations_table.c.keys():
            value = params.get(key, None)
            if not value:
                continue
            setattr(annotation, key, value)        
        session.commit()

        self.request.response.setStatus('NoContent')

    def _deleteAnnotation(self):
        """Deletes an Annotation."""
        params = {}
        params.update(parse_qsl(self.request['QUERY_STRING']))
        if self.request.environment.has_key('wsgi.input'):
            params.update(parse_qsl(self.request.environment['wsgi.input'].read()))
        
        annotation_id = params.get('id', None)
        annotation = self.getAnnotation(annotation_id)
        if annotation and annotation.quote_authorid == self.getAuthenticatedUserId():
            session = Session()
            session.delete(annotation)
            self.request.response.setStatus('NoContent')
            return
        self.request.response.setStatus('BadRequest') # No id

    def _listAnnotations(self):
        """Returns a list of Annotations."""
        params = { 'format' : 'atom' }
        params.update(parse_qsl(self.request['QUERY_STRING']))
        if self.request.environment.has_key('wsgi.input'):
            params.update(parse_qsl(self.request.environment['wsgi.input'].read()))
        format = params['format']
        response = self.request.response
                                
        if 'atom' == format:
            response.setHeader('Content-Type', 'application/atom+xml')                        
            return str(ViewPageTemplateFile('listAnnotations.pt')(self))

        elif 'blocks' == format:
            response.setHeader('Content-Type', 'application/xml')            
            return str(ViewPageTemplateFile('listBlocks.pt')(self))

    def _get_authenticated_user_id(self):
        """Returns the currently authenticated member."""
        return self.request.principal.id
    
    def _get_authenticated_user(self):
        """Returns the currently authenticated member."""
        
        if hasattr(self.request.principal, 'getLogin'):        
            return self.request.principal.getLogin()
        else:
            return self.request.principal.title            
