import lxml.html
import lxml.etree
import hashlib

from zope import interface
from zope import component
from zope.traversing.interfaces import ITraversable

from plone.transforms.interfaces import ITransformEngine
from plone.transforms.message import PloneMessageFactory as _
from plone.transforms.stringiter import StringIter
from plone.transforms.transform import Transform
from plone.transforms.transform import TransformResult

class TransformationAdapter(object):
    interface.implements(ITraversable)
    default_source_mimetype = 'text/plain'
    
    def __init__(self, context):
        self.context = context

    def traverse(self, name, furtherPath):
        assert len(furtherPath) >= 3
        source_mimetype = "%s/%s" % (name, furtherPath.pop())
        mimetype = "%s/%s" % (furtherPath.pop(), furtherPath.pop())
        
        styles = tuple(furtherPath)
        del furtherPath[:]
        
        engine = component.getUtility(ITransformEngine)
        result = engine.transform(
            (self.context,), source_mimetype, mimetype, options={'styles': styles})

        if result is None:
            raise RuntimeError(
                "Unable to transform data from mime-type '%s' to '%s'." % (
                    source_mimetype, mimetype))
                
        return u"".join(result.data)

class HtmlFragmentOpenDocumentTransform(Transform):
    """A transform which converts an HTML fragment to an OpenDocument
    Format fragment.

    Currently supported elements:

    - b
    - em
    - i

    To-do:

    - table
    - tbody
    - thead
    - th
    - tr
    - td

    We can begin by enabling the XML comparison doctest extension from
    the ``lxml`` library.

      >>> import lxml.usedoctest

    Instantiate transform.
      
      >>> transform = HtmlFragmentOpenDocumentTransform()

    Boldface.
    
      >>> print "".join(transform.transform(('Hello, <b>world!</b>',)).data)
      <text:section xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
                    xmlns:html="http://www.w3.org/1999/xhtml"
                    text:name="Section-...">
          <text:p>
              <text:span>Hello, </text:span>
              <text:span text:style-name="Strong_20_Emphasis">world!</text:span>
          </text:p>
      </text:section>

    Root text-nodes gets wrapped in a <text:span> node.
    
      >>> print "".join(transform.transform(('Hello, <strong>world</strong>!',)).data)
      <text:section xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
                    xmlns:html="http://www.w3.org/1999/xhtml"
                    text:name="Section-...">
          <text:p>
              <text:span>Hello, </text:span>
              <text:span text:style-name="Strong_20_Emphasis">world</text:span>
              <text:span>!</text:span>
          </text:p>
      </text:section>

    Emphasis:
    
      >>> print "".join(transform.transform(
      ...    ('Hello, <b>world</b> and <em>universe</em>!',)).data)
      <text:section xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
                    xmlns:html="http://www.w3.org/1999/xhtml"
                    text:name="Section-...">
          <text:p>
              <text:span>Hello, </text:span>
              <text:span text:style-name="Strong_20_Emphasis">world</text:span>
              <text:span>and</text:span>
              <text:span text:style-name="Emphasis">universe</text:span>
              <text:span>!</text:span>
          </text:p>
      </text:section>

    """

    title = _(u'title_html_fragment_odf_transform',
              default=u'HTML fragment to OpenDocument format')

    inputs = ("text/html", )
    output = "application/vnd.oasis.opendocument.text-fragment"

    xslt_transform = lxml.etree.XSLT(
        lxml.etree.fromstring("""\
    <xsl:stylesheet
      xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
      xmlns:html="http://www.w3.org/1999/xhtml"
      xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
      version="1.0">

    <xsl:output encoding="UTF-8"/>

    <xsl:template match="processing-instruction()|comment()"/>

    <xsl:template match="html:html//html:p/text()">
      <text:span>
        <xsl:value-of select="." />
      </text:span>
    </xsl:template>
    
    <xsl:template match="html:html">
      <text:section>
        <xsl:attribute name="text:name">
           <xsl:value-of select="@name" />
        </xsl:attribute>
        <text:p>
        <xsl:apply-templates />
        </text:p>
      </text:section>
    </xsl:template>

    <xsl:template match="html:b | html:strong">
      <text:span text:style-name="Strong_20_Emphasis">
        <xsl:apply-templates select="node()"/>
      </text:span>
    </xsl:template>

    <xsl:template match="html:em | html:i">
      <text:span text:style-name="Emphasis">
        <xsl:apply-templates select="node()"/>
      </text:span>
    </xsl:template>

    </xsl:stylesheet>
    """))
    
    def transform(self, data, options={}):
        if self._validate(data) is None:
            return None

        # parse as HTML and serialize as XHTML
        body = "".join(data).encode('utf-8')
        doc = lxml.html.fromstring('<html name="Section-%s">%s</html>' % (
            hashlib.sha1(body).hexdigest(), body))
        lxml.html.html_to_xhtml(doc)
        body = lxml.html.tostring(doc)

        # reparse as valid XML, then apply transform
        doc = lxml.etree.fromstring(body)
        result_tree = self.xslt_transform(doc)
        
        # apply styles (optional)
        for style in options.get('styles', ()):
            tag, name = style.split(':')
            for element in result_tree.xpath(
                ".//text:%s" % tag, namespaces={
                    'text': "urn:oasis:names:tc:opendocument:xmlns:text:1.0"}):
                key = "{%s}style-name" % \
                      "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
                if key not in element.attrib:
                    element.attrib[key] = name

        data = unicode(result_tree)

        # strip XML declaration since this transform deals with
        # fragments.
        data = data.lstrip('<?xml version="1.0"?>')

        return TransformResult(StringIter(data))
