from zope.interface import Interface
from zope.schema import Text, TextLine

class ISimpleDocument(Interface):
    """Simple Document."""
    
    title = TextLine(
        title=u"Title",
        description=u"Title of the Document",
        required = True
        )
    
    description = Text(
        title=u"Description",
        description=u"Description of the document",
        required=True
        )

class IMarginaliaAnnotatable(Interface):
    '''Annotatable Marker Interface'''

    # Acts as a marker interface    
    
class IMarginaliaAnnotatableAdaptor(Interface):
    '''Annotatable Adaptor Interface'''

    def isAnnotatable():
        """Returns True if the object is annotatable """

    def getAnnotatedUrl(request):
        """Returns the annotated url """

    def getBodyText():
        """Returns the body text."""

    def getTitle():
        """Returns the title."""

class IMarginaliaAnnotation(Interface):
    """Stores details relating to the Annotation."""

    url = TextLine(
        title=u"Url",
        description=u"Url",
        )

    start_block = TextLine(
        title=u"Start Block",
        description=u"Start Block",
        )

    start_xpath = TextLine(
        title=u"Start XPath",
        description=u"Start Block",
        )

    start_word = TextLine(
        title=u"Start Word",
        description=u"Start Word",
        )

    start_char = TextLine(
        title=u"Start Character",
        description=u"Start Character",
        )

    end_block = TextLine(
        title=u"End Block",
        description=u"End Block",
        )

    end_xpath = TextLine(
        title=u"End XPath",
        description=u"End XPath",
        )

    end_word = TextLine(
        title=u"End Word",
        description=u"End Word",
        )

    end_char = TextLine(
        title=u"End Char",
        description=u"End Char",
        )

    note = TextLine(
        title=u"Note",
        description=u"Note",
        )

    access = TextLine(
        title=u"Access",
        description=u"Access",
        )
    
    action = TextLine(
        title=u"Action",
        description=u"Action",
        )
    
    edit_type = TextLine(
        title=u"Edit Type",
        description=u"Edit Type",
        )
    
    quote = TextLine(
        title=u"Quote",
        description=u"Quote",
        )
    
    quote_title = TextLine(
        title=u"Quote Title",
        description=u"Quote Title",
        )
    
    quote_author = TextLine(
        title=u"Quote Author",
        description=u"Quote Author",
        )

    link_title = TextLine(
        title=u"Link Title",
        description=u"Link Title",
        )
    
    indexed_url = TextLine(
        title=u"Indexed Url",
        description=u"Computed Field",
        )
    
    link = TextLine(
        title=u"Link",
        description=u"Reference Field",
        )    

    def getUserName():
        """Owner name."""

    def Title():
        """Title."""

    def Description():
        """Description."""

    def SearchableText():
        """Returns Searchable text."""

    def getEditType():
        """Returns edit type."""

    def getIndexed_url():
        """ There may be more than one annotatable area on a page,
        identified by fragment (#1, #2, ...). Annotations are queried
        per page (#*), so catalog under the page URL.

        Note that the URL includes the server name, so if the server is
        accessed with different names, annotations will be partitioned
        per name.
        
        TODO: Use config settings to strip server name.
        """

    def getLink():
        """Returns the reference link."""

    def getSequenceRange():
        """Returns Sequence Range."""
        
    def getXPathRange():
        """Returns XPath Range."""
        
