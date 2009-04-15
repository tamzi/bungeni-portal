import copy
import zipfile
import lxml.etree

namespaces = {'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'}

class OpenDocument(object):
    def __init__(self, filename):
        self.filename = filename
        self.zipfile = zipfile.ZipFile(filename)
        self.contents = dict(
            (info, None) for info in self.zipfile.filelist)
        
    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.filename)

    def get(self, info):
        bytes = self.contents.get(info)
        if bytes is None:
            bytes = self.zipfile.read(info.filename)
            self.contents[info] = bytes
        return bytes

    def read(self, filename):
        info = self.zipfile.getinfo("content.xml")
        return self.get(info)

    def save(self, filename):
        outfile = zipfile.ZipFile(filename, 'w')
        try:
            for info in self.contents:
                bytes = self.get(info)
                outfile.writestr(info, bytes)
        finally:
            outfile.close()

    def merge(self, databases):
        """Mail-merge document using ``databases``.

        If a field appears outside a section, a single row is fetched
        immediately and consecutive rows only when a 'next marker'
        appears*.

        Sections that contain fields are repeated until the table of
        the field is exhausted. If fields from multiple tables are
        used, the tables must contain the same number of rows.

        Only the first section in a branch will be repeated; nested
        sections have no semantic value.

        *) To-do: Add support for 'next marker'.
        """
        
        info = self.zipfile.getinfo("content.xml")
        content = self.get(info)
        tree = lxml.etree.fromstring(content)

        # initialize table pointer directory
        tp = {}
        for db_name, database in databases.items():
            for tb_name in database:
                tp[db_name, tb_name] = 0

        # process elements that appear outside a section
        elements = []
        for element in tree.xpath(".//text:database-display", namespaces=namespaces):
            if element.xpath('ancestor::text:section', namespaces=namespaces):
                continue
            elements.append(element)
        process_elements(elements, databases, tp)

        # process sections
        for element in tree.xpath(".//text:section", namespaces=namespaces):
            if element.xpath('ancestor::text:section', namespaces=namespaces):
                continue

            while True:
                section = copy.deepcopy(element)
                tp_keys = process_elements(
                    section.xpath(".//text:database-display", namespaces=namespaces),
                    databases, tp)

                if tp_keys is None:
                    break
                else:
                    for key in tp_keys:
                        tp[key] = tp[key] + 1

                # add section
                element.addnext(section)
            
            # remove original section
            parent = element.getparent()
            parent.remove(element)

        content = lxml.etree.tostring(tree)
        self.contents[info] = content

def process_elements(elements, databases, tp):
    tp_keys = set()
    for element in elements:
        db_name = element.attrib["{%s}database-name" % namespaces['text']]
        tb_name = element.attrib["{%s}table-name" % namespaces['text']]
        cl_name = element.attrib["{%s}column-name" % namespaces['text']]

        key = db_name, tb_name
        tp_keys.add(key)
        pointer = tp[key]
        
        table = databases[db_name][tb_name]
        if pointer > len(table) - 1:
            return None
        element.text = table[pointer][cl_name]
        
    return tp_keys
