from zope.component import createObject, getMultiAdapter
from zope.publisher.browser import BrowserPage, BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile
from ore.alchemist.vocabulary import DatabaseSource, ObjectSource, Session
from cgi import parse_qsl

from marginalia.tools.SequenceRange import SequenceRange, SequencePoint
from marginalia.tools.XPathRange import XPathRange, XPathPoint
from marginalia.tools.RangeInfo import RangeInfo, mergeRangeInfos


class ViewAnnotation(BrowserPage):

    __call__ = ViewPageTemplateFile('annotationview.pt')

    def renderQuote(self):
        plaintext = createObject('zope.source.plaintext',
                                 self.context.quote)
        view = getMultiAdapter((plaintext, self.request), name=u'')
        return view.render()


class AnnotationQuery(BrowserPage):
    def getTitle(self):
        return 'Annotation Utility'

    def getDescription(self):
        return ''

    def getBaseUrl(self):
        view = getMultiAdapter((self.context, self.request), name=u'absolute_url')
        return view()

    def getModificationDate(self):
        from datetime import datetime
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    def getFeedUID(self):
        return 'tag:marginalia:annotation'

    def _listAnnotations(self):
        """Returns a list of Annotations."""
        params = { 'format' : 'atom' }
        params.update(parse_qsl(self.request['QUERY_STRING']))
        format = params['format']

        response = self.request.response
                                
        if 'atom' == format:
            #jacob - Check encoding
            response.setHeader('Content-Type', 'application/atom+xml')                        
            return str(ViewPageTemplateFile('listAnnotations.pt')(self))
        elif 'blocks' == format:
            response.setHeader('Content-Type', 'application/xml')            
            return str(ViewPageTemplateFile('listBlocks.pt')(self))
        
    def _createAnnotation(self):
        """Create an annotation from the POST request."""
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
        sequenceRange = SequenceRange( params[ 'sequence-range' ] )
        xpathRange = XPathRange( params[ 'xpath-range' ] )
        print params.get("edit_type", "")
        params[ 'start_block' ] = sequenceRange.start.getPaddedPathStr( )
        params[ 'start_xpath' ] = xpathRange.start.getPathStr( )
        params[ 'start_word' ] = xpathRange.start.words
        params[ 'start_char' ] = xpathRange.start.chars
        params[ 'end_block' ] = sequenceRange.end.getPaddedPathStr( )
        params[ 'end_xpath' ] = xpathRange.end.getPathStr( )
        params[ 'end_word' ] = xpathRange.end.words
        params[ 'end_char' ] = xpathRange.end.chars
        del params[ 'sequence-range' ]
        del params[ 'xpath-range' ]
        plone = getToolByName(self, 'portal_url').getPortalObject()
        obj_id = plone.generateUniqueId('Annotation')
        
        #new_id = self.invokeFactory('Annotation', id=obj_id, **params)

        new_id = self.invokeFactory('Annotation', id=obj_id)        
        annotation = getattr(self, new_id)
        annotation.update(**params)

        self.request['RESPONSE'].setStatus('Created')
        location = annotation.absolute_url()
        self.request['RESPONSE'].setHeader("location", location)
        return new_id

    def _updateAnnotation(self):
        """Updates an annotation."""
        params = {}
        params.update(self.request)
        params.update(parse_qsl(self.request['QUERY_STRING']))
        annotation = self.get(params['id'], None)
        if not annotation:
            self.request['RESPONSE'].setStatus('BadRequest')
            return
        if params.has_key('link'):
            if  params['link'].startswith("http://"):
                annotation.hyper_link = params['link']
                params.pop('link')
            else:
                if hasattr(annotation, 'hyper_link'):
                    del annotation.hyper_link
            
        annotation.edit(**params)
        if params.has_key("access"):
            workflow = getToolByName(self, 'portal_workflow')
            annotation_workflow = workflow.getWorkflowsFor(annotation)[0]
            status = workflow.getStatusOf("annotation_workflow", annotation)
            if params['access'] == "public" and status['review_state']=="private":
                annotation_workflow.doActionFor(annotation, "publish")
            elif params['access'] == "private" and status['review_state']=="published":
                annotation_workflow.doActionFor(annotation, "retract")
            annotation.reindexObject()
            
        self.request['RESPONSE'].setStatus('NoContent')

    def _deleteAnnotation(self):
        """Deletes an Annotation."""
        name, value = self.request['QUERY_STRING'].split('=')
        if value:
            self.manage_delObjects(value)
            self.request['RESPONSE'].setStatus('NoContent')
            return
        self.request['RESPONSE'].setStatus('BadRequest') # No id

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
        return []
        catalog = getToolByName(self, 'portal_catalog')
			
        query = {
            'portal_type': 'Annotation',
            'getIndexed_url': url
            }
        if search_string:
            query['SearchableText'] = search_string

        public_annotations = catalog(query)
                    
        if user:
            query['Creator'] = user
            
        ps = catalog(query) + public_annotations

        # Filter by position (if block was specified )
        annotations = [ ]
        uids = []
        if block is not None and block != '':
            block = SequencePoint( block );
            for p in ps:
                annotation = p.getObject( )
                
                if annotation.UID() in uids:
                    continue
                uids.append(annotation.UID())
                
                arange = annotation.getSequenceRange( )
                if arange.start.compareInclusive( block ) <= 0 and arange.end.compareInclusive( block ) >= 0:
                    annotations.append( annotation )
        else:
            for p in ps:
                annotation = p.getObject( )
                if annotation.UID() in uids:
                    continue
                uids.append(annotation.UID())                
                annotations.append(annotation)

        if filter_name and "select_all" in filter_name:
            filter_name = None
        if filter_type and "select_all" in filter_type:
            filter_type = None

        if filter_name:
            filter_name = filter_name.split(",")
            annotations = [annotation for annotation in annotations if annotation.Creator() in filter_name]

        if filter_type:
            filter_type = filter_type.split(",")
            annotations = [annotation for annotation in annotations if annotation.getEditType() in filter_type]

        auth_member = self._getUser()        
        
        return  [annotation for annotation in annotations if auth_member.has_permission("View", annotation)]

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

from zope.formlib.form import EditForm, AddForm, Fields, applyChanges
from zope.formlib.namedtemplate import NamedTemplate
from zope.formlib.namedtemplate import NamedTemplateImplementation
from marginalia.interfaces import IAnnotation, IAnnotatable, IAnnotatableAdaptor
from zope.interface import implements
from zope.component import adapts

class AnnotationEditForm(EditForm):
    form_fields = Fields(IAnnotation).omit('__parent__', '__name__')
    label = u"Edit annotation"

    template = NamedTemplate('annotation.form')

class AnnotationAddForm(AddForm):
    form_fields = Fields(IAnnotation).omit('__parent__', '__name__')
    label = u"Add annotation"

    template = NamedTemplate('annotation.form')

    def create(self, data):
        annotation = createObject(u'marginalia.Annotation')
        applyChanges(annotation, self.form_fields, data)
        return annotation

class AnnotationView(BrowserView):
    """Annotation View Class. """
    def getOwnerList(self, request):
        """Return a list of members who have added annotations."""
        return []

    def getAuthenticatedUser(self):
        """Returns the currently authenticated member."""
        return "test"

    def getAnnotatedUrl(self, url):
        """Returns annotated url."""
        obj = IAnnotatableAdaptor(self.context)
        return obj.getAnnotatedUrl(url)

    def getBodyText(self):
        """Returns annotated url."""
        obj = IAnnotatableAdaptor(self.context)
        return obj.getBodyText()

    def isAnnotatable(self):
        """
        """
        obj = IAnnotatableAdaptor(self.context)
        return obj.isAnnotatable()

class AnnotationAdaptor(object):
    """
    """
    implements(IAnnotatable)
    adapts(IAnnotatableAdaptor)

    def __init__(self, context):
        self.context = context

    def getBodyText(self):
        return self.context.description
        
    def getAnnotatedUrl(self, url ):
        """Returns annotated url."""        
        x = url.find( '/annotate' )
        if -1 != x:
            url = url[ : x ]
        return url

    def isAnnotatable(self):
        """
        """
        return True


form_template = NamedTemplateImplementation(
    ViewPageTemplateFile('form.pt'))
