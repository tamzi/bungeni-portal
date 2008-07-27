from zope.security.interfaces import IGroupAwarePrincipal
from zope.app.security.principalregistry import principalRegistry
from zope.component import createObject, getMultiAdapter
from zope.publisher.browser import BrowserPage, BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile
from ore.alchemist import Session
from cgi import parse_qsl

from marginalia.tools.SequenceRange import SequenceRange, SequencePoint
from marginalia.tools.XPathRange import XPathRange
from marginalia.tools.RangeInfo import RangeInfo, mergeRangeInfos
from marginalia.schema import annotations_table, AnnotationMaster
from marginalia.interfaces import IMarginaliaAnnotatableAdaptor
from datetime import datetime
from marginalia.browser import parser

class MarginaliaPage(BrowserPage):
    """All the methods required by Marginalia Annotation Tab."""

    def getTitle(self):
        return 'Annotation Utility'

    def getDescription(self):
        return ''

    def getBaseUrl(self):
        obj = IMarginaliaAnnotatableAdaptor(self.context)
        return obj.getAnnotatedUrl(self.request)

    def getModificationDate(self):
        from datetime import datetime
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    def getFeedUID(self):
        return 'tag:marginalia:annotation'

    def getAnnotation(self, id):
        """Returns the annotation object."""
        session = Session()
        annotations = session.query(AnnotationMaster).filter(AnnotationMaster.id==id).all()
        if annotations:
            return annotations[0]

    def getAuthenticatedUserId(self):
        """Returns the currently authenticated member."""
        return self.request.principal.id

    def getAuthenticatedUser(self):
        """Returns the currently authenticated member."""
        if hasattr(self.request.principal, 'getLogin'):        
            return self.request.principal.getLogin()
        else:
            return self.request.principal.title            

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
        
    def _createAnnotation(self):
        """Create an annotation from the POST request."""
        session = Session()
        # TODO: do something useful with 'access'. Plone already
        # enforces security based on ownership, so access is 'private'
        # by default. 'public' access could mean sharing the annotation
        # with the 'Anonymous' role, though a more restrictive
        # implementation such as 'Member' or 'MemberOfParliament'
        # probably makes more sense.
        params = {
            'url': '',
            'block-range': '',
            'xpath-range': '',
            'note': '',
            'access': '',
            'action': '',
            'quote': '',
            'quote_title': '',
            'quote_author': '',
            'quote_authorid': '',            
            'link': '',            
            }
        # TODO: Don't treat query string and body parameters as equivalent.
        # Query string parameters should identify the resources, while
        # parameters in the body should specify the action to take.
        params.update(self.request)
        params.update(parse_qsl(self.request['QUERY_STRING']))
        if self.request.environment.has_key('wsgi.input'):
            params.update(parse_qsl(self.request.environment['wsgi.input'].read()))        
        sequenceRange = SequenceRange(params['sequence-range'])
        xpathRange = XPathRange(params['xpath-range'])
        params['start_block'] = sequenceRange.start.getPaddedPathStr()
        params['start_xpath'] = xpathRange.start.getPathStr()
        params['start_word'] = xpathRange.start.words
        params['start_char'] = xpathRange.start.chars
        params['end_block'] = sequenceRange.end.getPaddedPathStr()
        params['end_xpath'] = xpathRange.end.getPathStr()
        params['end_word'] = xpathRange.end.words
        params['end_char'] = xpathRange.end.chars
        del params['sequence-range']
        del params['xpath-range']
        params['modified'] = datetime.now()
        params['quote_author'] = self.getAuthenticatedUser()
        params['quote_authorid'] = self.getAuthenticatedUserId()

        annotation = AnnotationMaster()
        for key in annotations_table.c.keys():
            value = params.get(key, None)
            if value == None:
                continue
            setattr(annotation, key, unicode(value))        
        session.save(annotation)
        session.commit()

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
        if not annotation or annotation.quote_author != \
               self.getAuthenticatedUser():
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
        if annotation and annotation.quote_author == self.getAuthenticatedUser():
            session = Session()
            session.delete(annotation)
            self.request.response.setStatus('NoContent')
            return
        self.request.response.setStatus('BadRequest') # No id

    def __call__(self):
        rest_verb_map = {
            'GET': self._listAnnotations, # Finds listAnnotations.pt in skins
            'POST': self._createAnnotation,
            'PUT': self._updateAnnotation,
            'DELETE': self._deleteAnnotation,
            }
        verb = rest_verb_map[self.request['REQUEST_METHOD']]
        return verb()

    def renderQuote(self):
        plaintext = createObject('zope.source.plaintext',
                                 self.context.quote)
        view = getMultiAdapter((plaintext, self.request), name=u'')
        return view.render()

    def getSortedFeedEntries(self, user, url, block=None, filter_name=None, filter_group=None, filter_type=None, search_string=None):
        """ The incoming query specifies an URL like 
        http://server/somedocument/annotate/#*
        where the fragment identifier ('#*') specifies all annotations
        for this page. The document is cataloged under the URL w/o
        fragment, so chop that to get the same effect. 

        To query per fragment identifier, filter the returned
        annotations by looking at their 'url' field.
        """
        session = Session()
        query = session.query(AnnotationMaster)

        if filter_name and "select_all" in filter_name:
            filter_name = None
        if filter_group and "select_all" in filter_group:
            filter_group = None

        if filter_name:
            filter_name = filter_name.split(";")
        if filter_group:
            filter_group = filter_group.split(";")

        filter_type = [u'annotate', ]
        
        query = query.filter(AnnotationMaster.url == unicode(url))
        if search_string:
            query = query.filter(AnnotationMaster.note.like("%"+search_string+"%"))            
        if filter_type:
            query = query.filter(AnnotationMaster.edit_type.in_(filter_type))
        if filter_name:
            query = query.filter(AnnotationMaster.quote_author.in_(filter_name))
                                 
        user = self.getAuthenticatedUser()

        annotation_list = []
        public_annotations = query.filter(AnnotationMaster.access == u'public').all()
        users_annotations =  query.filter(AnnotationMaster.quote_author == user).all()                        
        annotation_list.extend(public_annotations)
        annotation_list.extend(users_annotations)
                    
        # Filter by position (if block was specified )
        annotations = [ ]
        uids = []
        if block is not None and block != '':
            block = SequencePoint(block);
            for annotation in annotation_list:
                if annotation.id in uids:
                    continue
                uids.append(annotation.id)                
                arange = annotation.getSequenceRange( )
                if arange.start.compareInclusive(block) <= 0 and \
                       arange.end.compareInclusive(block) >= 0:            
                    annotations.append( annotation )
            return annotations

        for annotation in annotation_list:
            if annotation.id in uids:
                continue
            uids.append(annotation.id)                
            annotations.append(annotation)

        if filter_group:
            filter_group = set(filter_group)
            group_annotations = []
            for annotation in annotations:
                principal = principalRegistry.getPrincipals(annotation.quote_author)
                if not principal:
                    continue
                principal = principal[0]
                groups = principal.groups
                if not groups:
                    groups = [principal.id,]
                if not set(groups).intersection(filter_group):
                    continue
                group_annotations.append(annotation)
            annotations = group_annotations
        return annotations

    def getRangeInfos(self, user, url):
        """ As with getSortedFeedEntries, but instead of returning individual
        annotations, return BlockInfo entries. """
        annotations = self.getSortedFeedEntries(user, url)
        infos = [ ]
        for annotation in annotations:
            info = RangeInfo()
            info.fromAnnotation(annotation)
            infos.append(info)
        return mergeRangeInfos(infos)


class AmendmentPage(MarginaliaPage):
    """All the methods required by Marginalia Amendment Tab."""
    def __call__(self):
        rest_verb_map = {
            'GET': self._listAnnotations, # Finds listAnnotations.pt in skins
            'POST': self._createAnnotation,
            'PUT': self._updateAnnotation,
            'DELETE': self._deleteAnnotation,
            }
        verb = rest_verb_map[self.request['REQUEST_METHOD']]
        return verb()

    def getSortedFeedEntries(self, user, url, block=None, filter_name=None, filter_group=None, filter_type=None, search_string=None):
        """ Processes the  incoming query."""
        session = Session()
        query = session.query(AnnotationMaster)

        if filter_name and "select_all" in filter_name:
            filter_name = None
        if filter_type and "select_all" in filter_type:
            filter_type = None
        if filter_group and "select_all" in filter_group:
            filter_group = None

        if filter_name:
            filter_name = filter_name.split(";")
        if filter_type:
            filter_type = filter_type.split(";")
        if filter_group:
            filter_group = filter_group.split(";")

        if not filter_type:
            filter_type = [u'comment', u'delete', u'insert', u'replace']
        if 'annotate' in filter_type:
            raise Exception, "Cannot display annotations on the amendment page"            
        
        query = query.filter(AnnotationMaster.url == unicode(url))
        if search_string:            
            query = query.filter(AnnotationMaster.note.like("%"+search_string+"%"))
        if filter_type:
            query = query.filter(AnnotationMaster.edit_type.in_(filter_type))
        if filter_name:
            query = query.filter(AnnotationMaster.quote_author.in_(filter_name))
                                 
        user = self.getAuthenticatedUser()

        annotation_list = []
        public_annotations = query.filter(AnnotationMaster.access == u'public').all()
        users_annotations =  query.filter(AnnotationMaster.quote_author == user).all()                        
        annotation_list.extend(public_annotations)
        annotation_list.extend(users_annotations)
                    
        # Filter by position (if block was specified )
        annotations = [ ]
        uids = []
        if block is not None and block != '':
            block = SequencePoint(block);
            for annotation in annotation_list:
                if annotation.id in uids:
                    continue
                uids.append(annotation.id)                
                arange = annotation.getSequenceRange( )
                if arange.start.compareInclusive(block) <= 0 and \
                       arange.end.compareInclusive(block) >= 0:            
                    annotations.append( annotation )
            return annotations

        for annotation in annotation_list:
            if annotation.id in uids:
                continue
            uids.append(annotation.id)                
            annotations.append(annotation)

        if filter_group:
            filter_group = set(filter_group)
            group_annotations = []
            for annotation in annotations:
                principal = principalRegistry.getPrincipals(annotation.quote_author)
                if not principal:
                    continue
                principal = principal[0]
                groups = principal.groups
                if not groups:
                    groups = [principal.id,]                
                if not set(groups).intersection(filter_group):
                    continue
                group_annotations.append(annotation)
            annotations = group_annotations
                
        return annotations

class DownloadPage(MarginaliaPage):
    """All the methods required by Marginalia Amendment Tab."""
    def __call__(self):
        response = self.request.response
        contents = str(ViewPageTemplateFile('document.pt')(self))
        response.setHeader('Content-Type', 'text/html')

        if self.request.has_key('filter_type'):
            page = u'amend.html'
        else:
            page = u'annote.html'
            
        try:
            contents = parser.physical_representation(contents)
        except IndexError, err:
            view = getMultiAdapter((self.context, self.request), name=page)
            view.statusmessage = "Click on the 'Search' button to refresh the page before using the 'Download' button"
            return view()
        except Exception, err:
            view = getMultiAdapter((self.context, self.request), name=page)
            view.statusmessage = str(err)
            return view()
            
        response.setHeader('Content-Disposition', 'attachment;filename="document.html"')        
        return contents

    def getDocumentBody(self):
        """Returns the downloadable representation of the annotated document."""
        return self.request['content']
    
class MarginaliaAnnotationView(BrowserView):
    """Annotation View Class. """
    def getPortalGroups(self):
        """Returns portal wide groups."""
        for principal in principalRegistry.getPrincipals(''):
            if IGroupAwarePrincipal.providedBy(principal):
                continue
            yield principal.id, principal.title
    
    def getOwnerList(self):
        """Return a list of members who have added annotations."""
        user = self.getAuthenticatedUser()
        view = getMultiAdapter((self.context, self.request), name=u'annotate')
        url = view.getBaseUrl()
        annotations = view.getSortedFeedEntries(user, url)
        return set([annotation.quote_author for annotation in annotations] )

    def getAuthenticatedUserId(self):
        """Returns the currently authenticated member."""
        return self.request.principal.id

    def getAuthenticatedUser(self):
        """Returns the currently authenticated member."""
        if hasattr(self.request.principal, 'getLogin'):        
            return self.request.principal.getLogin()
        else:
            return self.request.principal.title            

    def getBodyText(self):
        """Returns annotated url."""
        obj = IMarginaliaAnnotatableAdaptor(self.context)
        return obj.getBodyText()

    def isAnnotatable(self):
        """Returns a boolean True"""
        obj = IMarginaliaAnnotatableAdaptor(self.context)
        return obj.isAnnotatable()

    def getAnnotatedUrl(self):
        """Returns a boolean True"""
        obj = IMarginaliaAnnotatableAdaptor(self.context)
        return obj.getAnnotatedUrl(self.request)

