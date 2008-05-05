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

class MarginaliaPage(BrowserPage):
    """All the methods required by Marginalia."""

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
            'link': '',
            }
        # TODO: Don't treat query string and body parameters as equivalent.
        # Query string parameters should identify the resources, while
        # parameters in the body should specify the action to take.
        params.update(self.request)
        params.update(parse_qsl(self.request['QUERY_STRING']))
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

        params['quote_author'] = self.getAuthenticatedUser()

        annotation = AnnotationMaster()
        for key in annotations_table.c.keys():
            value = params.get(key, None)
            if value == None:
                continue
            setattr(annotation, key, value)        
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
        
        annotation = self.getAnnotation(params['id'])
        if not annotation or annotation.quote_author != \
               self.getAuthenticatedUser():
            self.request.response.setStatus('BadRequest')
            return

        session = Session()
        
        if params.has_key('link'):
            if  params['link'].startswith("http://"):
                annotation.hyper_link = params['link']
                params.pop('link')
            else:
                if annotation.hyper_link:
                    annotation.hyper_link = ''

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

    def getSortedFeedEntries(self, user, url, block=None, filter_name=None, filter_type=None, search_string=None):
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
        if filter_type and "select_all" in filter_type:
            filter_type = None

        if filter_name:
            filter_name = filter_name.split(",")
        if filter_type:
            filter_type = filter_type.split(",")
        
        query = query.filter(AnnotationMaster.url == url)
        if search_string:
            query = query.filter(AnnotationMaster.quote == search_string)
        if filter_type:
            query = query.filter(AnnotationMaster.edit_type.in_(filter_type))
        if filter_name:
            query = query.filter(AnnotationMaster.quote_author.in_(filter_name))
                                 
        user = self.getAuthenticatedUser()

        annotation_list = []
        public_annotations = query.filter(AnnotationMaster.access == 'public').all()
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

class MarginaliaAnnotationView(BrowserView):
    """Annotation View Class. """
    def getOwnerList(self):
        """Return a list of members who have added annotations."""
        user = self.getAuthenticatedUser()
        view = getMultiAdapter((self.context, self.request), name=u'annotate')
        url = view.getBaseUrl()
        annotations = view.getSortedFeedEntries(user, url)
        return set([annotation.quote_author for annotation in annotations] )

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

