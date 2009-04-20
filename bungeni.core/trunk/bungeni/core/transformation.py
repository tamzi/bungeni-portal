import lxml.etree

from zope import interface
from zope import component
from zope.traversing.interfaces import ITraversable

from plone.transforms.interfaces import ITransformEngine
from plone.transforms.message import PloneMessageFactory as _
from plone.transforms.stringiter import StringIter
from plone.transforms.transform import Transform
from plone.transforms.transform import TransformResult
from plone.transforms.utils import html_bodyfinder
  
class TransformationAdapter(object):
    interface.implements(ITraversable)
    default_source_mimetype = 'text/plain'
    
    def __init__(self, context):
        self.context = context

    def traverse(self, name, furtherPath):
        if len(furtherPath) == 1:
            source_mimetype = self.default_source_mimetype
        elif len(furtherPath) == 3:
            source_mimetype = "%s/%s" % (name, furtherPath.pop())
            name = furtherPath.pop()

        mimetype = "%s/%s" % (name, furtherPath.pop())
        engine = component.getUtility(ITransformEngine)
        result = engine.transform(
            (self.context,), source_mimetype, mimetype)

        if result is None:
            raise RuntimeError(
                "Unable to transform data from mime-type '%s' to '%s'." % (
                    source_mimetype, mimetype))
                
        return u"".join(result.data)

class HtmlFragmentOpenDocumentTransform(Transform):
    """A transform which converts an HTML fragment to an OpenDocument
    Format fragment."""

    title = _(u'title_html_fragment_odf_transform',
              default=u'HTML fragment to OpenDocument format')

    inputs = ("text/html", )
    output = "application/vnd.oasis.opendocument.text-fragment"

    xslt_transform = lxml.etree.XSLT(
        lxml.etree.fromstring("""\
    <xsl:stylesheet
      xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
      xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
      version="1.0">

    <xsl:output encoding="UTF-8"/>

    <xsl:template match="p">
    <xsl:apply-templates />
    </xsl:template>

    <xsl:template match="b">
    <xsl:element name="text:p">
    <xsl:value-of select="." />
    </xsl:element>
    </xsl:template>

    </xsl:stylesheet>
    """))
    
    def transform(self, data, options=None):
        if self._validate(data) is None:
            return None

        doc = lxml.html.fromstring(u"<div>%s</div>" % u"".join(data))
        result_tree = self.xslt_transform(doc)
        data = unicode(result_tree)

        # strip XML declaration since this transform deals with
        # fragments.
        data = data.lstrip('<?xml version="1.0"?>')

        return TransformResult(StringIter(data))
