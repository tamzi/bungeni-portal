from xml.dom.minidom import parse
from xml.sax.saxutils import XMLGenerator
from xml.sax import saxutils, handler, make_parser
from StringIO import StringIO
from xml.sax.saxutils import writeattr
from xml.dom.minidom import parseString

class AnnotationFilter(XMLGenerator):
    def __init__(self, out):
        XMLGenerator.__init__(self, out)
        self.count = {}
        self._tags = []

    def startElement(self, name, attrs):
        flag = False
        if name =='em' and 'identifier' in attrs.keys():
            flag = True
            name = 'span'
            
        tag = StringIO()
        
        tag.write('<' + name)
        for (attrname, value) in attrs.items():            
            if flag and attrname == 'class':
                continue
            tag.write(' %s=' % attrname)
            writeattr(tag, value)
        tag.write('>')

        if flag:
            tag.write('</%s>' % name)

        tag.seek(0)
        data = tag.read()
        self._out.write(data)

        if flag:
            self._tags.append((True, data))
        else:
            self._tags.append((False, data))

    def endElement(self, name):
        replace, data = self._tags.pop()
        if replace:
            self._out.write(data)
        else:
            self._out.write('</%s>' % name)

def physical_representation(contents):
    """Creates a physical representation of an annotated document."""

    input_file = StringIO()
    output_file = StringIO()

    contents = contents.replace("&nbsp;", " ")
    contents = contents.replace("<br>", "<br/> ")

    parser = make_parser()
    parser.setContentHandler(AnnotationFilter(output_file))

    input_file.write(contents)
    input_file.seek(0)
    parser.parse(input_file)

    output_file.seek(0)
    output =  output_file.read()

    document = parseString(output)

    span_tags = [span for span in document.getElementsByTagName("span") if span.getAttribute('identifier')]

    position = {}
    index = 0
    for span_tag in span_tags:
        identifier = span_tag.getAttribute('identifier')
        positions = position.get(identifier, [])
        positions.append(index)
        position[identifier] = positions
        index = index + 1


    for identifier, positions in position.iteritems():
        first = span_tags[positions[0]]
        first.setAttribute("type", "begin")
        last = span_tags[positions[-2]]
        last.setAttribute("type", "end")

        for index in positions[1:-2]:
            span_tag = span_tags[index]
            span_tag.parentNode.removeChild(span_tag)
            span_tag.unlink()

    return document.toxml()



